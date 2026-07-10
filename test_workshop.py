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

    def test_interest_score_rewards_first_party_sunset_signal(self):
        # ANALYSIS.md conclusion folded into the heuristic (run 14): an
        # explicitly retired repo outranks an otherwise-identical one.
        from workshop import interest_score
        base = {"stars": 300, "pushed_at": "2020-01-01", "topics": [],
                "license": "MIT"}
        plain = dict(base)
        sunset = dict(base, sunset={"evidence": "archive banner"})
        with_successor = dict(
            base, sunset={"evidence": "archive banner",
                          "successor": "https://example.com/v2"})
        self.assertGreater(interest_score(sunset), interest_score(plain))
        self.assertGreater(interest_score(with_successor),
                           interest_score(sunset))
        # Exact deltas: +4.0 for the sunset signal, +1.0 for a successor.
        self.assertAlmostEqual(
            interest_score(sunset) - interest_score(plain), 4.0)
        self.assertAlmostEqual(
            interest_score(with_successor) - interest_score(sunset), 1.0)

    def test_sunset_bonus_applies_to_every_dataset_sunset_entry(self):
        # Live-data property: removing an entry's sunset object lowers its
        # score by exactly the documented bonus (5.0 with a recorded
        # successor, 4.0 without), and never affects non-sunset entries.
        from workshop import interest_score, load_candidates
        found = 0
        for item in load_candidates():
            sunset = item.get("sunset")
            if not isinstance(sunset, dict):
                continue
            found += 1
            stripped = {k: v for k, v in item.items() if k != "sunset"}
            expected = 5.0 if sunset.get("successor") else 4.0
            self.assertAlmostEqual(
                interest_score(item) - interest_score(stripped), expected,
                msg=item["id"])
        self.assertGreater(found, 0)

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

    def test_new_creative_candidate_is_present_and_findable(self):
        # Run 8: googlecreativelab/teachable-machine-v1 is the dataset's first
        # purely creative non-game system (browser-based creative ML experiment).
        code, out, err = run_cli("show", "teachable-machine-v1")
        self.assertEqual(code, 0, err)
        self.assertIn("googlecreativelab/teachable-machine-v1", out)
        self.assertIn("Apache-2.0", out)
        code, out, err = run_cli("search", "creative-coding")
        self.assertEqual(code, 0, err)
        self.assertIn("teachable-machine-v1", out)

    def test_new_simulator_candidate_is_present_and_findable(self):
        # Run 10: Azure/device-simulation-dotnet is the dataset's first
        # simulator-shaped entry (IoT device simulation microservice),
        # closing the last unrepresented SEED.md shape.
        code, out, err = run_cli("show", "azure-device-simulation")
        self.assertEqual(code, 0, err)
        self.assertIn("Azure/device-simulation-dotnet", out)
        self.assertIn("MIT", out)
        code, out, err = run_cli("search", "simulation-engine")
        self.assertEqual(code, 0, err)
        self.assertIn("azure-device-simulation", out)


class TestJsonOutput(unittest.TestCase):
    """Run 7: --json flag gives machine-readable output for scripting."""

    def test_list_json_parses_and_matches_dataset_size(self):
        with DATA.open() as f:
            expected = len([line for line in f if line.strip()])
        code, out, err = run_cli("list", "--json")
        self.assertEqual(code, 0, err)
        items = json.loads(out)
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), expected)

    def test_rank_json_includes_score_and_is_sorted_desc(self):
        code, out, err = run_cli("rank", "--json")
        self.assertEqual(code, 0, err)
        items = json.loads(out)
        scores = [i["interest_score"] for i in items]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_show_json_roundtrips_single_item(self):
        code, out, err = run_cli("show", "dmarx-psaw", "--json")
        self.assertEqual(code, 0, err)
        item = json.loads(out)
        self.assertEqual(item["id"], "dmarx-psaw")
        self.assertEqual(item["license"], "BSD-2-Clause")

    def test_stats_json_totals_match_dataset(self):
        with DATA.open() as f:
            expected = len([line for line in f if line.strip()])
        code, out, err = run_cli("stats", "--json")
        self.assertEqual(code, 0, err)
        stats = json.loads(out)
        self.assertEqual(stats["total"], expected)
        self.assertEqual(sum(stats["by_license"].values()), expected)



class TestVerifiedOnly(unittest.TestCase):
    """Tests for the --verified-only flag and the [!] caveat marker (run 9)."""

    @staticmethod
    def _caveated(item):
        return any(k.endswith("_note") for k in item)

    def test_list_verified_only_excludes_all_caveated_entries(self):
        code, out, err = run_cli("list", "--verified-only", "--json")
        self.assertEqual(code, 0, err)
        kept = json.loads(out)
        self.assertGreater(len(kept), 0, "some entries should be caveat-free")
        for item in kept:
            self.assertFalse(self._caveated(item),
                             f"{item['id']} carries a caveat but survived --verified-only")
        with DATA.open() as f:
            expected = [json.loads(line) for line in f if line.strip()]
        expected_ids = {i["id"] for i in expected if not self._caveated(i)}
        self.assertEqual({i["id"] for i in kept}, expected_ids)

    def test_rank_verified_only_agrees_with_list_and_stays_sorted(self):
        code, out, err = run_cli("rank", "--verified-only", "--json")
        self.assertEqual(code, 0, err)
        ranked = json.loads(out)
        code, out, err = run_cli("list", "--verified-only", "--json")
        self.assertEqual(code, 0, err)
        listed = json.loads(out)
        self.assertEqual({i["id"] for i in ranked}, {i["id"] for i in listed})
        scores = [i["interest_score"] for i in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_list_marks_caveated_rows_with_flag(self):
        code, out, err = run_cli("list")
        self.assertEqual(code, 0, err)
        with DATA.open() as f:
            items = [json.loads(line) for line in f if line.strip()]
        by_id = {i["id"]: self._caveated(i) for i in items}
        for line in out.splitlines():
            for cid, caveated in by_id.items():
                if line.startswith(cid + " "):
                    self.assertEqual("[!]" in line, caveated,
                                     f"marker mismatch on row for {cid}: {line!r}")

    def test_search_respects_verified_only(self):
        # 'archived' appears in the why/description of caveated entries too;
        # with --verified-only none of the hits may carry caveats.
        code, out, err = run_cli("search", "archived", "--verified-only", "--json")
        self.assertEqual(code, 0, err)
        for item in json.loads(out):
            self.assertFalse(self._caveated(item),
                             f"{item['id']} carries a caveat but matched under --verified-only")


class TestCaveatsInJson(unittest.TestCase):
    """The computed 'caveats' array in --json output (run 11)."""

    @staticmethod
    def _raw_by_id():
        with DATA.open() as f:
            return {json.loads(line)["id"]: json.loads(line)
                    for line in f if line.strip()}

    def test_list_json_caveats_match_raw_note_fields(self):
        code, out, err = run_cli("list", "--json")
        self.assertEqual(code, 0, err)
        raw = self._raw_by_id()
        for entry in json.loads(out):
            expected = sorted(k for k in raw[entry["id"]] if k.endswith("_note"))
            self.assertEqual(entry["caveats"], expected, entry["id"])

    def test_show_json_includes_caveats_array(self):
        code, out, err = run_cli("show", "teachable-machine-v1", "--json")
        self.assertEqual(code, 0, err)
        entry = json.loads(out)
        self.assertIn("stars_note", entry["caveats"])
        self.assertIn("pushed_at_note", entry["caveats"])

    def test_rank_json_carries_both_caveats_and_score(self):
        code, out, err = run_cli("rank", "--json")
        self.assertEqual(code, 0, err)
        for entry in json.loads(out):
            self.assertIn("caveats", entry)
            self.assertIn("interest_score", entry)

    def test_verified_only_json_entries_have_empty_caveats(self):
        code, out, err = run_cli("list", "--verified-only", "--json")
        self.assertEqual(code, 0, err)
        entries = json.loads(out)
        self.assertGreater(len(entries), 0)
        for entry in entries:
            self.assertEqual(entry["caveats"], [], entry["id"])

    def test_stats_reports_caveated_count_in_both_outputs(self):
        with DATA.open() as f:
            raw = [json.loads(line) for line in f if line.strip()]
        expected = sum(1 for i in raw
                       if any(k.endswith("_note") for k in i))
        code, out, err = run_cli("stats", "--json")
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["caveated"], expected)
        code, out, err = run_cli("stats")
        self.assertEqual(code, 0, err)
        self.assertIn(f"Caveated (any *_note): {expected}/{len(raw)}", out)


class TestSunsets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DATA.open() as f:
            cls.raw = [json.loads(line) for line in f if line.strip()]
        cls.sunset_ids = {i["id"] for i in cls.raw if isinstance(i.get("sunset"), dict)}

    def test_sunset_data_carries_evidence(self):
        # Every sunset object must record its evidence string (honesty rule:
        # the claim of a deliberate retirement must be traceable).
        for item in self.raw:
            if isinstance(item.get("sunset"), dict):
                self.assertIn("evidence", item["sunset"], item["id"])
                self.assertTrue(item["sunset"]["evidence"].strip(), item["id"])

    def test_sunsets_command_matches_raw_data(self):
        code, out, err = run_cli("sunsets")
        self.assertEqual(code, 0, err)
        for sid in self.sunset_ids:
            self.assertIn(sid, out)
        self.assertIn(f"{len(self.sunset_ids)} of {len(self.raw)} candidate(s)", out)
        # Entries without a sunset object must not be listed.
        for item in self.raw:
            if item["id"] not in self.sunset_ids:
                self.assertNotIn(item["id"], out)

    def test_sunsets_json_ids_and_caveats(self):
        code, out, err = run_cli("sunsets", "--json")
        self.assertEqual(code, 0, err)
        data = json.loads(out)
        self.assertEqual({i["id"] for i in data}, self.sunset_ids)
        for entry in data:
            self.assertIn("caveats", entry)
            self.assertIn("evidence", entry["sunset"])

    def test_show_renders_sunset_successor(self):
        code, out, err = run_cli("show", "azure-device-simulation")
        self.assertEqual(code, 0, err)
        self.assertIn("self-aware sunset", out)
        self.assertIn("azure-iot-pcs-device-simulation", out)

    def test_stats_reports_sunset_census_in_both_outputs(self):
        expected = len(self.sunset_ids)
        code, out, err = run_cli("stats", "--json")
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["self_aware_sunsets"], expected)
        code, out, err = run_cli("stats")
        self.assertEqual(code, 0, err)
        self.assertIn(f"Self-aware sunsets: {expected}/{len(self.raw)}", out)

    def test_sunsets_respects_verified_only(self):
        code, out, err = run_cli("sunsets", "--verified-only", "--json")
        self.assertEqual(code, 0, err)
        for entry in json.loads(out):
            self.assertEqual(entry["caveats"], [])
            self.assertIn(entry["id"], self.sunset_ids)


if __name__ == "__main__":
    unittest.main()


class TestShowSlugLookup(unittest.TestCase):
    """Run 16: `show` accepts the GitHub owner/name slug as an alternate key,
    and misses exit non-zero with near-miss suggestions on stderr."""

    def test_show_by_exact_slug(self):
        code, out, err = run_cli("show", "PagerDuty/cronner")
        self.assertEqual(code, 0, err)
        self.assertIn("pagerduty-cronner", out)

    def test_show_slug_is_case_insensitive(self):
        # GitHub slugs are case-insensitive; ours should be too.
        code, out, err = run_cli("show", "pagerduty/CRONNER")
        self.assertEqual(code, 0, err)
        self.assertIn("pagerduty-cronner", out)

    def test_show_by_slug_json_matches_id_lookup(self):
        code_slug, out_slug, _ = run_cli("show", "mozilla/notes", "--json")
        code_id, out_id, _ = run_cli("show", "mozilla-notes", "--json")
        self.assertEqual(code_slug, 0)
        self.assertEqual(code_id, 0)
        self.assertEqual(json.loads(out_slug), json.loads(out_id))

    def test_every_dataset_slug_resolves(self):
        with DATA.open() as f:
            entries = [json.loads(line) for line in f if line.strip()]
        for entry in entries:
            code, out, err = run_cli("show", entry["name"])
            self.assertEqual(code, 0, f"slug {entry['name']} failed: {err}")
            self.assertIn(entry["id"], out)

    def test_miss_suggests_near_matches_and_exits_nonzero(self):
        code, out, err = run_cli("show", "cronner")
        self.assertEqual(code, 1)
        self.assertIn("no candidate", err)
        self.assertIn("did you mean", err)
        self.assertIn("pagerduty-cronner", err)

    def test_miss_with_no_near_match_exits_nonzero_without_suggestions(self):
        code, out, err = run_cli("show", "zzz-nope")
        self.assertEqual(code, 1)
        self.assertIn("no candidate", err)
        self.assertNotIn("did you mean", err)


class TestListSort(unittest.TestCase):
    """Black-box tests for `list --sort stars|age|score` (run 17)."""

    @staticmethod
    def _raw_entries():
        with DATA.open() as f:
            return [json.loads(line) for line in f if line.strip()]

    def _listed_ids(self, *args):
        code, out, err = run_cli("list", "--json", *args)
        self.assertEqual(code, 0, err)
        return [e["id"] for e in json.loads(out)]

    def test_default_order_is_file_order(self):
        raw_ids = [e["id"] for e in self._raw_entries()]
        self.assertEqual(self._listed_ids(), raw_ids)

    def test_sort_stars_is_descending(self):
        entries = {e["id"]: e for e in self._raw_entries()}
        stars = [entries[i].get("stars") or 0
                 for i in self._listed_ids("--sort", "stars")]
        self.assertEqual(stars, sorted(stars, reverse=True))

    def test_sort_age_puts_oldest_push_first(self):
        entries = {e["id"]: e for e in self._raw_entries()}
        dates = [entries[i].get("pushed_at")
                 for i in self._listed_ids("--sort", "age")]
        dated = [d for d in dates if d]
        self.assertEqual(dated, sorted(dated))  # ISO dates sort lexically

    def test_sort_score_matches_rank_ordering(self):
        code, out, err = run_cli("rank", "--json")
        self.assertEqual(code, 0, err)
        rank_ids = [e["id"] for e in json.loads(out)]
        list_ids = self._listed_ids("--sort", "score")
        # Same score => order among ties is not asserted; compare scores.
        rank_scores = {e["id"]: e["interest_score"] for e in json.loads(out)}
        self.assertEqual([rank_scores[i] for i in list_ids],
                         [rank_scores[i] for i in rank_ids])

    def test_sort_equals_syntax_matches_flag_syntax(self):
        self.assertEqual(self._listed_ids("--sort=stars"),
                         self._listed_ids("--sort", "stars"))

    def test_unknown_sort_key_exits_2_with_valid_keys_listed(self):
        code, out, err = run_cli("list", "--sort", "bogus")
        self.assertEqual(code, 2)
        self.assertIn("unknown sort key", err)
        for key in ("stars", "age", "score"):
            self.assertIn(key, err)

    def test_sort_missing_value_exits_2_with_usage(self):
        code, out, err = run_cli("list", "--sort")
        self.assertEqual(code, 2)
        self.assertIn("usage", err)

    def test_sort_respects_verified_only(self):
        ids = self._listed_ids("--sort", "stars", "--verified-only")
        entries = {e["id"]: e for e in self._raw_entries()}
        for i in ids:
            notes = [k for k in entries[i] if k.endswith("_note")]
            self.assertEqual(notes, [], f"{i} should have no caveats")
        stars = [entries[i].get("stars") or 0 for i in ids]
        self.assertEqual(stars, sorted(stars, reverse=True))
