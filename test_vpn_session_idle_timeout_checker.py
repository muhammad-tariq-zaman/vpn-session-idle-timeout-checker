import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
import datetime
from main import check

AS_OF = datetime.datetime(2026, 11, 16, 10, 0, 0)

def row(user, start, last):
    return {"user": user, "session_start": start, "last_activity": last}

class TestVpnIdleChecker(unittest.TestCase):
    def test_idle(self):
        r, _ = check([row("bilal", "2026-11-16T07:30:00", "2026-11-16T08:10:00")],
                     as_of=AS_OF)
        self.assertEqual((r[0][2], r[0][1]), ("IDLE", 110))

    def test_active(self):
        r, _ = check([row("ayesha", "2026-11-16T08:00:00", "2026-11-16T09:55:00")],
                     as_of=AS_OF)
        self.assertEqual((r[0][2], r[0][1]), ("ACTIVE", 5))

    def test_exactly_threshold_is_active(self):
        r, _ = check([row("sara", "2026-11-16T09:00:00", "2026-11-16T09:30:00")],
                     as_of=AS_OF)
        self.assertEqual(r[0][2], "ACTIVE")

    def test_custom_threshold(self):
        r, _ = check([row("bilal", "2026-11-16T07:30:00", "2026-11-16T08:10:00")],
                     idle_minutes=120, as_of=AS_OF)
        self.assertEqual(r[0][2], "ACTIVE")

    def test_longest_idle_first(self):
        r, _ = check([row("ayesha", "2026-11-16T08:00:00", "2026-11-16T09:55:00"),
                      row("omar", "2026-11-16T06:00:00", "2026-11-16T06:05:00"),
                      row("bilal", "2026-11-16T07:30:00", "2026-11-16T08:10:00")],
                     as_of=AS_OF)
        self.assertEqual([x[0] for x in r], ["omar", "bilal", "ayesha"])

    def test_invalid_timestamp_is_skipped(self):
        r, skipped = check([row("broken", "2026-11-16T08:00:00", "not-a-time"),
                            row("ayesha", "2026-11-16T08:00:00", "2026-11-16T09:55:00")],
                           as_of=AS_OF)
        self.assertEqual((len(r), skipped), (1, 1))

    def test_empty_input(self):
        self.assertEqual(check([], as_of=AS_OF), ([], 0))
