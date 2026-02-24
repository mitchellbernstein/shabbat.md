#!/usr/bin/env python3
"""
Shabbat check — pure Python, no API. Computes shkia/tzait from SHABBAT.md.
Uses NOAA formula (Meeus). Stdlib only. Supports all IANA timezones.
"""
from __future__ import annotations

import math
import re
import sys
from datetime import datetime, time, timedelta
from pathlib import Path

# Timezone → (lat, lon) for approximate zmanim. Uses representative city.
# Unknown timezones: coordinates derived from UTC offset (works for any IANA zone).
TZ_COORDS: dict[str, tuple[float, float]] = {
    "America/New_York": (40.71, -74.01),
    "America/Chicago": (41.88, -87.63),
    "America/Denver": (39.74, -104.99),
    "America/Los_Angeles": (34.05, -118.24),
    "America/Phoenix": (33.45, -112.07),
    "America/Detroit": (42.33, -83.05),
    "America/Toronto": (43.65, -79.38),
    "America/Vancouver": (49.28, -123.12),
    "America/Mexico_City": (19.43, -99.13),
    "America/Sao_Paulo": (-23.55, -46.63),
    "Europe/London": (51.51, -0.13),
    "Europe/Paris": (48.86, 2.35),
    "Europe/Berlin": (52.52, 13.41),
    "Europe/Amsterdam": (52.37, 4.89),
    "Europe/Jerusalem": (31.78, 35.22),
    "Asia/Jerusalem": (31.78, 35.22),
    "Asia/Tel_Aviv": (32.09, 34.78),
    "Australia/Sydney": (-33.87, 151.21),
    "Australia/Melbourne": (-37.81, 144.96),
    "Pacific/Auckland": (-36.85, 174.76),
    "UTC": (51.51, 0.0),
}


def _parse_shabbat_md(path: Path) -> dict[str, str]:
    """Parse SHABBAT.md for timezone, pause_trigger, resume_trigger, life_safety_override."""
    out: dict[str, str] = {}
    content = path.read_text()
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("- timezone:"):
            out["timezone"] = line.split(":", 1)[1].strip()
        elif line.startswith("- pause_trigger:"):
            out["pause_trigger"] = line.split(":", 1)[1].strip()
        elif line.startswith("- resume_trigger:"):
            out["resume_trigger"] = line.split(":", 1)[1].strip()
        elif line.startswith("- life_safety_override:"):
            out["life_safety_override"] = re.search(r"true|false", line, re.I)[0].lower()
        elif line.startswith("- latitude:") or line.startswith("- lat:"):
            out["latitude"] = line.split(":", 1)[1].strip()
        elif line.startswith("- longitude:") or line.startswith("- lon:"):
            out["longitude"] = line.split(":", 1)[1].strip()
    return out


def _sun_times(lat: float, lon: float, when: datetime, zenith_sunset: float = 90.833, zenith_tzait: float = 96.0) -> tuple[time, time]:
    """
    NOAA-style sun position. Returns (sunset_time, tzait_time) in local time.
    zenith_sunset: 90.833 for shkia (refraction + solar disk)
    zenith_tzait: 96 for 6° below horizon (nightfall)
    """
    day = when.toordinal() - (734124 - 40529)
    t = when.time()
    time_frac = (t.hour + t.minute / 60.0 + t.second / 3600.0) / 24.0
    tz_offset = when.utcoffset()
    tz_hours = tz_offset.total_seconds() / 3600.0 if tz_offset else 0

    Jday = day + 2415018.5 + time_frac - tz_hours / 24
    Jcent = (Jday - 2451545) / 36525

    Manom = 357.52911 + Jcent * (35999.05029 - 0.0001537 * Jcent)
    Mlong = (280.46646 + Jcent * (36000.76983 + Jcent * 0.0003032)) % 360
    Eccent = 0.016708634 - Jcent * (0.000042037 + 0.0001537 * Jcent)
    Mobliq = 23 + (26 + ((21.448 - Jcent * (46.815 + Jcent * (0.00059 - Jcent * 0.001813)))) / 60) / 60
    obliq = Mobliq + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * Jcent))
    vary = math.tan(math.radians(obliq / 2)) ** 2
    Seqcent = (
        math.sin(math.radians(Manom)) * (1.914602 - Jcent * (0.004817 + 0.000014 * Jcent))
        + math.sin(math.radians(2 * Manom)) * (0.019993 - 0.000101 * Jcent)
        + math.sin(math.radians(3 * Manom)) * 0.000289
    )
    Struelong = Mlong + Seqcent
    Sapplong = Struelong - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * Jcent))
    declination = math.degrees(math.asin(math.sin(math.radians(obliq)) * math.sin(math.radians(Sapplong))))

    eqtime = 4 * math.degrees(
        vary * math.sin(2 * math.radians(Mlong))
        - 2 * Eccent * math.sin(math.radians(Manom))
        + 4 * Eccent * vary * math.sin(math.radians(Manom)) * math.cos(2 * math.radians(Mlong))
        - 0.5 * vary * vary * math.sin(4 * math.radians(Mlong))
        - 1.25 * Eccent * Eccent * math.sin(2 * math.radians(Manom))
    )

    def hour_angle(zenith: float) -> float:
        cos_ha = (
            math.cos(math.radians(zenith))
            - math.sin(math.radians(lat)) * math.sin(math.radians(declination))
        ) / (math.cos(math.radians(lat)) * math.cos(math.radians(declination)))
        cos_ha = max(-1, min(1, cos_ha))
        return math.degrees(math.acos(cos_ha))

    ha_sunset = hour_angle(zenith_sunset)
    ha_tzait = hour_angle(zenith_tzait)

    solarnoon_frac = (720 - 4 * lon - eqtime + tz_hours * 60) / 1440
    sunset_frac = solarnoon_frac + ha_sunset * 4 / 1440
    tzait_frac = solarnoon_frac + ha_tzait * 4 / 1440

    def frac_to_time(frac: float) -> time:
        frac = frac % 1.0
        if frac < 0:
            frac += 1
        hours = 24.0 * frac
        h = int(hours)
        m = int((hours - h) * 60)
        s = int(((hours - h) * 60 - m) * 60)
        return time(hour=h, minute=m, second=s)

    return frac_to_time(sunset_frac), frac_to_time(tzait_frac)


def main() -> int:
    repo = Path.cwd()
    shabbat_md = repo / "SHABBAT.md"
    if not shabbat_md.exists():
        for parent in repo.parents:
            if (parent / "SHABBAT.md").exists():
                shabbat_md = parent / "SHABBAT.md"
                break
        else:
            print("SHABBAT.md not found", file=sys.stderr)
            return 1

    cfg = _parse_shabbat_md(shabbat_md)
    tz_name = cfg.get("timezone", "America/New_York")
    pause = cfg.get("pause_trigger", "shkia")
    resume = cfg.get("resume_trigger", "tzait")
    life_safety = cfg.get("life_safety_override", "false").lower() == "true"

    if life_safety:
        print("life_safety_override=true")
        print("is_shabbat=0")
        return 0

    lat = lon = None
    if "latitude" in cfg and "longitude" in cfg:
        try:
            lat = float(cfg["latitude"])
            lon = float(cfg["longitude"])
        except ValueError:
            pass
    if lat is None or lon is None:
        coords = TZ_COORDS.get(tz_name)
        if coords is not None:
            lat, lon = coords
        else:
            # Fallback: derive from UTC offset. Works for any IANA timezone.
            try:
                from zoneinfo import ZoneInfo
            except ImportError:
                print("zoneinfo not available (Python < 3.9)", file=sys.stderr)
                return 1
            try:
                tz = ZoneInfo(tz_name)
                now_temp = datetime.now(tz)
                offset = now_temp.utcoffset()
                offset_hours = offset.total_seconds() / 3600.0 if offset else 0
                lon = offset_hours * 15.0  # 15° per hour (UTC+3 → 45°E)
                lat = 30.0  # default mid-latitude; add latitude/longitude to SHABBAT.md for accuracy
            except Exception:
                lat, lon = 40.71, -74.01  # America/New_York fallback

    try:
        from zoneinfo import ZoneInfo
    except ImportError:
        print("zoneinfo not available (Python < 3.9)", file=sys.stderr)
        return 1

    try:
        now = datetime.now(ZoneInfo(tz_name))
    except Exception:
        print(f"Invalid timezone: {tz_name}", file=sys.stderr)
        return 1
    sunset_t, tzait_t = _sun_times(lat, lon, now)

    sunset_dt = now.replace(hour=sunset_t.hour, minute=sunset_t.minute, second=sunset_t.second, microsecond=0)
    tzait_dt = now.replace(hour=tzait_t.hour, minute=tzait_t.minute, second=tzait_t.second, microsecond=0)
    candle_dt = sunset_dt - timedelta(minutes=18)

    if pause == "candle-lighting":
        pause_dt = candle_dt
    else:
        pause_dt = sunset_dt
    if resume == "havdalah" or resume == "tzait":
        resume_dt = tzait_dt
    else:
        resume_dt = tzait_dt

    is_friday = now.weekday() == 4
    is_saturday = now.weekday() == 5

    is_shabbat = False
    if is_friday and now >= pause_dt:
        is_shabbat = True
    elif is_saturday and now < resume_dt:
        is_shabbat = True

    print(f"pause_at={pause_dt.strftime('%H:%M')}")
    print(f"resume_at={resume_dt.strftime('%H:%M')}")
    print(f"is_shabbat={'1' if is_shabbat else '0'}")
    return 0 if not is_shabbat else 2


if __name__ == "__main__":
    sys.exit(main())
