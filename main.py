"""Flag VPN sessions idle over a threshold.

Usage: python3 main.py sessions.csv [--idle-minutes 30]
       [--as-of 2026-11-16T10:00:00]
CSV columns: user,session_start,last_activity (ISO datetimes,
e.g. 2026-11-16T08:00:00). Idle time is --as-of (default: now)
minus last_activity. Verdicts:
- IDLE: idle longer than --idle-minutes (default 30).
- ACTIVE: idle at or under the threshold.
Longest idle first. Rows with an unparseable timestamp are
reported as skipped, not silently dropped.
"""
import argparse, csv, sys
from datetime import datetime

def check(rows, idle_minutes=30, as_of=None):
    as_of = as_of or datetime.now()
    out = []
    skipped = 0
    for row in rows:
        try:
            user = row["user"].strip()
            start = datetime.fromisoformat(row["session_start"].strip())
            last = datetime.fromisoformat(row["last_activity"].strip())
            if not user:
                raise ValueError("missing user")
        except (KeyError, AttributeError, ValueError, TypeError):
            skipped += 1
            continue
        idle = int((as_of - last).total_seconds() // 60)
        verdict = "IDLE" if idle > idle_minutes else "ACTIVE"
        detail = (f"idle {idle} minute(s), session started {start}, "
                  f"last activity {last}")
        out.append((user, idle, verdict, detail))
    out.sort(key=lambda r: (-r[1], r[0]))
    return out, skipped

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--idle-minutes", type=int, default=30)
    parser.add_argument("--as-of", default=None,
                        help="reference time ISO format (default: now)")
    args = parser.parse_args(argv)
    as_of = datetime.fromisoformat(args.as_of) if args.as_of else None
    with open(args.path, newline="", encoding="utf-8") as f:
        results, skipped = check(list(csv.DictReader(f)),
                                 args.idle_minutes, as_of)
    for user, _, verdict, detail in results:
        print(f"{user}: {verdict} - {detail}")
    idle_count = sum(1 for *_, verdict, _ in results if verdict == "IDLE")
    print(f"{idle_count} idle, {len(results) - idle_count} active out of "
          f"{len(results)} session(s).")
    if skipped:
        print(f"Skipped {skipped} invalid row(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
