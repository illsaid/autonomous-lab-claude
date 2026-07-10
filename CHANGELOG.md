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
