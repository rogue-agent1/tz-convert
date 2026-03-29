#!/usr/bin/env python3
"""Timezone converter."""
from datetime import datetime, timedelta, timezone

TZ_OFFSETS = {
    "UTC": 0, "GMT": 0, "EST": -5, "EDT": -4, "CST": -6, "CDT": -5,
    "MST": -7, "MDT": -6, "PST": -8, "PDT": -7, "CET": 1, "CEST": 2,
    "EET": 2, "EEST": 3, "IST": 5.5, "JST": 9, "KST": 9, "CST_CN": 8,
    "AEST": 10, "AEDT": 11, "NZST": 12, "NZDT": 13,
}

def get_tz(name):
    name = name.upper()
    if name in TZ_OFFSETS:
        hours = TZ_OFFSETS[name]
        return timezone(timedelta(hours=hours))
    if name.startswith("UTC") or name.startswith("GMT"):
        offset_str = name[3:]
        if offset_str:
            hours = float(offset_str.replace("+", ""))
            return timezone(timedelta(hours=hours))
    return timezone.utc

def convert(dt_str, from_tz, to_tz, fmt="%Y-%m-%d %H:%M"):
    src = get_tz(from_tz)
    dst = get_tz(to_tz)
    dt = datetime.strptime(dt_str, fmt).replace(tzinfo=src)
    return dt.astimezone(dst).strftime(fmt)

def now_in(tz_name):
    tz = get_tz(tz_name)
    return datetime.now(tz)

def time_diff(tz1, tz2):
    o1 = TZ_OFFSETS.get(tz1.upper(), 0)
    o2 = TZ_OFFSETS.get(tz2.upper(), 0)
    return o2 - o1

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 4:
        print(convert(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        for tz in ["PST", "EST", "UTC", "CET", "JST"]:
            print(f"{tz}: {now_in(tz).strftime('%H:%M')}")

def test():
    r = convert("2026-03-29 12:00", "PST", "EST")
    assert r == "2026-03-29 15:00"
    r2 = convert("2026-03-29 00:00", "UTC", "JST")
    assert r2 == "2026-03-29 09:00"
    r3 = convert("2026-03-29 12:00", "EST", "UTC")
    assert r3 == "2026-03-29 17:00"
    assert time_diff("PST", "EST") == 3
    assert time_diff("UTC", "JST") == 9
    n = now_in("UTC")
    assert n.tzinfo is not None
    print("  tz_convert: ALL TESTS PASSED")
