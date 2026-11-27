#!/usr/bin/env python3
"""view_data.py 的回归测试:最新快照自动选取与基于 asof 的过期天数计算。

运行:python3 -m unittest _digested/ecosystem/test_view_data.py
"""
import importlib.util
import tempfile
import unittest
from datetime import date
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "view_data", Path(__file__).resolve().parent / "view_data.py")
view_data = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(view_data)


class ViewDataTest(unittest.TestCase):
    def test_latest_snapshot_picks_newest_by_date(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "live-2026-11-19.json").write_text("{}", encoding="utf-8")
            (d / "live-2026-11-27.json").write_text("{}", encoding="utf-8")
            (d / "stars-2026-09-30.json").write_text("{}", encoding="utf-8")
            self.assertEqual(view_data.latest_snapshot(d).name, "live-2026-11-27.json")

    def test_latest_snapshot_empty(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertIsNone(view_data.latest_snapshot(Path(td)))

    def test_days_since_uses_ref_date_not_wall_clock(self):
        ref = date(2026, 11, 19)
        self.assertEqual(view_data.days_since("2026-11-18T12:00:00Z", ref_date=ref), 1)
        self.assertEqual(view_data.days_since("2026-08-16T00:00:00Z", ref_date=ref), 95)

    def test_parse_ref_date(self):
        self.assertEqual(view_data.parse_ref_date("2026-11-27"), date(2026, 11, 27))
        self.assertEqual(view_data.parse_ref_date("2026-11-27T08:00:00Z"), date(2026, 11, 27))
        self.assertIsNone(view_data.days_since("bad-date", ref_date=date(2026, 11, 27)))


if __name__ == "__main__":
    unittest.main()
