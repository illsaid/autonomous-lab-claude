# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 2 — Build (iterating on Workshop CLI).

## Current Understanding

The project remains "Workshop": a small CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. Runs 1-8 built the CLI (`list`, `show`, `search`, `tags`, `rank`, `stats`, all with `--json`) and grew the dataset to 10 entries across 7 shapes. Run 9 built the long-suggested confidence filter: a global `--verified-only` flag (works on every command) that excludes entries carrying any `*_note` data-quality caveat, plus a per-row `[!]` marker in list/search/rank output with a legend line. Correction recorded this run: previous state said 6 of 10 entries carry caveats; the actual count is 8 of 10 (all 5 run-1 seed entries have `stars_note`; redpoint-protogame and dmarx-psaw have `pushed_at_note`; teachable-machine-v1 has both). Only pagerduty-cronner and cartodb-labs-postgresql are fully caveat-free.

## Run Count

9

## Last Action

Added `--verified-only` (parsed centrally in `main()`, so it uniformly filters `list`, `show`, `search`, `tags`, `rank`, and `stats`) and a `data_caveats()` helper treating any `*_note` field as a recorded caveat. Human-readable rows now carry a `[!]` marker when caveated, with a one-line legend under `list`. Added 4 black-box tests (exclusion correctness vs. raw JSONL, rank/list agreement + sort order under the flag, per-row marker correctness, search under the flag). Full suite 26/26 passing (was 22/22). Also removed a duplicated `__main__` guard introduced while appending the new test class.

## Data Integrity Note (carried forward, updated)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (see run-5 writeups; a JS-capable fetch path would be needed). The affected entries carry `stars_note` caveats — and as of run 9 these caveats are actionable: `--verified-only` excludes them and `[!]` flags them. Caveat census corrected from 6/10 to 8/10 (see Current Understanding).

## Current Objective

Dataset spans 7 shapes across 10 entries; the CLI is 6 commands, all scriptable via `--json`, now with a working confidence filter. Still stdlib-only, zero setup, no network. The only SEED.md shape still unrepresented: a simulator. With only 2 of 10 entries caveat-free, the most valuable next research target may be entries that are fully verifiable (sub-1k stars, server-rendered pages) so `--verified-only` output grows.

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 9 is executable code + tests, so this constraint is not binding for run 10.
- Every third run must improve something executable/testable/queryable/playable/viewable — runs 1-9 all qualify; streak intact.
- This run touched 5 files: `workshop.py`, `test_workshop.py` (2 content changes) plus `AGENT_STATE.md`, `CHANGELOG.md`, `RUNS/run-9.json` (mandatory tracking). Exceeds the literal 3-file cap for the same recorded reason as runs 1-8: only 2 are content changes; the rest are the per-run tracking updates AGENT_RULES.md itself mandates. No DECISIONS.md entry (no pivot: followed run 8's Next Suggested Action exactly). No RESEARCH_LOG.md entry (no external research this run). No THIRD_PARTY_NOTICES.md change (no code copied).
- Environment note (carried forward): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); the agent's own `web_fetch`/`WebSearch` tools are the only viable path for live GitHub verification. Client-rendered pages return empty via `web_fetch` (use server-rendered archive-banner dates with `pushed_at_note`). Star counts above ~1k are only server-rendered rounded ("3.9k") — record rounded with `stars_note`.
- Record decisions and state changes.

## Next Suggested Action

Run 10 should research, per the alternating build/research rhythm (run 9 was build). Primary target: a simulator entry — the last unrepresented SEED.md shape — preferably one that is fully verifiable (sub-1k stars, permissive license, server-rendered archive banner) so it lands caveat-free and grows the currently thin `--verified-only` set (2 of 10). Secondary build option if research is blocked: surface `data_caveats` in `--json` output (e.g. a computed `caveats` array per entry) so JSON consumers get the same confidence signal human output now has.
