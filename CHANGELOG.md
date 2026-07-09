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
