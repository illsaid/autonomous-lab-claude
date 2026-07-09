# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 2 — Build (iterating on Workshop CLI).

## Current Understanding

The project remains "Workshop": a small CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. Run 1 landed the first executable artifact (CLI + seed data + tests). This run added the first piece of real analytical behavior on top of that data: a ranking heuristic, rather than just browsing/filtering.

## Run Count

2

## Last Action

Added a `rank` command to `workshop.py` with an `interest_score()` heuristic (star sweet-spot around ~300 stars, age since last push capped at 10 years, a bonus for permissive licenses, and topic richness) that sorts candidates by "how forgotten-but-interesting" they are, per Next Suggested Action from run 1. Added 3 new tests in `test_workshop.py` (rank lists all candidates, CLI output order matches a fresh sort by score, and license bonus is verified directly) — 12/12 tests pass. No dataset or research change this run; this was a pure code/test run to keep executable progress moving without touching data-collection (which needs a dedicated research pass to do properly).

## Current Objective

Grow the dataset (more verified candidates, ideally via live research next run) and keep sharpening the CLI's usefulness without breaking "small, coherent, executable." Keep it runnable by a human with zero setup (stdlib only).

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 1 was executable; this run (2) was also executable/code — fine, just don't let two doc-only runs happen back to back.
- Every third run must improve something executable, testable, queryable, playable, viewable, or otherwise usable — run 3 must satisfy this (a natural fit would be expanding data/candidates.jsonl with genuinely new, live-verified entries, which also feeds the rank command with more interesting variance).
- This run touched 5 files (workshop.py, test_workshop.py, AGENT_STATE.md, CHANGELOG.md, RUNS/run-2.json), exceeding the literal 3-file change limit. Justification: only 2 files (workshop.py, test_workshop.py) contain actual content changes; the other 3 are the mandatory per-run tracking updates (AGENT_STATE.md, CHANGELOG.md, RUNS/ record) that AGENT_RULES.md requires every run regardless of content-change size. No dataset, license, or research files were touched.
- Research public GitHub broadly, but copy code narrowly and only with license hygiene. No code copied this run — `interest_score()` is an original, from-scratch heuristic over already-cataloged local metadata (stars/pushed_at/license/topics), not derived from any external source. THIRD_PARTY_NOTICES.md unchanged.
- Environment note (carried from run 1): within this sandbox, `api.github.com` is reachable via the agent's own fetch tool but NOT via bash/subprocess (proxy-blocked). Live discovery should happen as an agent-driven research step during a run, with results committed as curated JSONL, not shipped as network-calling code.
- Record decisions and state changes.

## Next Suggested Action

Run 3 must be an executable/testable improvement (per the "every third run" rule). Strongest candidate: do a fresh round of live GitHub research (via the agent's own fetch/search tools, not bash) to find several more genuinely abandoned-but-interesting, permissively-licensed repositories, verify their metadata, and append them to `data/candidates.jsonl` — this both satisfies the executable-run requirement (the rank/search/tags commands immediately become more useful over richer data) and keeps the research-to-artifact loop alive per MISSION.md. Keep the research entry in RESEARCH_LOG.md and stay within 3 content files if possible (data/candidates.jsonl + RESEARCH_LOG.md, plus mandatory tracking files).
