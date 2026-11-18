#!/usr/bin/env python3
"""delta.py 的回归测试:重点是 ③b 的仓库身份归一与候选分层。

运行:python3 -m unittest _digested/ecosystem/test_delta.py
"""
import importlib.util
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "delta", Path(__file__).resolve().parent / "delta.py")
delta = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(delta)


def entry(name, url, en="", zh=""):
    return {
        "name": name,
        "url": url,
        "repo": delta.repo_key(url),
        "description.en": en,
        "description.zh": zh,
    }


class RepoKeyTest(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(
            delta.repo_key("https://github.com/omdsh-dev/DSH-better-sidebar"),
            "omdsh-dev/dsh-better-sidebar")

    def test_tree_subpath(self):
        self.assertEqual(
            delta.repo_key("https://github.com/volcengine/OpenViking/tree/main/examples/dsh-memory-plugin"),
            "volcengine/openviking")

    def test_hash_subpath(self):
        self.assertEqual(
            delta.repo_key("https://github.com/Q00/ouroboros#integrations/dsh-plugin"),
            "q00/ouroboros")

    def test_dot_git_and_case(self):
        self.assertEqual(
            delta.repo_key("https://github.com/Vectorize-IO/Hindsight.git"),
            "vectorize-io/hindsight")

    def test_bare_owner_repo(self):
        self.assertEqual(delta.repo_key("omdsh-dev/DSH-better-sidebar"),
                         "omdsh-dev/dsh-better-sidebar")
        self.assertEqual(delta.repo_key("omdsh-dev/DSH-better-sidebar#tab"),
                         "omdsh-dev/dsh-better-sidebar")

    def test_non_github(self):
        self.assertIsNone(delta.repo_key("https://example.com/a/b"))


class ClassifyTest(unittest.TestCase):
    def setUp(self):
        self.entries = [
            entry("vectorize-io/hindsight", "https://github.com/vectorize-io/hindsight",
                  en="long-term memory"),
            entry("vectorize-io/hindsight#coding-agents",
                  "https://github.com/vectorize-io/hindsight/tree/main/coding-agents",
                  en="harness adapter"),
            entry("alice/dsh-hindsight-gui", "https://github.com/alice/dsh-hindsight-gui",
                  en="GUI for hindsight"),
            entry("bob/memory-tools", "https://github.com/bob/memory-tools",
                  en="works with hindsight memory"),
            entry("carol/unrelated", "https://github.com/carol/unrelated",
                  en="nothing here"),
        ]

    def test_self_is_repo_identity_not_url_substring(self):
        tiers = delta.classify_hits(self.entries, "hindsight", "vectorize-io/hindsight")
        self.assertEqual(len(tiers["self"]), 2)
        self.assertEqual([e["name"] for e in tiers["name"]], ["alice/dsh-hindsight-gui"])
        self.assertEqual([e["name"] for e in tiers["mention"]], ["bob/memory-tools"])

    def test_name_following_derivative_is_not_self(self):
        entries = [
            entry("omdsh-dev/DSH-better-sidebar",
                  "https://github.com/omdsh-dev/DSH-better-sidebar"),
            entry("All3nCN/dsh-better-sidebar-N23",
                  "https://github.com/All3nCN/dsh-better-sidebar-N23",
                  en="full workbench fork"),
        ]
        tiers = delta.classify_hits(entries, "better-sidebar", "omdsh-dev/dsh-better-sidebar")
        self.assertEqual(len(tiers["self"]), 1)
        self.assertEqual(len(tiers["name"]), 1)
        self.assertEqual(tiers["mention"], [])


if __name__ == "__main__":
    unittest.main()
