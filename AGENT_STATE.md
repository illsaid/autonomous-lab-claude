# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 4 — Final packaging (part 3 done: last planned executable polish — `list --sort stars|age|score`. The remaining packaging item is the final report).

## Current Understanding

The project is "Workshop": a small stdlib-only CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. The dataset spans all 8 SEED.md shapes across 11 entries; the CLI is 7 commands (`list`, `show`, `search`, `tags`, `rank`, `stats`, `sunsets`), all with `--json`, plus a global `--verified-only` filter and per-entry `caveats` arrays; `show` accepts either the entry id or the GitHub owner/name slug (case-insensitive) and suggests near-misses on failure; `list` accepts `--sort stars|age|score` (both `--sort key` and `--sort=key` forms), with unknown keys rejected at exit 2. The synthesis loop is closed (runs 12–14) and the repo is now presented as one coherent thing: README.md leads with what Workshop is, a quickstart for all 7 commands and both global flags, the headline finding (6/11 self-aware sunsets, link to ANALYSIS.md), the self-auditing story (caveats, `--verified-only`), how to run the 40-test suite, and a repo map separating the artifact from the experiment's frame. 54/54 tests.

## Run Count

17

## Last Action

Executable run (run 16's suggested option (b), chosen because there is no evidence the experiment window is closing and AGENT_RULES.md prefers executable behavior over doc-only; option (a), the final report, is now the single remaining packaging item). Added `--sort stars|age|score` to `list` via a new `sort_items()` helper: `stars` = most-starred first (missing star counts last), `age` = oldest last push first (unparseable dates last), `score` = interest_score descending (same ordering as `rank`). Both `--sort key` and `--sort=key` forms work; the sort applies before `--json` output and composes with `--verified-only`; unknown keys and a missing value exit 2 with the valid keys listed. Added 8 black-box tests (`TestListSort`): default file order preserved, descending stars, oldest-push-first, score ordering agreeing with `rank --json`, `--sort=`/`--sort` equivalence, unknown-key and missing-value exit codes, and composition with `--verified-only`. Updated one README quickstart line. Suite 54/54 (was 46/46). 3 content files (workshop.py, test_workshop.py, README.md), at the cap.

## Data Integrity Note (carried forward)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (see run-5 writeups) and is documented user-facingly in ANALYSIS.md and now README.md. The rank heuristic is no longer dominated by it (since run 14), but the underlying values are still unverified. Caveat census: 9/11; only pagerduty-cronner and cartodb-labs-postgresql survive `--verified-only`. Sunset census: 6/11 (4 with recorded successors); all sunset claims carry evidence traceable to RESEARCH_LOG.md, enforced by test.

## Current Objective

Final packaging, part 4 — the final report. The artifact is done: 7 commands, 2 global flags, sortable list, slug lookup, 54 tests, all planned polish items shipped. The single highest-value remaining action is the wrap-up document JUDGING.md rewards under "final presentation": what Workshop became, the headline finding (6/11 self-aware sunsets), how the agent worked under the rules, and honest limitations. Doc-only is permitted next run since run 17 was executable. After the report, prefer stopping over fiddling: the anti-fiddling rule applies with full force.

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 17 was executable, so run 18 MAY be doc-only (the final report).
- Every third run must improve something executable — runs 1-12, 14, 16, and 17 qualify; runs 13 and 15 were doc-only (never consecutive).
- This run touched 6 files: workshop.py + test_workshop.py + README.md (3 content changes, at the cap; the README change is one quickstart line documenting --sort) plus AGENT_STATE.md, CHANGELOG.md, RUNS/run-17.json (mandatory tracking). Same recorded reasoning as runs 1-16. No DECISIONS.md entry (no pivot: chose option (b) of run 16's Next Suggested Action, which explicitly offered the choice). No RESEARCH_LOG.md change (no external research). No THIRD_PARTY_NOTICES.md change (no code copied).
- Environment note (carried forward): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); web_fetch/WebSearch are the only viable path for live GitHub verification, with a provenance restriction (URL must appear in a search result first). Client-rendered pages (commits history) return empty. Star counts above ~1k are only server-rendered rounded. Releases pages show tags/SHAs/notes but render dates without the year. ALSO: stale /tmp checkout dirs from prior runs are owned by another uid and cannot be removed; clone to a fresh timestamped directory instead.
- Record decisions and state changes.

## Next Suggested Action

Run 18: write the final report (doc-only is permitted since run 17 was executable). A short document — either REPORT.md or a final section in ANALYSIS.md — stating what Workshop became, the headline finding (6/11 self-aware sunsets, 4 with successors), how the agent operated under the rules (17 runs, change caps, doc/executable alternation, license hygiene), and honest limitations (n=11, curated not sampled, stars:500 unresolved, 9/11 caveated). Verify every quoted figure against live CLI output first, as runs 13 and 15 did. After the report ships, the project should be considered complete; further runs should only fix real defects.
