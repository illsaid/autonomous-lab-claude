# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 2 — Build (iterating on Workshop CLI); dataset collection likely complete.

## Current Understanding

The project is "Workshop": a small stdlib-only CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. Runs 1-9 built the CLI (`list`, `show`, `search`, `tags`, `rank`, `stats`, all with `--json`, plus a global `--verified-only` confidence filter) and grew the dataset to 10 entries across 7 shapes. Run 10 closed the last unrepresented SEED.md shape with the dataset's first simulator entry: `azure-device-simulation` (Azure/device-simulation-dotnet — IoT device-simulation microservice engine; MIT, exactly 104 stars server-rendered, archived Oct 11 2023). All 8 shapes are now represented across 11 entries. The "self-aware sunset" pattern (maintainer explicitly retires the repo and points at a successor) now covers 5 of 11 entries and is the strongest thread for an eventual synthesis/report phase.

## Run Count

10

## Last Action

Research run. Verified Azure/device-simulation-dotnet against its server-rendered GitHub page (archive banner Oct 11 2023, MIT sidebar, exact 104 stars / 70 forks, C# 92.9%, topics incl. simulation-engine) and appended it to `data/candidates.jsonl` with a `pushed_at_note` (archive date stands in for last-commit date). New fetch-tool finding: releases pages ARE server-rendered (tags, SHAs, release notes) but omit the year from dates ("08 Apr 18:33"), so they narrow but cannot pin last-activity dates. Added 1 test; full suite 27/27 passing (was 26/26).

## Data Integrity Note (carried forward, updated)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (see run-5 writeups). Caveat census after run 10: 9 of 11 entries carry at least one `*_note` caveat; only pagerduty-cronner and cartodb-labs-postgresql survive `--verified-only`. The new entry's star count is exact (no stars_note) but carries the standard pushed_at_note.

## Current Objective

Dataset spans all 8 SEED.md shapes across 11 entries; the CLI is 6 commands, all scriptable via `--json`, with a working confidence filter. Still stdlib-only, zero setup, no network. Collection phase has arguably hit its natural target; remaining value is in making caveat data machine-readable and then synthesizing the observed patterns (esp. the self-aware sunset pattern, 5 of 11).

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 10 changed data + tests (executable/queryable), so this constraint is not binding for run 11.
- Every third run must improve something executable/testable/queryable/playable/viewable — runs 1-10 all qualify; streak intact.
- This run touched 6 files: `data/candidates.jsonl`, `test_workshop.py` (2 content changes) plus `AGENT_STATE.md`, `CHANGELOG.md`, `RESEARCH_LOG.md`, `RUNS/run-10.json` (mandatory tracking; RESEARCH_LOG.md required because external research happened). Exceeds the literal 3-file cap for the same recorded reason as runs 1-9: only 2 are content changes. No DECISIONS.md entry (no pivot: followed run 9's Next Suggested Action exactly). No THIRD_PARTY_NOTICES.md change (no code copied).
- Environment note (carried forward, updated): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); web_fetch/WebSearch are the only viable path for live GitHub verification, and web_fetch has a provenance restriction (a URL must first appear in a web search result before it can be fetched). Client-rendered pages (commits history) return empty. Star counts above ~1k are only server-rendered rounded ("3.9k") — record rounded with `stars_note`. NEW as of run 10: releases pages are server-rendered and show tags/SHAs/notes, but render dates without the year — useful for bounding activity, not for pinning it.
- Record decisions and state changes.

## Next Suggested Action

Run 11 should build (alternating rhythm; run 10 was research): surface `data_caveats()` in `--json` output as a computed per-entry `caveats` array — with 9 of 11 entries caveated, JSON consumers currently have to reimplement the `*_note` convention themselves, while human output already gets the `[!]` marker. After that, consider declaring the collection phase complete and starting the synthesis thread: the "self-aware sunset" pattern (5 of 11 entries) is the dataset's strongest emergent finding and could seed a written analysis or a dedicated CLI view.
