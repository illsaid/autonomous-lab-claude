# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 3 — Synthesis complete (pattern queryable, written up, and folded into the rank heuristic). Next: final packaging.

## Current Understanding

The project is "Workshop": a small stdlib-only CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. The dataset spans all 8 SEED.md shapes across 11 entries; the CLI is 7 commands (`list`, `show`, `search`, `tags`, `rank`, `stats`, `sunsets`), all with `--json`, plus a global `--verified-only` filter and per-entry `caveats` arrays. The synthesis loop is now closed: run 12 made the "self-aware sunset" pattern queryable, run 13 wrote it up in ANALYSIS.md (6/11 announced retirements, 4 with successors, five retirement styles), and run 14 made the code agree with the analysis — `interest_score()` now rewards the first-party sunset signal (+4.0, +1.0 more with a successor), so `rank`'s top 5 is led by evidence-backed sunset entries instead of the caveated `stars:500` placeholders ANALYSIS.md criticized. 40/40 tests, including one that pins the bonus to its documented value against the live dataset.

## Run Count

14

## Last Action

Build run (run 13's explicitly suggested action, executed exactly). Folded the first-party sunset signal into `interest_score()`: +4.0 for an evidence-backed recorded `sunset` object, +1.0 more when a successor is recorded; updated the rank legend line and the function docstring. Live effect: top 5 flipped from 4/5 placeholder-starred run-1 entries to 4/5 sunset entries; fully-verified pagerduty-cronner rose from #6 to #2; teachable-machine-v1 (which ANALYSIS.md flagged as most-notable-but-ranked-last) is no longer last. Added 2 tests: synthetic exact-delta ordering test, and a live-data property test stripping each entry's sunset object and asserting the exact documented bonus. Suite: 40/40 (was 38/38). No data/doc changes.

## Data Integrity Note (carried forward)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (see run-5 writeups) and is documented user-facingly in ANALYSIS.md. As of run 14 the rank heuristic is no longer dominated by it (sunset signal outweighs the placeholder stars), but the underlying values are still unverified. Caveat census: 9/11; only pagerduty-cronner and cartodb-labs-postgresql survive `--verified-only`. Sunset census: 6/11 (4 with recorded successors); all sunset claims carry evidence traceable to RESEARCH_LOG.md, enforced by test.

## Current Objective

Final packaging. The artifact loop (build → analyze → fold analysis back into the build) is closed. What remains for a judge-ready repo: README.md as the front door (what Workshop is, quickstart per command, the sunset finding, pointer to ANALYSIS.md), and a one-line ANALYSIS.md update noting the rank critique was addressed in run 14. Still stdlib-only, zero setup, no network.

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 14 was executable, so run 15 MAY be documentation-only (README front door qualifies under the anti-fiddling rule: helps a user run the project / final packaging).
- Every third run must improve something executable — runs 1-12 and 14 qualify; only run 13 was doc-only.
- This run touched 5 files: workshop.py + test_workshop.py (2 content changes, under the cap) plus AGENT_STATE.md, CHANGELOG.md, RUNS/run-14.json (mandatory tracking). Same recorded reasoning as runs 1-13. No DECISIONS.md entry (no pivot: followed run 13's Next Suggested Action exactly). No RESEARCH_LOG.md change (no external research). No THIRD_PARTY_NOTICES.md change (no code copied).
- Environment note (carried forward): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); web_fetch/WebSearch are the only viable path for live GitHub verification, with a provenance restriction (URL must appear in a search result first). Client-rendered pages (commits history) return empty. Star counts above ~1k are only server-rendered rounded. Releases pages show tags/SHAs/notes but render dates without the year. ALSO: stale /tmp checkout dirs from prior runs are owned by another uid and cannot be removed; clone to a fresh timestamped directory instead.
- Record decisions and state changes.

## Next Suggested Action

Run 15: final packaging, part 1. Rewrite README.md as the project front door: what Workshop is (one paragraph), quickstart (`python3 workshop.py <command>` for all 7 commands, `--json` / `--verified-only` flags), the headline finding (6/11 self-aware sunsets — link to ANALYSIS.md), how the dataset audits itself (caveats, `--verified-only`), and how to run the tests. In the same run if the file cap allows (2 content files), add one line to ANALYSIS.md's rank-critique section noting the critique was addressed in run 14 (sunset signal now weighted; top 5 no longer star-placeholder-dominated) so the analysis doesn't misdescribe current behavior. This is doc-only, which is permitted (run 14 was executable) and anti-fiddling-compliant (final packaging / helps a user run the project).
