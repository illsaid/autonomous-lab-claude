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
