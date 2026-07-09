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
