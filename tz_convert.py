#!/usr/bin/env python3
"""tz_convert - Convert times between timezones."""
import sys
from datetime import datetime, timezone, timedelta

ZONES = {
    'UTC':0,'GMT':0,'EST':-5,'EDT':-4,'CST':-6,'CDT':-5,'MST':-7,'MDT':-6,
    'PST':-8,'PDT':-7,'CET':1,'CEST':2,'IST':5.5,'JST':9,'KST':9,'CST_CN':8,
    'AEST':10,'AEDT':11,'NZST':12,'NZDT':13,'HST':-10,'AKST':-9,'BRT':-3,
    'GST':4,'PKT':5,'ICT':7,'WIB':7,'SGT':8,'HKT':8,'PHT':8,
}

def tz(offset_hours):
    return timezone(timedelta(hours=offset_hours))

def now_all():
    now = datetime.now(timezone.utc)
    for name, off in sorted(ZONES.items(), key=lambda x: x[1]):
        t = now.astimezone(tz(off))
        print(f"  {name:>6} (UTC{off:+.1f}): {t.strftime('%Y-%m-%d %H:%M')}")

def convert(time_str, from_tz, to_tz):
    from_off = ZONES.get(from_tz.upper())
    to_off = ZONES.get(to_tz.upper())
    if from_off is None or to_off is None:
        print(f"Unknown timezone. Available: {', '.join(sorted(ZONES))}"); return
    for fmt in ('%H:%M','%I:%M%p','%Y-%m-%d %H:%M'):
        try:
            dt = datetime.strptime(time_str, fmt).replace(tzinfo=tz(from_off))
            result = dt.astimezone(tz(to_off))
            print(f"  {time_str} {from_tz} = {result.strftime('%H:%M')} {to_tz} ({result.strftime('%Y-%m-%d')})")
            return
        except: pass
    print(f"Can't parse: {time_str}")

def main():
    args = sys.argv[1:]
    if not args or '-h' in args:
        print("Usage:\n  tz_convert.py now\n  tz_convert.py 14:00 PST EST\n  tz_convert.py list"); return
    if args[0] == 'now': now_all()
    elif args[0] == 'list':
        for n, o in sorted(ZONES.items(), key=lambda x:x[1]): print(f"  {n}: UTC{o:+.1f}")
    elif len(args) >= 3:
        convert(args[0], args[1], args[2])

if __name__ == '__main__': main()
