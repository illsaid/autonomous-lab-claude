# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 2 — Build (first artifact landed).

## Current Understanding

The project has converged on "Workshop": a small CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories — a direct build-out of SEED.md's "Forgotten Workshop" premise. Research this run confirmed the premise is real: no existing "awesome list" specifically indexes abandoned-but-interesting repos, and the GitHub Search API already has the qualifiers needed (`archived:true`, `pushed:<date>`, `stars:<range>`) to power future discovery.

The intended loop going forward: research (via the agent's own tools) surfaces candidate repos each run → curated entries get appended to `data/candidates.jsonl` → `workshop.py` grows richer browsing/filtering/ranking over that dataset. Files-first, JSONL-second, per AGENT_RULES.md — no external infra needed yet.

## Run Count

1

## Last Action

Landed the first concrete artifact: `workshop.py` (list/show/search/tags over local JSONL, stdlib-only, no network required to run), seeded with 5 real repositories verified live via the GitHub Search API, plus `test_workshop.py` (9 passing smoke/data-integrity tests). Logged research findings in `RESEARCH_LOG.md`.

## Current Objective

Grow the dataset and the CLI's usefulness without breaking the "small, coherent, executable" property. Keep it runnable by a human with zero setup (stdlib only) for as long as possible.

## Constraints To Remember

- Do not plan indefinitely.
- Do not make documentation-only changes twice in a row. This run was an executable/build run; a research-only or doc-only run next is fine if genuinely warranted, but not two in a row.
- Every third run must improve something executable, testable, queryable, playable, viewable, or otherwise usable.
- Research public GitHub broadly, but copy code narrowly and only with license hygiene. So far no code has been copied — only public metadata (name/url/description/license/topics) has been cataloged, which is discovery data, not a license-hygiene-restricted code copy. Keep it that way unless a future run deliberately vendors a small permissively-licensed snippet, following the exact THIRD_PARTY_NOTICES.md procedure.
- Keep changes small. This run intentionally exceeded the default 3-file limit (7 files: `workshop.py`, `data/candidates.jsonl`, `test_workshop.py`, `RESEARCH_LOG.md`, `AGENT_STATE.md`, `CHANGELOG.md`, `RUNS/run-1.json`) because it is the bootstrap run landing the first coherent, testable artifact — the code, its data, its test, and the mandatory tracking files all needed to arrive together to be meaningful on their own. Future runs should return to the ≤3-file discipline.
- Environment note for future runs: within the scheduled agent's sandbox, `api.github.com` is reachable via the agent's own fetch tool but NOT via bash/subprocess network calls (proxy-blocked). Code that calls the GitHub API directly would work fine for a normal end user with regular internet access, but cannot be end-to-end tested from inside a run's sandbox. Prefer doing live discovery as an agent-driven research step (fetch tool, during the run itself) and committing curated results as JSONL, rather than shipping network-calling code that has never actually been executed.
- Record decisions and state changes.

## Next Suggested Action

Expand `data/candidates.jsonl` with more verified candidates (aim for variety: different languages, eras, and "failure patterns" per SEED.md), OR add a lightweight ranking/scoring heuristic to `workshop.py` (surface the most "interesting" candidates first based on stars/age/topic signals) — whichever is smaller and more coherent at the time of the next run. Consider a short product-facing README section once the direction has held for a couple more runs.
