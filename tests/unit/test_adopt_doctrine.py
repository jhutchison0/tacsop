"""Tests for scripts/adopt_doctrine.py."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import adopt_doctrine


# --- Fixtures ---


@pytest.fixture
def downstream(tmp_path):
    """A fake downstream repo root."""
    root = tmp_path / "downstream"
    root.mkdir()
    return root


# --- _detect_package ---


class TestDetectPackage:
    def test_single_src_subdir_returns_name(self, downstream):
        (downstream / "src" / "myrepo").mkdir(parents=True)
        assert adopt_doctrine._detect_package(downstream) == "myrepo"

    def test_no_src_raises(self, downstream):
        with pytest.raises(adopt_doctrine.DetectionError, match="no src/"):
            adopt_doctrine._detect_package(downstream)

    def test_multiple_src_subdirs_raises(self, downstream):
        (downstream / "src" / "pkg_a").mkdir(parents=True)
        (downstream / "src" / "pkg_b").mkdir(parents=True)
        with pytest.raises(adopt_doctrine.DetectionError, match="multiple"):
            adopt_doctrine._detect_package(downstream)

    def test_src_with_only_files_raises(self, downstream):
        (downstream / "src").mkdir()
        (downstream / "src" / "stray.py").write_text("")
        with pytest.raises(adopt_doctrine.DetectionError, match="no src/"):
            adopt_doctrine._detect_package(downstream)


# --- _plan_copies ---


class TestPlanCopies:
    def test_returns_expected_artifacts(self):
        upstream = Path("/fake/upstream")
        plan = adopt_doctrine._plan_copies(upstream)
        # Plan is a list of (src, dst, kind) tuples
        dsts = {dst for _src, dst, _kind in plan}
        # The six directory-form skills
        assert ".claude/skills/maintaining-ubiquitous-language" in dsts
        assert ".claude/skills/maintaining-project-context" in dsts
        assert ".claude/skills/recording-architecture-decisions" in dsts
        assert ".claude/skills/shift-left-testing" in dsts
        assert ".claude/skills/configuration-management" in dsts
        assert ".claude/skills/python-venv-management" in dsts
        # The four single-file artifacts
        assert ".claude/skills/SKILLS_FRAMEWORK.md" in dsts
        assert "docs/adr/ADR-FORMAT.md" in dsts
        assert "docs/session-doc-format.md" in dsts
        assert ".claude/commands/session-end.md" in dsts

    def test_kinds_are_dir_or_file(self):
        plan = adopt_doctrine._plan_copies(Path("/fake"))
        for _src, _dst, kind in plan:
            assert kind in {"dir", "file"}

    def test_sources_rooted_at_upstream(self):
        upstream = Path("/fake/upstream")
        plan = adopt_doctrine._plan_copies(upstream)
        for src, _dst, _kind in plan:
            # Use is_relative_to instead of string-prefix comparison so the
            # assertion works on Windows, where Path() normalizes to backslash
            # separators and str(src) starts with `\fake\upstream\…`.
            assert Path(src).is_relative_to(upstream)


# --- _apply_copies ---


@pytest.fixture
def upstream(tmp_path):
    """A fake upstream with a single skill dir + single file artifact."""
    root = tmp_path / "upstream"
    skill = root / ".claude" / "skills" / "shift-left-testing"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("upstream skill body")
    (skill / "PATTERNS.md").write_text("patterns body")
    framework = root / ".claude" / "skills" / "SKILLS_FRAMEWORK.md"
    framework.write_text("framework body")
    return root


class TestApplyCopies:
    def test_copies_directory_and_file(self, upstream, downstream):
        plan = [
            (upstream / ".claude/skills/shift-left-testing",
             ".claude/skills/shift-left-testing", "dir"),
            (upstream / ".claude/skills/SKILLS_FRAMEWORK.md",
             ".claude/skills/SKILLS_FRAMEWORK.md", "file"),
        ]
        result = adopt_doctrine._apply_copies(plan, downstream, dry_run=False)

        assert (downstream / ".claude/skills/shift-left-testing/SKILL.md").exists()
        assert (downstream / ".claude/skills/shift-left-testing/PATTERNS.md").exists()
        assert (downstream / ".claude/skills/SKILLS_FRAMEWORK.md").exists()
        assert "copied" in result[0]["status"]
        assert "copied" in result[1]["status"]

    def test_dry_run_writes_nothing(self, upstream, downstream, capsys):
        plan = [
            (upstream / ".claude/skills/SKILLS_FRAMEWORK.md",
             ".claude/skills/SKILLS_FRAMEWORK.md", "file"),
        ]
        adopt_doctrine._apply_copies(plan, downstream, dry_run=True)
        assert not (downstream / ".claude/skills/SKILLS_FRAMEWORK.md").exists()
        captured = capsys.readouterr()
        assert "[dry-run]" in captured.out

    def test_existing_target_skipped(self, upstream, downstream):
        target_dir = downstream / ".claude" / "skills" / "shift-left-testing"
        target_dir.mkdir(parents=True)
        (target_dir / "SKILL.md").write_text("user-customized")

        plan = [(upstream / ".claude/skills/shift-left-testing",
                 ".claude/skills/shift-left-testing", "dir")]
        result = adopt_doctrine._apply_copies(plan, downstream, dry_run=False)

        # User content preserved — helper never overwrites
        assert (target_dir / "SKILL.md").read_text() == "user-customized"
        assert "skipped" in result[0]["status"]

    def test_missing_source_records_error(self, downstream):
        plan = [(Path("/nonexistent"), ".claude/skills/missing", "dir")]
        result = adopt_doctrine._apply_copies(plan, downstream, dry_run=False)
        assert "missing" in result[0]["status"]


# --- _substitute_hook ---


HOOK_SAMPLE = """\
#!/bin/bash
# Logs evidence of test-partner presence for new production code in src/myproject/.
set -uo pipefail

case "$file_path" in
    */src/myproject/*.py) ;;
    *) exit 0 ;;
esac
"""


class TestSubstituteHook:
    def test_replaces_myproject_with_package_name(self, tmp_path, downstream):
        src = tmp_path / "post-tool-shift-left-audit.sh"
        src.write_text(HOOK_SAMPLE)

        result = adopt_doctrine._substitute_hook(
            src, downstream, package="rmireboot", dry_run=False
        )

        dst = downstream / ".claude" / "hooks" / "post-tool-shift-left-audit.sh"
        assert dst.exists()
        body = dst.read_text()
        assert "src/rmireboot/" in body
        assert "src/myproject/" not in body
        assert "copied" in result["status"]

    def test_preserves_bash_case_glob_syntax(self, tmp_path, downstream):
        src = tmp_path / "hook.sh"
        src.write_text(HOOK_SAMPLE)
        adopt_doctrine._substitute_hook(
            src, downstream, package="pkg", dry_run=False
        )
        dst = downstream / ".claude" / "hooks" / "post-tool-shift-left-audit.sh"
        body = dst.read_text()
        # Surrounding bash syntax must be intact
        assert "*/src/pkg/*.py) ;;" in body
        assert "esac" in body

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="NTFS has no POSIX +x bit; chmod(0o755) is a no-op on Windows. "
               "Hooks invoked via `bash <path>` from the harness don't need "
               "the bit anyway.",
    )
    def test_executable_bit_preserved(self, tmp_path, downstream):
        src = tmp_path / "hook.sh"
        src.write_text(HOOK_SAMPLE)
        src.chmod(0o755)
        adopt_doctrine._substitute_hook(
            src, downstream, package="pkg", dry_run=False
        )
        dst = downstream / ".claude" / "hooks" / "post-tool-shift-left-audit.sh"
        # Executable bit copied
        assert dst.stat().st_mode & 0o111

    def test_dry_run_writes_nothing(self, tmp_path, downstream, capsys):
        src = tmp_path / "hook.sh"
        src.write_text(HOOK_SAMPLE)
        adopt_doctrine._substitute_hook(
            src, downstream, package="pkg", dry_run=True
        )
        dst = downstream / ".claude" / "hooks" / "post-tool-shift-left-audit.sh"
        assert not dst.exists()
        assert "[dry-run]" in capsys.readouterr().out

    def test_existing_target_skipped(self, tmp_path, downstream):
        src = tmp_path / "hook.sh"
        src.write_text(HOOK_SAMPLE)
        dst = downstream / ".claude" / "hooks" / "post-tool-shift-left-audit.sh"
        dst.parent.mkdir(parents=True)
        dst.write_text("user-customized")

        result = adopt_doctrine._substitute_hook(
            src, downstream, package="pkg", dry_run=False
        )
        assert dst.read_text() == "user-customized"
        assert "skipped" in result["status"]


# --- _merge_settings ---


import json


class TestMergeSettings:
    def test_no_existing_settings_creates_minimal_file(self, downstream):
        result = adopt_doctrine._merge_settings(downstream, dry_run=False)

        settings_path = downstream / ".claude" / "settings.json"
        assert settings_path.exists()
        data = json.loads(settings_path.read_text())
        matchers = data["hooks"]["PostToolUse"]
        assert len(matchers) == 1
        assert matchers[0]["matcher"] == "Write|Edit"
        cmd = matchers[0]["hooks"][0]["command"]
        assert cmd.endswith("post-tool-shift-left-audit.sh")
        assert "added" in result["status"]

    def test_existing_settings_without_hooks_appends_block(self, downstream):
        settings_path = downstream / ".claude" / "settings.json"
        settings_path.parent.mkdir(parents=True)
        settings_path.write_text(json.dumps({
            "env": {"FOO": "1"},
            "permissions": {"allow": ["Read"]},
        }, indent=2))

        adopt_doctrine._merge_settings(downstream, dry_run=False)

        data = json.loads(settings_path.read_text())
        assert data["env"] == {"FOO": "1"}
        assert data["permissions"] == {"allow": ["Read"]}
        assert "hooks" in data
        assert data["hooks"]["PostToolUse"][0]["matcher"] == "Write|Edit"

    def test_existing_other_matcher_preserved_and_ours_appended(self, downstream):
        settings_path = downstream / ".claude" / "settings.json"
        settings_path.parent.mkdir(parents=True)
        settings_path.write_text(json.dumps({
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Bash",
                        "hooks": [{"type": "command", "command": "/other/hook.sh"}],
                    }
                ]
            }
        }, indent=2))

        adopt_doctrine._merge_settings(downstream, dry_run=False)

        data = json.loads(settings_path.read_text())
        matchers = data["hooks"]["PostToolUse"]
        assert len(matchers) == 2
        # Original preserved
        assert any(m["matcher"] == "Bash" for m in matchers)
        # Ours added
        assert any(
            m["matcher"] == "Write|Edit"
            and any(h["command"].endswith("post-tool-shift-left-audit.sh")
                    for h in m["hooks"])
            for m in matchers
        )

    def test_idempotent_when_our_matcher_already_present(self, downstream):
        # Run once to create
        adopt_doctrine._merge_settings(downstream, dry_run=False)
        settings_path = downstream / ".claude" / "settings.json"
        first = settings_path.read_text()

        # Run again — should detect and skip
        result = adopt_doctrine._merge_settings(downstream, dry_run=False)
        second = settings_path.read_text()

        assert first == second
        assert "skipped" in result["status"] or "present" in result["status"]

    def test_dry_run_writes_nothing(self, downstream, capsys):
        adopt_doctrine._merge_settings(downstream, dry_run=True)
        assert not (downstream / ".claude" / "settings.json").exists()
        assert "[dry-run]" in capsys.readouterr().out


# --- _append_gitignore ---


class TestAppendGitignore:
    def test_no_existing_gitignore_creates_with_lines(self, downstream):
        result = adopt_doctrine._append_gitignore(downstream, dry_run=False)
        gi = (downstream / ".gitignore").read_text()
        assert ".claude/audits/" in gi
        assert "docs/design/hold/" in gi
        assert "added" in result["status"]

    def test_existing_gitignore_appends_missing_lines(self, downstream):
        (downstream / ".gitignore").write_text("__pycache__/\n.venv/\n")
        adopt_doctrine._append_gitignore(downstream, dry_run=False)
        gi = (downstream / ".gitignore").read_text()
        assert "__pycache__/" in gi
        assert ".venv/" in gi
        assert ".claude/audits/" in gi
        assert "docs/design/hold/" in gi

    def test_existing_lines_not_duplicated(self, downstream):
        (downstream / ".gitignore").write_text(
            "__pycache__/\n.claude/audits/\n.venv/\n"
        )
        result = adopt_doctrine._append_gitignore(downstream, dry_run=False)
        gi = (downstream / ".gitignore").read_text()
        # .claude/audits/ should appear only once
        assert gi.count(".claude/audits/") == 1
        # docs/design/hold/ added (was missing)
        assert "docs/design/hold/" in gi
        # No duplicate-add status confusion
        assert "added" in result["status"] or "partial" in result["status"]

    def test_all_lines_already_present_skips(self, downstream):
        (downstream / ".gitignore").write_text(
            ".claude/audits/\ndocs/design/hold/\n"
        )
        result = adopt_doctrine._append_gitignore(downstream, dry_run=False)
        assert "skipped" in result["status"] or "present" in result["status"]

    def test_dry_run_writes_nothing(self, downstream, capsys):
        adopt_doctrine._append_gitignore(downstream, dry_run=True)
        assert not (downstream / ".gitignore").exists()
        assert "[dry-run]" in capsys.readouterr().out


# --- _print_manual_checklist ---


class TestPrintManualChecklist:
    def test_lists_customize_artifacts_with_doctrine_refs(self, capsys):
        adopt_doctrine._print_manual_checklist()
        out = capsys.readouterr().out
        # Must mention each CUSTOMIZE/CONDITIONAL/SKIP item by name
        assert "LANGUAGE.md" in out
        assert "CONTEXT.md" in out
        assert "ADR-0001" in out or "0001-directory-form" in out
        assert "python-prototyper" in out
        assert "CLAUDE.md" in out
        assert "Python 3.11" in out or "pyproject.toml" in out
        assert "propagation-protocol" in out
        assert "settings.local.json" in out
        # Mentions legacy single-file skill deletions
        assert "shift-left-testing.md" in out or "legacy single-file" in out
        # Points readers back to the doctrine entry
        assert "docs/doctrine-updates.md" in out


# --- adopt() orchestrator ---


@pytest.fixture
def full_upstream(tmp_path):
    """A full fake upstream with all 10 verbatim copy targets + the hook."""
    root = tmp_path / "upstream"
    # All ten verbatim COPY artifacts
    for rel, kind in adopt_doctrine.VERBATIM_COPIES:
        target = root / rel
        if kind == "dir":
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text(f"contents of {rel}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"contents of {rel}")
    # Hook
    hook = root / adopt_doctrine.HOOK_RELATIVE
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text("# hook for src/myproject/\ncase $f in */src/myproject/*.py) ;; esac\n")
    return root


@pytest.fixture
def real_downstream(tmp_path):
    """Downstream with src/<pkg>/ so detection works."""
    root = tmp_path / "real_downstream"
    (root / "src" / "rmireboot").mkdir(parents=True)
    return root


class TestAdopt:
    def test_dry_run_writes_nothing_and_prints_checklist(
        self, full_upstream, real_downstream, capsys
    ):
        adopt_doctrine.adopt(
            upstream=full_upstream,
            downstream=real_downstream,
            package="rmireboot",
            dry_run=True,
            yes=False,  # confirmation skipped in dry-run by design
        )
        # Nothing written
        assert not (real_downstream / ".claude" / "settings.json").exists()
        assert not (real_downstream / ".gitignore").exists()
        # Checklist printed
        out = capsys.readouterr().out
        assert "[dry-run]" in out
        assert "MANUAL ATTENTION REQUIRED" in out

    def test_yes_flag_skips_prompt_and_applies(self, full_upstream, real_downstream):
        adopt_doctrine.adopt(
            upstream=full_upstream,
            downstream=real_downstream,
            package="rmireboot",
            dry_run=False,
            yes=True,
        )
        # Side effects landed
        assert (real_downstream / ".claude" / "settings.json").exists()
        assert (real_downstream / ".gitignore").exists()
        assert (real_downstream / adopt_doctrine.HOOK_RELATIVE).exists()
        # Hook substitution worked
        hook_body = (real_downstream / adopt_doctrine.HOOK_RELATIVE).read_text()
        assert "src/rmireboot/" in hook_body
        assert "src/myproject/" not in hook_body

    def test_prompt_declined_writes_nothing(
        self, full_upstream, real_downstream, monkeypatch
    ):
        monkeypatch.setattr("builtins.input", lambda _prompt: "n")
        adopt_doctrine.adopt(
            upstream=full_upstream,
            downstream=real_downstream,
            package="rmireboot",
            dry_run=False,
            yes=False,
        )
        # User declined; no changes
        assert not (real_downstream / ".claude" / "settings.json").exists()
        assert not (real_downstream / ".gitignore").exists()
        assert not (real_downstream / adopt_doctrine.HOOK_RELATIVE).exists()

    def test_prompt_accepted_applies(
        self, full_upstream, real_downstream, monkeypatch
    ):
        monkeypatch.setattr("builtins.input", lambda _prompt: "y")
        adopt_doctrine.adopt(
            upstream=full_upstream,
            downstream=real_downstream,
            package="rmireboot",
            dry_run=False,
            yes=False,
        )
        assert (real_downstream / ".claude" / "settings.json").exists()


# --- CLI entry (main) ---


class TestMain:
    def test_resolves_args_and_invokes_adopt(
        self, full_upstream, real_downstream, monkeypatch
    ):
        called = {}

        def fake_adopt(**kwargs):
            called.update(kwargs)

        monkeypatch.setattr(adopt_doctrine, "adopt", fake_adopt)
        monkeypatch.chdir(real_downstream)
        adopt_doctrine.main([
            "--upstream", str(full_upstream),
            "--dry-run",
            "--yes",
        ])
        assert called["package"] == "rmireboot"
        assert called["upstream"] == full_upstream
        assert called["downstream"] == real_downstream
        assert called["dry_run"] is True
        assert called["yes"] is True

    def test_missing_upstream_errors(self, real_downstream, monkeypatch, capsys):
        monkeypatch.chdir(real_downstream)
        with pytest.raises(SystemExit) as exc_info:
            adopt_doctrine.main([
                "--upstream", "/nonexistent/path",
                "--dry-run",
            ])
        assert exc_info.value.code != 0
        err = capsys.readouterr().err
        assert "upstream" in err.lower() or "not found" in err.lower()

    def test_undetectable_package_errors(self, full_upstream, tmp_path, monkeypatch, capsys):
        bad_downstream = tmp_path / "bad"
        bad_downstream.mkdir()
        monkeypatch.chdir(bad_downstream)
        with pytest.raises(SystemExit) as exc_info:
            adopt_doctrine.main([
                "--upstream", str(full_upstream),
                "--dry-run",
            ])
        assert exc_info.value.code != 0
        err = capsys.readouterr().err
        assert "package" in err.lower() or "src" in err.lower()

    def test_explicit_package_overrides_detection(
        self, full_upstream, real_downstream, monkeypatch
    ):
        called = {}

        def fake_adopt(**kwargs):
            called.update(kwargs)

        monkeypatch.setattr(adopt_doctrine, "adopt", fake_adopt)
        monkeypatch.chdir(real_downstream)
        adopt_doctrine.main([
            "--upstream", str(full_upstream),
            "--package", "explicit_pkg",
            "--dry-run",
            "--yes",
        ])
        assert called["package"] == "explicit_pkg"
