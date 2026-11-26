# vpn-session-idle-timeout-checker

Flag VPN sessions idle over a threshold: the input CSV lists user, session_start and last_activity (ISO datetimes, e.g. 2026-11-16T08:00:00) — idle time is --as-of (default now) minus last_activity — IDLE when idle longer than --idle-minutes (default 30), ACTIVE when idle at or under the threshold — longest idle first. Rows with an unparseable timestamp are reported as skipped, not silently dropped.

Sample input is included (sample.csv with five sessions, one invalid row).

## How to run

```sh
python3 main.py sample.csv --as-of 2026-11-16T10:00:00
```

## Example output

```
omar: IDLE - idle 235 minute(s), session started 2026-11-16 06:00:00, last activity 2026-11-16 06:05:00
bilal: IDLE - idle 110 minute(s), session started 2026-11-16 07:30:00, last activity 2026-11-16 08:10:00
sara: ACTIVE - idle 10 minute(s), session started 2026-11-16 09:00:00, last activity 2026-11-16 09:50:00
ayesha: ACTIVE - idle 5 minute(s), session started 2026-11-16 08:00:00, last activity 2026-11-16 09:55:00
2 idle, 2 active out of 4 session(s).
Skipped 1 invalid row(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
