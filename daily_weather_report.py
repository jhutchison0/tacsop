# -*- coding: utf-8 -*-
"""
daily_weather_report.py

Core object for representing a single day's weather report.

This module is the foundation for a Raspberry‑Pi‑hosted weather‑dashboard project.
It now includes *robust* error‑handling so that:
    • Any failure to reach / parse a live API is caught and surfaced as a custom
      `WeatherAPIError`.
    • Demo / fallback data are clearly labeled via the `source` attribute so that
      later pipeline steps (e.g., database writes or UI renders) know whether the
      record is real or synthetic.

Author: John Hutchison (generated with ChatGPT assistance)
Updated: 2025‑04‑28
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional
import json
import logging

try:
    import requests  # Only needed when calling a live API
except ImportError:  # Keeps the object usable even when requests isn’t installed yet
    requests = None  # type: ignore

# %% Packages
""" Third party and local imports """
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional
import json
import logging

try:
    import requests  # Only needed when calling a live API
except ImportError:  # Keeps the object usable even when requests isn’t installed yet
    requests = None  # type: ignore


# %% Functions
""" Define functions """


###############################################################################
# Logging configuration
###############################################################################
logger = logging.getlogger("daily_weather_report")
if not logger.handlers:  # Avoid duplicate handlers in notebooks / reloads
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


###############################################################################
# Exceptions
###############################################################################
class WeatherAPIError(RuntimeError):
    """Raised when we cannot obtain or parse weather‑API data."""


###############################################################################
# Data Object
###############################################################################
@dataclass(slots=True)
class DailyWeatherReport:
    report_date: date
    high_temp_c: float
    low_temp_c: float
    precip_mm: float
    wind_kph: float
    summary: str
    source: str  # e.g. "wunderground", "demo"

    # ---------------------------------------------------------------------
    # Derived convenience properties
    # ---------------------------------------------------------------------
    @property
    def high_temp_f(self) -> float:
        return self.high_temp_c * 9 / 5 + 32

    @property
    def low_temp_f(self) -> float:
        return self.low_temp_c * 9 / 5 + 32

    @property
    def precip_in(self) -> float:
        return self.precip_mm / 25.4

    @property
    def wind_mph(self) -> float:
        return self.wind_kph / 1.60934

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------
    def to_json(self, indent: Optional[int] = 2) -> str:
        """Return a JSON string."""
        return json.dumps(asdict(self), default=str, indent=indent)

    def to_markdown(self) -> str:
        """Return a quick Markdown snippet suitable for a static site."""
        return (
            f"### Weather for {self.report_date:%Y‑%m‑%d}\n\n"
            f"*High*: {self.high_temp_c:.1f} °C / {self.high_temp_f:.1f} °F  \n"
            f"*Low*: {self.low_temp_c:.1f} °C / {self.low_temp_f:.1f} °F  \n"
            f"*Precip*: {self.precip_mm:.1f} mm / {self.precip_in:.2f} in  \n"
            f"*Wind*: {self.wind_kph:.1f} kph / {self.wind_mph:.1f} mph  \n"
            f"*Summary*: {self.summary}  \n"
            f"*Source*: `{self.source}`"
        )

    def save(self, path: Path | str, fmt: str = "json", **kwargs: Any) -> Path:
        """Write the report to *path* in *fmt* (json or md). Returns the Path."""
        path = Path(path)
        if fmt == "json":
            path.write_text(self.to_json(**kwargs))
        elif fmt in {"md", "markdown"}:
            path.write_text(self.to_markdown())
        else:
            raise ValueError(f"Unsupported format: {fmt}")
        logger.info("Saved %s weather report to %s", self.report_date, path)
        return path

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    @classmethod
    def from_api(
        cls,
        lat: float,
        lon: float,
        api_key: str,
        api_date: date | None = None,
        session: Optional["requests.Session"] = None,
    ) -> "DailyWeatherReport":
        """Fetch daily weather from Weather Underground and return an object.

        *All* network and parsing errors bubble up as :class:`WeatherAPIError` to
        encourage callers to handle failure explicitly (e.g., fallback to demo
        data or cached results).
        """
        if requests is None:
            raise WeatherAPIError("'requests' not installed. Cannot call API.")

        api_date = api_date or date.today()
        url = (
            "https://api.weather.com/v3/wx/forecast/daily/5day?"  # sample endpoint
            f"geocode={lat},{lon}&format=json&units=m&language=en‑US&apiKey={api_key}"
        )

        logger.info(
            "Fetching Weather Underground data for %s (%s, %s)", api_date, lat, lon
        )
        try:
            sess = session or requests.Session()
            resp = sess.get(url, timeout=10)
            resp.raise_for_status()
            data: Dict[str, Any] = resp.json()
            # === NB: Adjust keys below to actual API schema ===
            idx = 0  # We asked for 5‑day; day0 is today
            report = cls(
                report_date=api_date,
                high_temp_c=float(data["temperatureMax"][idx]),
                low_temp_c=float(data["temperatureMin"][idx]),
                precip_mm=float(data.get("precipitationProbability", [0])[idx] or 0),
                wind_kph=float(data.get("windSpeed", [0])[idx] or 0),
                summary=str(data.get("narrative", [""])[idx]),
                source="wunderground",
            )
            logger.info("Fetched weather for %s: %s", api_date, report.summary)
            return report
        except Exception as exc:
            logger.exception("Weather API failure: %s", exc)
            raise WeatherAPIError("Unable to fetch weather data") from exc

    @classmethod
    def demo(cls, for_date: date | None = None) -> "DailyWeatherReport":
        """Return a deterministic demo object for offline tests."""
        for_date = for_date or date.today()
        logger.warning("Using *demo* weather data for %s", for_date)
        return cls(
            report_date=for_date,
            high_temp_c=21.5,
            low_temp_c=13.2,
            precip_mm=5.6,
            wind_kph=12.8,
            summary="Partly cloudy with a light breeze.",
            source="demo",
        )


# %% Variables
""" Set script (global) variables """

path_data = Path("data/")


# %% Main
""" Display task data """

###############################################################################
# Quick‑n‑dirty CLI demo
###############################################################################
if __name__ == "__main__":
    # Replace with real API coordinates / key or fall back to demo.
    try:
        rpt = DailyWeatherReport.from_api(
            lat=41.8781,  # Chicago
            lon=-87.6298,
            api_key="YOUR‑API‑KEY",  # <-- replace!
        )
    except WeatherAPIError:
        rpt = DailyWeatherReport.demo()

    print(rpt.to_markdown())


# %%


"""
daily_weather_report.py

Foundation classes for our Raspberry‑Pi‑hosted weather dashboard.

Two layers now:

* **`DailyWeatherReport`** – encapsulates a single day (same as before).
* **`WeeklyWeatherForecast`** – wraps the 7‑day grid forecast from the National
  Weather Service (NWS), provides helper queries like `today()`, `tonight()`,
  `tomorrow()`, and `will_rain()`.

NWS remains free/no‑key; we just pass a User‑Agent.

Author: John Hutchison (generated with ChatGPT assistance)
Updated: 2025‑04‑28
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
import json
import logging
import re

try:
    import requests  # Needed for live API calls
except ImportError:
    requests = None  # type: ignore

###############################################################################
# Logging
###############################################################################
LOGGER = logging.getLogger("daily_weather_report")
if not LOGGER.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    LOGGER.addHandler(_h)
    LOGGER.setLevel(logging.INFO)


###############################################################################
# Exceptions
###############################################################################
class WeatherAPIError(RuntimeError):
    """Raised when we cannot obtain or parse weather‑API data."""


###############################################################################
# Helpers
###############################################################################
DEFAULT_USER_AGENT = "daily‑weather‑app/0.2 (john.hutchison@example.com)"

_TEMP_RE = re.compile(r"(-?\d+(?:\.\d+)?)")
_WIND_RE = re.compile(r"(\d+(?:\.\d+)?)")


###############################################################################
# Core daily object (unchanged except for minor doc tweaks)
###############################################################################
@dataclass(slots=True)
class DailyWeatherReport:
    """Lightweight representation of a single day's weather‑forecast snippet."""

    report_date: date
    high_temp_c: float
    low_temp_c: float
    precip_mm: float
    wind_kph: float
    summary: str
    source: str  # "nws" or "demo"

    # Unit helpers -----------------------------------------------------
    @property
    def high_temp_f(self) -> float:
        return self.high_temp_c * 9 / 5 + 32

    @property
    def low_temp_f(self) -> float:
        return self.low_temp_c * 9 / 5 + 32

    @property
    def precip_in(self) -> float:
        return self.precip_mm / 25.4

    @property
    def wind_mph(self) -> float:
        return self.wind_kph / 1.60934

    # Serialisation ----------------------------------------------------
    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(asdict(self), default=str, indent=kwargs.get("indent", 2))

    def to_markdown(self) -> str:
        return (
            f"### Weather for {self.report_date:%Y‑%m‑%d}\n\n"
            f"*High*: {self.high_temp_c:.1f} °C / {self.high_temp_f:.1f} °F  \n"
            f"*Low*: {self.low_temp_c:.1f} °C / {self.low_temp_f:.1f} °F  \n"
            f"*Precip*: {self.precip_mm:.1f} mm / {self.precip_in:.2f} in  \n"
            f"*Wind*: {self.wind_kph:.1f} kph / {self.wind_mph:.1f} mph  \n"
            f"*Summary*: {self.summary}  \n"
            f"*Source*: `{self.source}`"
        )

    def save(self, path: Path | str, fmt: str = "json", **kwargs: Any) -> Path:
        path = Path(path)
        txt = self.to_json(**kwargs) if fmt == "json" else self.to_markdown()
        path.write_text(txt)
        LOGGER.info("Saved %s weather report to %s", self.report_date, path)
        return path

    # Construction ------------------------------------------------------
    @classmethod
    def demo(cls, for_date: date | None = None) -> "DailyWeatherReport":
        for_date = for_date or date.today()
        return cls(
            report_date=for_date,
            high_temp_c=22.0,
            low_temp_c=14.0,
            precip_mm=3.0,
            wind_kph=10.0,
            summary="Sunny intervals with light winds.",
            source="demo",
        )


###############################################################################
# Weekly forecast object
###############################################################################
@dataclass(slots=True)
class WeeklyWeatherForecast:
    """Seven‑day forecast wrapper fetched from NWS /forecast endpoint."""

    periods: List[Dict[str, Any]]
    generated_at: datetime
    lat: float
    lon: float
    source: str = "nws"

    # --- Construction -------------------------------------------------
    @classmethod
    def from_nws(
        cls,
        lat: float,
        lon: float,
        *,
        session: Optional["requests.Session"] = None,
        user_agent: str | None = None,
    ) -> "WeeklyWeatherForecast":
        if requests is None:
            raise WeatherAPIError("'requests' not available – install requests module")

        headers = {
            "User-Agent": user_agent or DEFAULT_USER_AGENT,
            "Accept": "application/ld+json",
        }
        sess = session or requests.Session()

        # 1) Resolve /points for grid endpoint
        points_url = f"https://api.weather.gov/points/{lat:.4f},{lon:.4f}"
        try:
            LOGGER.info("GET %s", points_url)
            j = sess.get(points_url, headers=headers, timeout=8).json()
            fc_url = j["properties"]["forecast"]
        except Exception as exc:
            LOGGER.exception("Failed resolving NWS grid: %s", exc)
            raise WeatherAPIError("NWS /points lookup failed") from exc

        # 2) Fetch forecast periods list
        try:
            LOGGER.info("GET %s", fc_url)
            periods = sess.get(fc_url, headers=headers, timeout=8).json()["properties"][
                "periods"
            ]
        except Exception as exc:
            LOGGER.exception("Failed fetching forecast: %s", exc)
            raise WeatherAPIError("NWS forecast fetch failed") from exc

        if len(periods) < 1:
            raise WeatherAPIError("No forecast data returned")

        return cls(periods=periods, generated_at=datetime.utcnow(), lat=lat, lon=lon)

    # --- Convenience helpers ------------------------------------------
    def _find_period(self, predicate) -> Optional[Dict[str, Any]]:
        return next((p for p in self.periods if predicate(p)), None)

    def today(self) -> DailyWeatherReport:
        today = date.today()
        day_period = (
            self._find_period(
                lambda p: p["startTime"].startswith(str(today)) and p["isDaytime"]
            )
            or self.periods[0]
        )
        return self._period_to_daily(day_period)

    def tonight(self) -> DailyWeatherReport:
        today = date.today()
        night_period = (
            self._find_period(
                lambda p: p["startTime"].startswith(str(today)) and not p["isDaytime"]
            )
            or self.periods[1]
        )
        return self._period_to_daily(night_period)

    def tomorrow(self) -> DailyWeatherReport:
        tomorrow = date.today() + timedelta(days=1)
        day_period = (
            self._find_period(
                lambda p: p["startTime"].startswith(str(tomorrow)) and p["isDaytime"]
            )
            or self.periods[2]
        )
        return self._period_to_daily(day_period)

    def will_rain(self, threshold: int = 30) -> bool:
        """Return True if any period's probabilityOfPrecipitation ≥ *threshold*%."""
        for p in self.periods:
            pop = p.get("probabilityOfPrecipitation", {}).get("value") or 0
            if pop >= threshold:
                return True
        return False

    # --- Internal conversion -----------------------------------------
    def _period_to_daily(self, period: Dict[str, Any]) -> DailyWeatherReport:
        temp_f = float(period["temperature"])
        temp_c = (temp_f - 32) * 5 / 9
        # naive low estimation – assume ±8 °C swing
        low_c = temp_c - 8
        pop = period.get("probabilityOfPrecipitation", {}).get("value") or 0
        precip_mm = (pop / 100) * 0.5
        wind_match = _WIND_RE.search(period.get("windSpeed", "0 mph"))
        wind_mph = float(wind_match.group(1)) if wind_match else 0.0
        wind_kph = wind_mph * 1.60934

        return DailyWeatherReport(
            report_date=date.fromisoformat(period["startTime"][:10]),
            high_temp_c=round(temp_c, 1),
            low_temp_c=round(low_c, 1),
            precip_mm=round(precip_mm, 1),
            wind_kph=round(wind_kph, 1),
            summary=period.get("shortForecast", ""),
            source=self.source,
        )


###############################################################################
# CLI demo – prints today's and tomorrow's plus rain check
###############################################################################
if __name__ == "__main__":
    lat, lon = 41.8781, -87.6298  # Chicago
    try:
        weekly = WeeklyWeatherForecast.from_nws(lat, lon)
        print("# Chicago Forecast (NWS)\n")
        print(weekly.today().to_markdown())
        print("\n---\n")
        print("## Tonight\n")
        print(weekly.tonight().to_markdown())
        print("\n---\n")
        print("## Tomorrow\n")
        print(weekly.tomorrow().to_markdown())
        print("\n---\n")
        rain = "Yes" if weekly.will_rain() else "No"
        print(f"**Will it rain this week?** {rain}")
    except WeatherAPIError as e:
        LOGGER.error("Falling back to demo data: %s", e)
        today_demo = DailyWeatherReport.demo()
        print(today_demo.to_markdown())
