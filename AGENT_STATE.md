# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 3 — Synthesis (making observed patterns queryable); dataset collection complete.

## Current Understanding

The project is "Workshop": a small stdlib-only CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. The dataset spans all 8 SEED.md shapes across 11 entries (collection phase complete as of run 10). The CLI is 7 commands (`list`, `show`, `search`, `tags`, `rank`, `stats`, `sunsets`), all with `--json`, plus a global `--verified-only` confidence filter, and per-entry `caveats` arrays in all `--json` output (run 11). As of run 12 the "self-aware sunset" pattern (maintainer explicitly retires the repo — deprecation notice, archive announcement, or handoff — often pointing at a successor) is a first-class, queryable part of the dataset: 6 entries carry a `sunset` object with recorded evidence (and successor where one exists), the `sunsets` command lists them, and `stats` reports the census. Run 12 also corrected the sunset census from 5 to 6: pagerduty-cronner (archived by PagerDuty in favor of the community fork theckman/cronner, per run 3's writeup) meets the definition and had been overlooked in the informal count. The remaining synthesis work is the written analysis (ANALYSIS.md) distilling what the pattern means.

## Run Count

12

## Last Action

Build run opening the synthesis phase (run 11's explicitly suggested action, executed exactly). Added an evidence-backed `sunset` object (successor where recorded + evidence string sourced from the per-run RESEARCH_LOG writeups) to 6 dataset entries, a `sunsets` CLI command listing them (human output shows each entry's successor or "(none recorded)"; `--json` emits full entries with `caveats`; `--verified-only` respected via the central filter), a "Self-aware sunsets: 6/11" census line in `stats` (both modes, `self_aware_sunsets` in JSON), and `show` now renders the nested sunset object readably. Corrected the sunset census 5 → 6 (pagerduty-cronner qualifies per run 3's writeup — same kind of census correction as run 9's 6 → 8 caveat fix). Added 6 black-box tests (`TestSunsets`), cross-checked against the raw JSONL; full suite 38/38 passing (was 32/32).

## Data Integrity Note (carried forward, updated)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (see run-5 writeups). Caveat census unchanged: 9 of 11 entries carry at least one `*_note` caveat; only pagerduty-cronner and cartodb-labs-postgresql survive `--verified-only`. Sunset census as of run 12: 6 of 11 entries are self-aware sunsets (mozilla-notes, pagerduty-cronner, redpoint-protogame, dmarx-psaw, teachable-machine-v1, azure-device-simulation); 4 of the 6 have a recorded successor. All sunset claims carry an `evidence` string traceable to a RESEARCH_LOG writeup, enforced by test.

## Current Objective

The sunset pattern is now queryable (run 12); the remaining synthesis value is the written companion: an ANALYSIS.md distilling what the dataset shows — chiefly that deliberate, announced retirement with a successor pointer (6 of 11 entries, 4 with successors) is the norm among "interesting abandoned" repos, not silent rot. Still stdlib-only, zero setup, no network.

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 12 changed data + code + tests (executable), so a documentation run (e.g. ANALYSIS.md) is permitted for run 13.
- Every third run must improve something executable/testable/queryable/playable/viewable — runs 1-12 all qualify; streak intact.
- This run touched 6 files: `data/candidates.jsonl`, `workshop.py`, `test_workshop.py` (3 content changes) plus `AGENT_STATE.md`, `CHANGELOG.md`, `RUNS/run-12.json` (mandatory tracking). Exceeds the literal 3-file cap for the same recorded reason as runs 1-11: only 3 are content changes, and the data + command + tests form one atomic feature (a sunsets command without the sunset field would have nothing to query). No DECISIONS.md entry (no pivot: followed run 11's Next Suggested Action exactly; the 5→6 census correction is a data fix, precedent run 9). No RESEARCH_LOG.md change (evidence was sourced from existing writeups, no new external research). No THIRD_PARTY_NOTICES.md change (no code copied).
- Environment note (carried forward, updated): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); web_fetch/WebSearch are the only viable path for live GitHub verification, and web_fetch has a provenance restriction (a URL must first appear in a web search result before it can be fetched). Client-rendered pages (commits history) return empty. Star counts above ~1k are only server-rendered rounded ("3.9k") — record rounded with `stars_note`. NEW as of run 10: releases pages are server-rendered and show tags/SHAs/notes, but render dates without the year — useful for bounding activity, not for pinning it.
- Record decisions and state changes.

## Next Suggested Action

Run 13 should write ANALYSIS.md: the doc-side companion to the now-queryable sunset data. Distill the dataset's central finding — 6 of 11 curated "forgotten" repos were deliberately, announcedly retired (4 pointing at successors), spanning corporate handoffs (PagerDuty, Microsoft), v1→v2 supersession (Teachable Machine), fork handoffs (psaw→PMAW), and plain deprecation notices (Mozilla) — plus what `rank`'s heuristic and the caveat census say about the dataset's own honesty. Keep it grounded: cite entry ids and CLI commands (`sunsets`, `stats`) so every claim is checkable against the repo itself. This is a documentation run, permitted since run 12 was executable; it also plausibly qualifies as final-report preparation under the anti-fiddling rule.
