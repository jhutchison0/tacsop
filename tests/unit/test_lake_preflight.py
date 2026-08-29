"""Tests for scripts/lake_preflight.py."""

import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import lake_preflight  # noqa: E402

from src.myproject.utils.machine import Machine  # noqa: E402

# --- fixtures ---


def _machine(tmp_path, *, scope=("work",), lakehouse=True):
    """A resolved machine whose lakehouse reference may or may not exist."""
    refs = {}
    if lakehouse:
        refs["lakehouse"] = tmp_path / "dis-lakehouse"
    return Machine(
        name="testbox",
        role="workstation",
        scope=scope,
        references=refs,
        known=True,
    )


def _git_repo(path, *, days_old=0):
    """A real git repo with one commit, backdated by days_old."""
    path.mkdir(parents=True, exist_ok=True)
    when = (datetime.now(timezone.utc) - timedelta(days=days_old)).isoformat()
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@t",
        "GIT_AUTHOR_DATE": when,
        "GIT_COMMITTER_DATE": when,
    }
    subprocess.run(["git", "init", "-q", str(path)], check=True, env=env)
    (path / "README.md").write_text("x")
    subprocess.run(["git", "-C", str(path), "add", "."], check=True, env=env)
    subprocess.run(
        ["git", "-C", str(path), "commit", "-q", "-m", "init"], check=True, env=env
    )
    return path


# --- check_reference_repo ---


class TestCheckReferenceRepo:
    def test_missing_reference_repo_fails(self, tmp_path):
        result = lake_preflight.check_reference_repo(_machine(tmp_path))

        assert result.status == "FAIL"
        assert "dis-lakehouse" in result.detail

    def test_present_reference_repo_passes(self, tmp_path):
        _git_repo(tmp_path / "dis-lakehouse")

        result = lake_preflight.check_reference_repo(_machine(tmp_path))

        assert result.status == "PASS"


# --- check_reference_currency ---


class TestCheckReferenceCurrency:
    def test_fresh_repo_passes_and_reports_age(self, tmp_path):
        _git_repo(tmp_path / "dis-lakehouse", days_old=3)

        result = lake_preflight.check_reference_currency(_machine(tmp_path))

        assert result.status == "PASS"
        assert "3 days" in result.detail

    def test_stale_repo_warns_with_its_age(self, tmp_path):
        _git_repo(tmp_path / "dis-lakehouse", days_old=90)

        result = lake_preflight.check_reference_currency(_machine(tmp_path))

        assert result.status == "WARN"
        assert "90 days" in result.detail

    def test_currency_says_it_did_not_reach_the_network(self, tmp_path):
        _git_repo(tmp_path / "dis-lakehouse", days_old=1)

        result = lake_preflight.check_reference_currency(_machine(tmp_path))

        assert "local" in result.detail.lower()


# --- check_target ---


class TestCheckTarget:
    def test_bare_invocation_fails(self):
        result = lake_preflight.check_target(None)

        assert result.status == "FAIL"
        assert "refusing" in result.detail.lower()

    def test_unknown_target_fails_and_names_the_valid_set(self):
        result = lake_preflight.check_target("prd")

        assert result.status == "FAIL"
        assert "dev" in result.detail and "prod" in result.detail

    def test_declared_target_passes(self):
        assert lake_preflight.check_target("dev").status == "PASS"

    def test_prod_passes_but_says_so_loudly(self):
        result = lake_preflight.check_target("prod")

        assert result.status == "PASS"
        assert "PRODUCTION" in result.detail


# --- check_leg_threading ---


class TestCheckLegThreading:
    def test_every_leg_carrying_the_target_passes(self):
        legs = ["stage1 --lake-profile dev", "stage2 --lake-profile dev"]

        assert lake_preflight.check_leg_threading("dev", legs).status == "PASS"

    def test_one_unthreaded_leg_fails_and_names_it(self):
        legs = ["stage1 --lake-profile dev", "stage2 --write"]

        result = lake_preflight.check_leg_threading("dev", legs)

        assert result.status == "FAIL"
        assert "stage2" in result.detail

    def test_a_leg_carrying_a_different_target_fails(self):
        legs = ["stage1 --lake-profile dev", "stage2 --lake-profile prod"]

        result = lake_preflight.check_leg_threading("dev", legs)

        assert result.status == "FAIL"
        assert "stage2" in result.detail

    def test_no_legs_declared_warns_rather_than_passing_silently(self):
        result = lake_preflight.check_leg_threading("dev", [])

        assert result.status == "WARN"


# --- check_environment ---


class TestCheckEnvironment:
    def test_missing_credentials_fail(self, monkeypatch):
        for var in lake_preflight.CREDENTIAL_VARS:
            monkeypatch.delenv(var, raising=False)

        result = lake_preflight.check_environment()

        assert result.status == "FAIL"

    def test_one_namespace_present_passes_with_a_note(self, monkeypatch):
        for var in lake_preflight.CREDENTIAL_VARS:
            monkeypatch.delenv(var, raising=False)
        for var in ("MINIO_ENDPOINT", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY"):
            monkeypatch.setenv(var, "x")

        result = lake_preflight.check_environment()

        assert result.status == "WARN"
        assert "S3_" in result.detail

    def test_both_namespaces_present_passes(self, monkeypatch):
        for var in lake_preflight.CREDENTIAL_VARS:
            monkeypatch.setenv(var, "x")

        assert lake_preflight.check_environment().status == "PASS"

    def test_environment_never_claims_the_lake_is_reachable(self, monkeypatch):
        for var in lake_preflight.CREDENTIAL_VARS:
            monkeypatch.setenv(var, "x")

        assert "presence" in lake_preflight.check_environment().detail.lower()


# --- check_local_data ---


class TestCheckLocalData:
    def test_no_data_files_passes(self, tmp_path):
        (tmp_path / "notes.md").write_text("x")

        assert lake_preflight.check_local_data(tmp_path).status == "PASS"

    def test_data_shaped_files_warn_with_a_byte_count(self, tmp_path):
        (tmp_path / "big.parquet").write_bytes(b"0" * 4096)

        result = lake_preflight.check_local_data(tmp_path)

        assert result.status == "WARN"
        assert "big.parquet" in result.detail

    def test_the_venv_is_not_counted(self, tmp_path):
        venv = tmp_path / ".venv" / "lib"
        venv.mkdir(parents=True)
        (venv / "vendored.parquet").write_bytes(b"0" * 4096)

        assert lake_preflight.check_local_data(tmp_path).status == "PASS"


# --- main ---


class TestMain:
    def test_bare_invocation_exits_nonzero(self, capsys):
        assert lake_preflight.main([]) == 1
        assert "FAIL" in capsys.readouterr().out

    def test_unknown_target_exits_nonzero(self, capsys):
        assert lake_preflight.main(["--target", "prd"]) == 1

    def test_strict_promotes_a_warn_to_a_failure(self, tmp_path, monkeypatch):
        _git_repo(tmp_path / "dis-lakehouse", days_old=1)
        monkeypatch.setattr(
            lake_preflight, "resolve_machine", lambda: _machine(tmp_path)
        )
        monkeypatch.setattr(lake_preflight, "REPO_ROOT", tmp_path)
        for var in lake_preflight.CREDENTIAL_VARS:
            monkeypatch.setenv(var, "x")

        # No legs declared is a WARN, so lenient passes and strict does not.
        assert lake_preflight.main(["--target", "dev"]) == 0
        assert lake_preflight.main(["--target", "dev", "--strict"]) == 1

    def test_output_names_every_check(self, tmp_path, monkeypatch, capsys):
        _git_repo(tmp_path / "dis-lakehouse", days_old=1)
        monkeypatch.setattr(
            lake_preflight, "resolve_machine", lambda: _machine(tmp_path)
        )
        monkeypatch.setattr(lake_preflight, "REPO_ROOT", tmp_path)

        lake_preflight.main(["--target", "dev"])
        out = capsys.readouterr().out

        for name in ("reference repo", "reference currency", "target",
                     "leg threading", "environment", "local data"):
            assert name in out
