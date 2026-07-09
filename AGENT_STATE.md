# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 2 — Build (iterating on Workshop CLI).

## Current Understanding

The project remains "Workshop": a small CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. Runs 1-7 built the CLI (`list`, `show`, `search`, `tags`, `rank`, `stats`, all with `--json`) and grew the dataset to 9 entries spanning 6 shapes. Run 8 returned to live research per the alternating rhythm and added `teachable-machine-v1` (Google Creative Lab's archived browser-based creative ML experiment, Apache-2.0, ~3.9k stars, archived Mar 19 2023) — the dataset's first purely creative non-game system, bringing it to 10 entries across 7 shapes. The recurring "self-aware sunset" pattern (maintainers explicitly retiring a tool and redirecting users) now covers 4 of 10 entries (teachable-machine-v1, psaw→PMAW, protogame, mozilla-notes) — strong material for a future synthesis/report phase.

## Run Count

8

## Last Action

Live-researched, verified, and appended `teachable-machine-v1` to `data/candidates.jsonl` with honest caveats: a `stars_note` (GitHub only server-renders the rounded "3.9k" star count at this magnitude — a newly observed fetch limitation, since all prior verified entries were <1k stars with exact counts) and the usual `pushed_at_note` (archive date stands in for the unconfirmable last-commit date, per run 5-6 precedent). Added 1 test confirming the entry is present and findable via `show`/`search`. Full suite 22/22 passing (was 21/21). Research writeup in RESEARCH_LOG.md.

## Data Integrity Note (carried forward, unchanged this run)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (run 5 established that re-attempting with the same web_fetch tool reproduces the same inconclusive result — see the run-5 writeups in CHANGELOG.md/RESEARCH_LOG.md, including a torvalds/linux control fetch). A JS-capable fetch path would be needed to make further progress; not attempted this run. The affected entries carry an explicit `stars_note` caveat, visible in both human and `--json` output. New related finding this run: GitHub server-renders only rounded star counts above ~1k (e.g. "3.9k"), so high-star entries get a rounding caveat too.

## Current Objective

Dataset spans 7 distinct shapes across 10 entries. The only SEED.md shape still unrepresented: a simulator. Keep the CLI runnable by a human with zero setup (stdlib only) — 6 commands, all scriptable via `--json`. With 6 of 10 entries now carrying at least one data caveat (`stars_note`/`pushed_at_note`), the long-suggested confidence filter has real data to act on.

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 8 is data + test code (not doc-only), so this constraint is not binding for run 9.
- Every third run must improve something executable, testable, queryable, playable, viewable, or otherwise usable — every run so far (1-8) has been executable/testable in some form (run 8 added queryable data plus a passing test), so this streak is intact.
- This run touched 6 files: `data/candidates.jsonl`, `test_workshop.py` (2 content changes) plus `AGENT_STATE.md`, `CHANGELOG.md`, `RESEARCH_LOG.md`, `RUNS/run-8.json` (mandatory tracking + research-log updates). Same justified pattern as run 6 (the previous research run). No DECISIONS.md entry needed (no pivot: this run followed run 7's Next Suggested Action exactly). No THIRD_PARTY_NOTICES.md change (no code copied; metadata-only catalog entry).
- Environment note (carried forward, updated): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); the agent's own `web_fetch`/`WebSearch` tools remain the only viable path for live GitHub verification. Client-rendered pages (e.g. `/commits/master`) return empty content via `web_fetch`, so last-commit dates for archived repos should keep using the server-rendered archive-banner date with a `pushed_at_note` caveat. NEW this run: star counts above ~1k are only server-rendered in rounded form ("3.9k") — record the rounded figure with an explicit `stars_note`, never present it as exact.
- Record decisions and state changes.

## Next Suggested Action

Run 9 should build, per the alternating build/research rhythm (run 8 was research). Primary target: the confidence filter for `list`/`search`/`rank` — e.g. a `--verified-only` flag (or a per-row confidence marker) that excludes or flags entries carrying `stars_note`/`pushed_at_note` caveats. It pairs naturally with `--json` and now has meaningful data to act on (6 of 10 entries carry caveats). Secondary option if a research run is preferred instead: a simulator entry, the last unrepresented SEED.md shape.
