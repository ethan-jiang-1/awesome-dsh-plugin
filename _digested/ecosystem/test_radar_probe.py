#!/usr/bin/env python3
"""radar_probe.py 的回归测试:标识符校验、GraphQL 查询构造与来源启发式分类。

运行:python3 -m unittest _digested/ecosystem/test_radar_probe.py
"""
import importlib.util
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "radar_probe", Path(__file__).resolve().parent / "radar_probe.py")
radar_probe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(radar_probe)


class RadarProbeTest(unittest.TestCase):
    def test_split_valid_repo(self):
        self.assertEqual(radar_probe.split_valid_repo("omdsh-dev/dsh-better-sidebar"),
                         ("omdsh-dev", "dsh-better-sidebar"))
        self.assertEqual(radar_probe.split_valid_repo("user.1/repo_2.js"),
                         ("user.1", "repo_2.js"))
        self.assertIsNone(radar_probe.split_valid_repo('bad"owner/repo'))
        self.assertIsNone(radar_probe.split_valid_repo("only-one-part"))
        self.assertIsNone(radar_probe.split_valid_repo("a/b/c"))

    def test_build_graphql_query(self):
        q = radar_probe.build_graphql_query([(0, "foo", "bar"), (1, "baz", "qux")])
        self.assertIn('r0: repository(owner:"foo",name:"bar")', q)
        self.assertIn('r1: repository(owner:"baz",name:"qux")', q)
        self.assertIn("stargazerCount", q)
        self.assertIn("createdAt", q)

    def test_classify_origin(self):
        self.assertEqual(
            radar_probe.classify_origin({"created_at": "2024-05-01T00:00:00Z", "is_fork": False}),
            "pre-dsh-host",
        )
        self.assertEqual(
            radar_probe.classify_origin({"created_at": "2026-11-20T00:00:00Z", "is_fork": False}, has_subpath=True),
            "monorepo-subpath",
        )
        self.assertEqual(
            radar_probe.classify_origin({"created_at": "2026-11-20T00:00:00Z", "is_fork": True}),
            "github-fork",
        )
        self.assertEqual(
            radar_probe.classify_origin({"created_at": "2026-11-20T00:00:00Z", "is_fork": False}),
            "dsh-native",
        )


if __name__ == "__main__":
    unittest.main()
