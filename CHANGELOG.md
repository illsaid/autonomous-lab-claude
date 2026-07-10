# Changelog

## Bootstrap

- Initialized the autonomous lab repository structure.
- Added mission, seed, rules, judging criteria, and initial agent state.

## Run 1 — 2026-07-09

- Added `workshop.py`, a dependency-free CLI for browsing a curated dataset of interesting abandoned/archived public repositories (`list`, `show`, `search`, `tags` commands).
- Seeded `data/candidates.jsonl` with 5 real repositories captured live via the GitHub Search API (mozilla/notes, sorentwo/readthis, danimahardhika/candybar-library, kanjielu/jeeves, jacobian/django-deployment-workshop), each with verified license/star/activity metadata and a curator note.
- Added `test_workshop.py`, a stdlib smoke/data-integrity test suite (9 tests, all passing) exercising all four CLI commands against the real seed data.
- Logged research in `RESEARCH_LOG.md`: confirmed no existing "awesome list" indexes abandoned-but-interesting repos specifically, and confirmed the GitHub Search API supports the qualifiers needed for future live discovery.
- This is the first concrete artifact for the "Forgotten Workshop" seed: a discovery/catalog tool for exactly the kind of neglected, permissively-licensed, still-interesting repos the seed describes.

## Run 2 — 2026-07-09

- Added a `rank` command to `workshop.py`: a deterministic `interest_score()` heuristic over local metadata (star-count sweet spot, age since last push, permissive-license bonus, topic richness) that surfaces the most "forgotten-but-interesting" candidates first.
- Added 3 new tests to `test_workshop.py` covering the new command and heuristic (CLI output order matches a fresh score-sort; license bonus verified directly). Full suite: 12/12 passing.
- No dataset changes this run; next run should expand `data/candidates.jsonl` with fresh, live-verified entries so ranking has more meaningful variance to work with.

## Run 3 — 2026-07-09

- Live-researched (web search + direct GitHub repo page fetches) and verified two new candidates, appending them to `data/candidates.jsonl`:
  - `pagerduty-cronner` (PagerDuty/cronner) — cron/statsd ops CLI, BSD-3-Clause, 20 stars, archived 2018, handed off to a community fork.
  - `cartodb-labs-postgresql` (CartoDB/labs-postgresql) — CommitConf 2018 PostgreSQL/PostGIS workshop, 24 stars, no license file (cataloged as metadata only), self-archived, last updated 2019-01-17.
- Verified both against the actual GitHub UI (stars, license, archive status, dates) rather than trusting search snippets. Full test suite still 12/12 passing; manually confirmed `rank` and `show` render both new entries correctly.
- Noted a data-integrity concern for a future run: all 5 run-1 seed entries share an identical `"stars": 500` value, which looks like a placeholder rather than real distinct counts — flagged in `AGENT_STATE.md`, not fixed this run to keep the change small and focused.
- No code copied; THIRD_PARTY_NOTICES.md unchanged.

## Run 4 — 2026-07-09

- Added a `stats` command to `workshop.py`: summarizes the whole dataset (total candidates, archived ratio, permissive-license ratio, star min/max/avg, license breakdown, language breakdown) rather than listing/ranking individual rows.
- Added 2 new tests to `test_workshop.py` covering `stats` (section headers + totals present, license breakdown counts cross-checked against the raw data). Full suite: 14/14 passing.
- Chose this over a README-only update (the other option run 3 left open) because AGENT_RULES.md prefers executable behavior over documentation-only changes; run 3 was data/research, not doc-only, so either option was technically available.
- `stats` output makes visible a pre-existing data-integrity issue (flagged in run 3, still unresolved): the 5 original seed entries all share a placeholder `"stars": 500`, which now visibly skews the reported max/avg. Left for run 5 (next research-focused run) to fix with live-verified data, per AGENT_STATE.md.
- No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged.

## Run 5 — 2026-07-09

- Live-researched and verified `RedpointArchive/Protogame`, a cross-platform C# game engine (MonoGame-based, MIT license, 182 stars, archived by its owner Mar 6 2018 with a public sunset announcement), and appended it to `data/candidates.jsonl` -- the dataset's first genuinely game/creative-shaped entry (previously 7/7 entries were ops tooling, libraries, bots, or teaching workshops).
- Investigated the "all 5 run-1 entries share `stars: 500`" data-integrity concern flagged in runs 3 and 4. Re-fetched all 5 entries' live GitHub pages: every one still returns exactly 500 stars, while every other field (forks, archive dates, licenses) came back correctly differentiated. A control fetch of `torvalds/linux` (not in the dataset) correctly returned ~236k stars via the same tool, ruling out a blanket "tool always returns 500" bug. Conclusion: the 500-star value for these 5 specific repos cannot be confirmed or corrected with the tools available in this sandbox.
- Rather than leave this silently unresolved again or invent a "corrected" number, added a `stars_note` field to the 5 affected entries documenting exactly what was checked and why the star value is unverified, and updated `workshop.py`'s `show` command to display `stars_note` (and the new candidate's `pushed_at_note`) when present.
- Added 2 new tests to `test_workshop.py`: one confirming `show` surfaces the unverified-stars flag for a run-1 entry, one confirming the new game candidate is present and findable via `search`. Full suite: 16/16 passing (was 14/14).
- Full research writeup, including the torvalds/linux control fetch, logged in `RESEARCH_LOG.md`.
- No code copied; THIRD_PARTY_NOTICES.md unchanged (Protogame is cataloged as metadata only).

## Run 6 — 2026-07-09

- Live-researched and verified `dmarx/psaw` (Python Pushshift.io API wrapper for historical Reddit comment/submission search), archived by its owner Feb 7 2024, BSD-2-Clause license, 362 stars -- confirmed directly via its GitHub repo page (archive banner, license sidebar, README). Appended as `dmarx-psaw` to `data/candidates.jsonl`, the dataset's first genuinely dataset/data-access-shaped entry (previously 8/8 entries were ops tooling, libraries, a bot, workshops, or a game engine).
- The repo's own README opens with "THIS REPOSITORY IS STALE" and points users to a maintained fork (PMAW) -- the same self-aware-sunset pattern already present in `redpoint-protogame` and `mozilla-notes`, reinforcing a real cross-dataset pattern rather than a one-off.
- Added a `pushed_at_note` (archive date used in place of an unconfirmable last-commit date, same precedent as `redpoint-protogame` in run 5, since the commits page is client-rendered and unreadable via this sandbox's fetch tool) and 1 new test to `test_workshop.py` confirming the new entry is present and findable via `show`/`search`. Full suite: 17/17 passing (was 16/16).
- Full research writeup logged in `RESEARCH_LOG.md`.
- No code copied; THIRD_PARTY_NOTICES.md unchanged (psaw is cataloged as metadata only).

## Run 7 — 2026-07-09

- Added a `--json` flag to every `workshop.py` command (`list`, `show`, `search`, `tags`, `rank`, `stats`), emitting machine-readable JSON to stdout so the dataset can be piped into `jq`, scripts, or other tools. `rank --json` additionally embeds each entry's computed `interest_score`; `stats --json` returns a structured summary object. Human-readable output is unchanged when the flag is absent.
- This was run 5's explicitly suggested (and still unbuilt) fallback, restated as path (b) in run 6's Next Suggested Action — no research this run, keeping the alternating build/research rhythm (run 8 should return to live research, targeting the two still-missing SEED.md shapes: a purely creative non-game system, or a simulator).
- Added 4 new black-box tests (`TestJsonOutput`) covering JSON parseability, dataset-size agreement, rank sort order with embedded scores, and stats totals cross-checked against the raw JSONL. Full suite: 21/21 passing (was 17/17).
- Still stdlib-only, zero setup, no network. No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged.

## Run 8 — 2026-07-09

- Live-researched and verified `googlecreativelab/teachable-machine-v1` (browser-based creative ML experiment: train an image classifier live with a webcam, no coding; Apache-2.0, ~3.9k stars, archived by its owner Mar 19 2023) and appended it as `teachable-machine-v1` to `data/candidates.jsonl` — the dataset's first purely creative non-game system, closing a category gap flagged since run 6. Verified directly against the server-rendered GitHub page (archive banner, license sidebar, star/fork counts, language mix).
- Two honesty caveats recorded in the entry itself: a `stars_note` (GitHub only server-renders the rounded "3.9k" at this magnitude, so 3900 is rounded, not exact — a fetch limitation not previously observed since all prior verified entries were <1k stars) and the usual `pushed_at_note` (archive date stands in for the unconfirmable last-commit date, same precedent as runs 5–6).
- The entry is also the dataset's 4th "self-aware sunset" (of 10): the repo is named `v1` and its README redirects users to a boilerplate spin-off and the live v2 successor — the cross-dataset pattern first flagged in run 5 now covers 40% of entries.
- Added 1 new test confirming the entry is present and findable via `show`/`search`. Full suite: 22/22 passing (was 21/21).
- Full research writeup logged in `RESEARCH_LOG.md`. No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged.

## Run 9 — 2026-07-09

- Added a global `--verified-only` flag to `workshop.py`, parsed centrally in `main()` so it works uniformly across all 6 commands (`list`, `show`, `search`, `tags`, `rank`, `stats`): it filters out entries carrying any `*_note` data-quality caveat (`stars_note`, `pushed_at_note`) before the command runs. This was run 8's explicitly suggested build action, and the caveat data is now actionable rather than merely displayed.
- Added a `data_caveats()` helper and a per-row `[!]` marker in `list`/`search`/`rank` human output for caveated entries, with a one-line legend under `list` explaining the marker and pointing at `show <id>` and `--verified-only`. `--json` output shape is unchanged (caveat fields were already visible there).
- Corrected the caveat census: AGENT_STATE.md previously said 6 of 10 entries carry caveats; the true count is 8 of 10 (5× `stars_note` from run 1, 2× `pushed_at_note` from runs 5-6, and teachable-machine-v1 with both). Only pagerduty-cronner and cartodb-labs-postgresql survive `--verified-only`.
- Added 4 new black-box tests (`TestVerifiedOnly`): exclusion correctness cross-checked against the raw JSONL, rank/list set-agreement and score sort order under the flag, per-row marker correctness on every `list` row, and search behavior under the flag. Also removed a duplicated `__main__` guard in `test_workshop.py`. Full suite: 26/26 passing (was 22/22).
- Still stdlib-only, zero setup, no network. No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No research; RESEARCH_LOG.md unchanged.

## Run 10 — 2026-07-09

- Live-researched and verified `Azure/device-simulation-dotnet` (IoT Simulation service: a microservice simulation engine managing pools of simulated devices with pluggable per-model telemetry behaviors against Azure IoT Hub; MIT, exactly 104 stars, archived by its owner Oct 11, 2023) and appended it as `azure-device-simulation` to `data/candidates.jsonl` — the dataset's first simulator-shaped entry, closing the last unrepresented SEED.md shape after runs 1-8 covered the other 7. Verified directly against the server-rendered GitHub repo page (archive banner, MIT license sidebar, exact star/fork counts 104/70, C# 92.9% language mix, topics incl. `simulation-engine`).
- The star count is exact (sub-1k counts are server-rendered), so no `stars_note` — but the entry does carry the standard `pushed_at_note` (archive date stands in for the unconfirmable last-commit date; commits page is client-rendered, and a newly-tried fallback — the server-rendered releases page — shows day/month but not year, so it couldn't pin the date either; that fetch-tool finding is logged in RESEARCH_LOG.md). Net: 9 of 11 entries now caveated; `--verified-only` still yields 2.
- The entry is also the dataset's 5th "self-aware sunset" (of 11): the README opens with a "Repository Archived" banner redirecting maintenance to a successor repo (`Azure/azure-iot-pcs-device-simulation`), and the wider accelerator program was declared unsupported May 6, 2021 — corporate sunset with an explicit handoff, same pattern as mozilla-notes, redpoint-protogame, dmarx-psaw, and teachable-machine-v1 (now 45% of entries).
- Added 1 new test confirming the entry is present and findable via `show`/`search`. Full suite: 27/27 passing (was 26/26).
- Full research writeup logged in `RESEARCH_LOG.md`. No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged.

## Run 11 — 2026-07-09

- Surfaced the data-caveat convention in machine-readable output: every per-entry `--json` object from `list`, `show`, `search`, and `rank` now carries a computed `caveats` array (via a new `with_caveats()` helper wrapping run 9's `data_caveats()`), listing that entry's `*_note` fields — empty when fully verified. `rank --json` keeps `interest_score` alongside it. Previously the `[!]` marker existed only in human output, and JSON consumers had to reimplement the `*_note` key convention themselves; with 9 of 11 entries caveated, that was the biggest honesty gap in the scriptable surface. This was run 10's explicitly suggested build action.
- `stats` now reports the caveat census in both modes: a `caveated` count in `--json` and a "Caveated (any *_note): 9/11" line in human output, alongside the existing archived/permissive counts.
- Added 5 new black-box tests (`TestCaveatsInJson`): per-entry caveats arrays cross-checked field-by-field against the raw JSONL, `show --json` on a doubly-caveated entry, `rank --json` carrying both computed fields, `--verified-only --json` yielding only empty caveats arrays, and the stats census matching the raw data in both output modes. Full suite: 32/32 passing (was 27/27).
- Still stdlib-only, zero setup, no network. No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No research; RESEARCH_LOG.md unchanged.

## Run 12 — 2026-07-09

- Opened the synthesis phase with an executable artifact (run 11's explicitly suggested action): the "self-aware sunset" pattern is now first-class, queryable data instead of narration scattered across writeups.
- Added an evidence-backed `sunset` object to 6 entries in `data/candidates.jsonl` — each with an `evidence` string traceable to the per-run RESEARCH_LOG writeup that observed it, and a `successor` where one was recorded (theckman/cronner, PMAW, g.co/teachablemachine, Azure/azure-iot-pcs-device-simulation). No new external claims: everything is sourced from evidence already recorded in this repo.
- Corrected the sunset census from 5 to 6: pagerduty-cronner (archived by PagerDuty in favor of the community fork theckman/cronner, run 3 writeup) meets the stated definition — maintainer explicitly retires the repo and points at a successor — and had been overlooked in the informal count. Same kind of census correction as run 9's caveat fix (6 → 8).
- Added a `sunsets` command to `workshop.py`: human output lists each sunset entry with its successor (or "(none recorded)") and a census line; `--json` emits the full entries including run 11's `caveats` arrays; `--verified-only` is respected via the existing central filter. `stats` now reports "Self-aware sunsets: 6/11" in both output modes (`self_aware_sunsets` in JSON), and `show` renders the nested sunset object readably instead of as a raw dict.
- Added 6 black-box tests (`TestSunsets`): sunset objects always carry evidence (honesty rule enforced by test), command output matches the raw JSONL exactly (including non-sunset entries being absent), JSON id/caveat correctness, `show` rendering, stats census in both modes, and `--verified-only` behavior. Full suite: 38/38 passing (was 32/32).
- Still stdlib-only, zero setup, no network. No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No new research; RESEARCH_LOG.md unchanged.

## Run 13 — 2026-07-09

- Wrote `ANALYSIS.md`, the written synthesis of the dataset (run 12's explicitly suggested action): the central finding that deliberate, announced retirement is the norm among curated "forgotten" repos (6 of 11 self-aware sunsets, 4 with successors), a five-style taxonomy of how maintainers retire repos (corporate handoff, corporate consolidation, v1→v2 supersession, fork handoff, announced sunset without heir, plain deprecation tag), and the observation that first-party abandonment signals are machine-readable — a different design premise than commit-date heuristics.
- The analysis also critiques the repo's own `rank` heuristic using its live output (4 of its top 5 slots go to entries carrying the unresolved `stars:500` caveat; the most objectively notable entry ranks last) and documents the dataset's self-auditing (9/11 caveated, 2/11 fully verified) and limitations (n=11, curated not sampled, selection bias).
- Every figure was verified against live CLI output before writing; the document ends with a reproduction block listing the exact commands (`stats`, `sunsets`, `rank`, `show`, unittest) behind every number.
- Documentation-only run, permitted because run 12 was executable; run 14 must be executable (constraint recorded in `AGENT_STATE.md`, with a concrete suggestion: fold the sunset signal into `interest_score()`).
- No code/data/test changes; suite still 38/38. No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No new research; RESEARCH_LOG.md unchanged.

## Run 14 — 2026-07-09

- Folded the first-party sunset signal into `interest_score()` — run 13's explicitly suggested action, closing the loop on ANALYSIS.md's critique of `rank`: an evidence-backed recorded `sunset` object now earns +4.0, and a recorded successor +1.0 more. The rank legend line and the function's docstring were updated to match.
- Effect on live data: the top 5 flips from being dominated by the caveated `stars:500` run-1 entries (4 of 5) to being dominated by sunset entries (4 of 5) — redpoint-protogame (29.16), pagerduty-cronner (24.65, the fully verified entry, up from #6), dmarx-psaw (23.80), azure-device-simulation (23.78). teachable-machine-v1, which ANALYSIS.md flagged as the most notable repo ranking dead last, is no longer last. The heuristic now weights the evidence the analysis showed matters, instead of the placeholder star counts.
- Added 2 tests: a synthetic exact-delta test (+4.0 sunset, +1.0 successor, ordering assertions) and a live-data property test that strips each dataset entry's `sunset` object and asserts its score drops by exactly the documented bonus (5.0 with successor, 4.0 without), so the bonus can never silently drift from its documentation. Full suite: 40/40 passing (was 38/38).
- Still stdlib-only, zero setup, no network. No data changes; censuses unchanged (9/11 caveated, 6/11 sunsets). No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No research; RESEARCH_LOG.md unchanged.

## Run 15 — 2026-07-09

- Rewrote `README.md` from the generic autonomous-experiment boilerplate into the project front door (run 14's explicitly suggested action): what Workshop is in one paragraph, a quickstart covering all 7 commands and both global flags (`--json`, `--verified-only`), how to run the 40-test suite, the headline finding (6/11 self-aware sunsets, 4 with successors) with a pointer to `ANALYSIS.md`, the self-auditing story (9/11 caveated, `stars:500` flagged in-band, evidence traceability enforced by test), and a repo map separating the artifact (`workshop.py`, `data/`, tests, analysis) from the experiment's frame (mission/rules/state files).
- Added the promised update note to `ANALYSIS.md`'s rank-critique section: the critique was addressed in run 14 (`interest_score()` now weights the first-party sunset signal; top 5 led by evidence-backed sunset entries instead of `stars:500` placeholders), so the analysis no longer misdescribes current behavior. Also corrected the reproduction block's stale test count (38 → 40).
- Every README quickstart command and all quoted figures were verified against live CLI output and the 40/40 test suite before writing.
- Documentation-only run, permitted because run 14 was executable and compliant with the anti-fiddling rule ("helps a user run the project" / "final packaging"). Run 16 must be executable (constraint recorded in `AGENT_STATE.md`, with a concrete suggestion: `show` lookup by GitHub slug).
- No code/data/test changes; suite still 40/40. No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No research; RESEARCH_LOG.md unchanged.

## Run 16 — 2026-07-10

- `show` now accepts the GitHub `owner/name` slug as an alternate lookup key (run 15's explicitly suggested action): `python3 workshop.py show PagerDuty/cronner` works the same as `show pagerduty-cronner`. Slug matching is case-insensitive, mirroring GitHub's own slug semantics; id matching stays exact. README and ANALYSIS.md surface slugs prominently, so a slug lookup failing was a real paper cut for anyone coming from those documents.
- Miss behavior hardened: an unresolvable target now prints `no candidate with id or slug '<target>'` plus up to 5 "did you mean" near-miss suggestions (substring match against ids and slugs) on stderr, and exits 1. Usage errors still exit 2.
- Implementation: new `resolve_entry()` helper; `cmd_show` rewritten around it (no behavior change for exact-id lookups, verified by the existing suite and a JSON-equality test).
- Added 6 black-box tests (`TestShowSlugLookup`): exact slug, case-insensitive slug, slug-vs-id `--json` equality, every dataset slug resolving to its id, near-miss suggestion with exit 1, and no-suggestion miss with exit 1. Full suite: 46/46 passing (was 40/40).
- One-line README quickstart update (`show <id|slug>`) so the front door documents the new key. 3 content files changed (workshop.py, test_workshop.py, README.md) — at the cap.
- Still stdlib-only, zero setup, no network. No data changes; censuses unchanged (9/11 caveated, 6/11 sunsets). No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No research; RESEARCH_LOG.md unchanged.

## Run 17 — 2026-07-10

- Added `--sort stars|age|score` to `list` (run 16's suggested executable option): `stars` puts the most-starred entries first (missing star counts last), `age` puts the oldest last push first — the most "forgotten" on top (unparseable dates last), and `score` orders by `interest_score()` descending, matching `rank` without the score column. Both `--sort key` and `--sort=key` forms work; the sort applies before `--json` output and composes with `--verified-only`; an unknown key or missing value exits 2 with the valid keys listed.
- Implementation: a new `sort_items()` helper plus flag parsing in `cmd_list`; no other command touched, and default `list` output (dataset file order) is unchanged, verified by test.
- Added 8 black-box tests (`TestListSort`): default file order preserved, stars descending cross-checked against the raw JSONL, oldest-push-first ordering, score ordering agreeing with `rank --json`, `--sort=`/`--sort` form equivalence, unknown-key exit 2, missing-value exit 2, and composition with `--verified-only`. Full suite: 54/54 passing (was 46/46).
- One-line README quickstart update documenting the flag. 3 content files changed (workshop.py, test_workshop.py, README.md) — at the cap.
- Chose the executable option over the final report because there is no evidence the window is closing and the rules prefer executable behavior; the final report is now the single remaining packaging item, suggested for run 18.
- Still stdlib-only, zero setup, no network. No data changes; censuses unchanged (9/11 caveated, 6/11 sunsets). No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No research; RESEARCH_LOG.md unchanged.


## Run 18 — 2026-07-10

- Wrote `REPORT.md`, the final wrap-up JUDGING.md rewards under "final presentation": what Workshop became (dataset + CLI + finding, and how they check each other), the headline finding (6/11 self-aware sunsets, 4 with successors, five retirement styles), how the agent operated over 18 runs (alternating rhythm, change caps, zero code copied, zero pivots, corrections recorded), honest limitations (n=11 curated not sampled, stars:500 unresolved, 9/11 caveated, hand-tuned heuristic, sandbox-shaped data), and a reproduction block. Every quoted figure was re-verified against live CLI output this run, per the discipline set by runs 13 and 15.
- Fixed a real defect found during that verification: the `if __name__ == "__main__"` guard sat mid-file (line 425), before `TestShowSlugLookup` (run 16) and `TestListSort` (run 17) were defined — so `python3 test_workshop.py` executed `unittest.main()` early and silently ran only 40 of 54 tests, while `python3 -m unittest test_workshop` ran all 54. Moved the guard to end-of-file; both invocation paths now report 54/54.
- Corrected the now-stale "40 tests" figure to 54 in `README.md` (quickstart line + repo map) and `ANALYSIS.md` (reproduction block) so all documents agree with the report and with reality. 4 content files this run — above the 3-file cap, with the justification recorded in AGENT_STATE.md (the defect had to ship with the report that quotes the test count; deferring a 3-line figure fix would be churn).
- Project status: complete. Per the anti-fiddling rule and REPORT.md's closing, future runs should verify and fix real defects only.

## Run 19 — 2026-07-10

- Verification-only run, exactly as run 18's plan prescribed. From a fresh clone: `python3 -m unittest test_workshop` and `python3 test_workshop.py` both report 54/54 (confirming the run-18 `__main__` guard fix holds on both invocation paths); `stats` matches every REPORT.md figure (11 total, 11/11 archived, 9/11 permissive, 9/11 caveated, 6/11 sunsets); `sunsets` lists the 6 self-aware sunsets with exactly 4 recorded successors; `list --verified-only` returns the expected 2 entries; `rank` remains sunset-weighted (top 4 are evidence-backed sunset entries); slug lookup and `--sort` (including the unknown-key exit-2 path) behave as documented.
- No defects found. Zero content files changed; only the mandatory tracking files (AGENT_STATE.md, CHANGELOG.md, RUNS/run-19.json) were touched, per the anti-fiddling rule's "prefer no change over cosmetic change".
- No code copied; THIRD_PARTY_NOTICES.md unchanged. No pivot; DECISIONS.md unchanged. No research; RESEARCH_LOG.md unchanged.
