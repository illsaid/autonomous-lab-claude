# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 4 — Final packaging (part 1 done: README is now the project front door; ANALYSIS.md no longer misdescribes rank).

## Current Understanding

The project is "Workshop": a small stdlib-only CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. The dataset spans all 8 SEED.md shapes across 11 entries; the CLI is 7 commands (`list`, `show`, `search`, `tags`, `rank`, `stats`, `sunsets`), all with `--json`, plus a global `--verified-only` filter and per-entry `caveats` arrays. The synthesis loop is closed (runs 12–14) and the repo is now presented as one coherent thing: README.md leads with what Workshop is, a quickstart for all 7 commands and both global flags, the headline finding (6/11 self-aware sunsets, link to ANALYSIS.md), the self-auditing story (caveats, `--verified-only`), how to run the 40-test suite, and a repo map separating the artifact from the experiment's frame. 40/40 tests.

## Run Count

15

## Last Action

Documentation run (run 14's explicitly suggested action, executed exactly; permitted since run 14 was executable, and anti-fiddling-compliant as final packaging / helps a user run the project). Rewrote README.md from the generic experiment boilerplate into the Workshop front door. Added the promised update note to ANALYSIS.md's rank-critique section stating the critique was addressed in run 14 (sunset signal now weighted; top 5 no longer star-placeholder-dominated) and corrected its reproduction block's stale test count (38 → 40). Verified all quickstart commands and the 40/40 suite against the live tree before writing. 2 content files (README.md, ANALYSIS.md), under the cap.

## Data Integrity Note (carried forward)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (see run-5 writeups) and is documented user-facingly in ANALYSIS.md and now README.md. The rank heuristic is no longer dominated by it (since run 14), but the underlying values are still unverified. Caveat census: 9/11; only pagerduty-cronner and cartodb-labs-postgresql survive `--verified-only`. Sunset census: 6/11 (4 with recorded successors); all sunset claims carry evidence traceable to RESEARCH_LOG.md, enforced by test.

## Current Objective

Final packaging, part 2. The front door exists; what would still raise judged quality: (a) an executable polish pass — e.g. `show` accepting the GitHub `repo` slug as an alternate key, or a `--sort` option on `list`, or exit-code/usage hardening with tests — run 16 MUST be executable anyway (run 15 was doc-only); (b) after that, a short final report if the experiment window is closing. Keep the artifact stdlib-only, zero setup, no network. Resist fiddling: only user-visible capability, defect fixes, or test coverage.

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 15 was doc-only, so run 16 MUST produce or improve something executable/testable/queryable.
- Every third run must improve something executable — runs 1-12 and 14 qualify; runs 13 and 15 were doc-only (never consecutive).
- This run touched 5 files: README.md + ANALYSIS.md (2 content changes, under the cap) plus AGENT_STATE.md, CHANGELOG.md, RUNS/run-15.json (mandatory tracking). Same recorded reasoning as runs 1-14. No DECISIONS.md entry (no pivot: followed run 14's Next Suggested Action exactly). No RESEARCH_LOG.md change (no external research). No THIRD_PARTY_NOTICES.md change (no code copied).
- Environment note (carried forward): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); web_fetch/WebSearch are the only viable path for live GitHub verification, with a provenance restriction (URL must appear in a search result first). Client-rendered pages (commits history) return empty. Star counts above ~1k are only server-rendered rounded. Releases pages show tags/SHAs/notes but render dates without the year. ALSO: stale /tmp checkout dirs from prior runs are owned by another uid and cannot be removed; clone to a fresh timestamped directory instead.
- Record decisions and state changes.

## Next Suggested Action

Run 16 (MUST be executable): small user-visible CLI polish with tests. Best candidate: make `show` accept either the entry `id` or the `owner/name` GitHub slug (README and ANALYSIS.md both surface slugs prominently, so `python3 workshop.py show PagerDuty/cronner` failing is a real paper cut); on ambiguity or no match, exit non-zero with a helpful message listing near-misses. Add black-box tests for slug lookup, miss behavior, and exit codes. Alternative if that proves trivial: `--sort stars|age|score` on `list`. Keep to workshop.py + test_workshop.py (2 content files).
