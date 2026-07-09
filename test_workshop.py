"""
Smoke tests for workshop.py.

Runs the CLI as a subprocess (black-box) against the real seed dataset in
data/candidates.jsonl, so it also acts as a basic data-integrity check.
No external dependencies -- stdlib unittest + subprocess only.

Run with: python3 -m unittest test_workshop.py -v
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPT = ROOT / "workshop.py"
DATA = ROOT / "data" / "candidates.jsonl"


def run_cli(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout, result.stderr


class TestDataIntegrity(unittest.TestCase):
    def test_seed_data_exists_and_parses(self):
        self.assertTrue(DATA.exists(), "data/candidates.jsonl must exist")
        with DATA.open() as f:
            lines = [line for line in f if line.strip()]
        self.assertGreater(len(lines), 0, "seed dataset should not be empty")
        for line in lines:
            item = json.loads(line)
            for field in ("id", "name", "url", "license", "why"):
                self.assertIn(field, item, f"missing '{field}' in {item.get('id')}")

    def test_ids_are_unique(self):
        with DATA.open() as f:
            ids = [json.loads(line)["id"] for line in f if line.strip()]
        self.assertEqual(len(ids), len(set(ids)), "candidate ids must be unique")


class TestCLI(unittest.TestCase):
    def test_list_runs_and_shows_all_candidates(self):
        code, out, err = run_cli("list")
        self.assertEqual(code, 0, err)
        with DATA.open() as f:
            n = sum(1 for line in f if line.strip())
        self.assertIn(f"{n} candidate(s)", out)

    def test_show_known_id(self):
        code, out, err = run_cli("show", "mozilla-notes")
        self.assertEqual(code, 0, err)
        self.assertIn("mozilla/notes", out)
        self.assertIn("MPL-2.0", out)

    def test_show_unknown_id_fails_cleanly(self):
        code, out, err = run_cli("show", "does-not-exist")
        self.assertNotEqual(code, 0)
        self.assertIn("no candidate", err)

    def test_search_finds_expected_match(self):
        code, out, err = run_cli("search", "redis")
        self.assertEqual(code, 0, err)
        self.assertIn("readthis", out)

    def test_search_no_match(self):
        code, out, err = run_cli("search", "zzz-nonexistent-keyword")
        self.assertEqual(code, 0, err)
        self.assertIn("no matches", out)

    def test_tags_runs(self):
        code, out, err = run_cli("tags")
        self.assertEqual(code, 0, err)
        self.assertIn("android", out)

    def test_no_args_prints_usage_without_crashing(self):
        code, out, err = run_cli()
        self.assertEqual(code, 0)
        self.assertIn("commands:", out)

    def test_rank_runs_and_lists_all_candidates(self):
        code, out, err = run_cli("rank")
        self.assertEqual(code, 0, err)
        with DATA.open() as f:
            ids = [json.loads(line)["id"] for line in f if line.strip()]
        for candidate_id in ids:
            self.assertIn(candidate_id, out)
        self.assertIn("ranked by interest_score", out)

    def test_rank_output_order_matches_score_sort(self):
        from workshop import interest_score, load_candidates
        items = load_candidates()
        expected_order = [
            item["id"] for item in sorted(items, key=interest_score, reverse=True)
        ]
        code, out, err = run_cli("rank")
        self.assertEqual(code, 0, err)
        actual_order = [
            candidate_id
            for line in out.splitlines()
            for candidate_id in expected_order
            if candidate_id in line
        ]
        self.assertEqual(actual_order, expected_order)

    def test_interest_score_prefers_permissive_license(self):
        from workshop import interest_score
        base = {"stars": 300, "pushed_at": "2020-01-01", "topics": []}
        permissive = dict(base, license="MIT")
        proprietary = dict(base, license="Custom")
        self.assertGreater(interest_score(permissive), interest_score(proprietary))

    def test_stats_runs_and_reports_totals(self):
        code, out, err = run_cli("stats")
        self.assertEqual(code, 0, err)
        with DATA.open() as f:
            n = sum(1 for line in f if line.strip())
        self.assertIn(f"Total candidates: {n}", out)
        self.assertIn("By license:", out)
        self.assertIn("By language:", out)

    def test_stats_license_breakdown_matches_data(self):
        code, out, err = run_cli("stats")
        self.assertEqual(code, 0, err)
        with DATA.open() as f:
            licenses = [json.loads(line)["license"] for line in f if line.strip()]
        mit_count = licenses.count("MIT")
        self.assertIn(f"{mit_count:>3}  MIT", out)

    def test_show_flags_unverified_stars_on_run1_seed_entries(self):
        # Run 5 discovered that all 5 run-1 seed entries return an identical
        # (likely placeholder) star count from live fetches; they now carry a
        # stars_note field that `show` must surface to the user.
        code, out, err = run_cli("show", "mozilla-notes")
        self.assertEqual(code, 0, err)
        self.assertIn("stars_note", out)
        self.assertIn("Unverified", out)

    def test_new_game_candidate_is_present_and_findable(self):
        code, out, err = run_cli("show", "redpoint-protogame")
        self.assertEqual(code, 0, err)
        self.assertIn("RedpointArchive/Protogame", out)
        self.assertIn("MIT", out)
        code, out, err = run_cli("search", "game-engine")
        self.assertEqual(code, 0, err)
        self.assertIn("redpoint-protogame", out)

    def test_new_dataset_candidate_is_present_and_findable(self):
        # Run 6: dmarx/psaw is the dataset's first dataset/data-access-shaped
        # entry (a wrapper around the now-defunct Pushshift Reddit dataset).
        code, out, err = run_cli("show", "dmarx-psaw")
        self.assertEqual(code, 0, err)
        self.assertIn("dmarx/psaw", out)
        self.assertIn("BSD-2-Clause", out)
        code, out, err = run_cli("search", "pushshift")
        self.assertEqual(code, 0, err)
        self.assertIn("dmarx-psaw", out)


if __name__ == "__main__":
    unittest.main()
