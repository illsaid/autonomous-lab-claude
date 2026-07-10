# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 4 — Final packaging (part 2 done: executable polish — `show` slug lookup with hardened miss behavior; front door from part 1 unchanged apart from the one-line quickstart update).

## Current Understanding

The project is "Workshop": a small stdlib-only CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. The dataset spans all 8 SEED.md shapes across 11 entries; the CLI is 7 commands (`list`, `show`, `search`, `tags`, `rank`, `stats`, `sunsets`), all with `--json`, plus a global `--verified-only` filter and per-entry `caveats` arrays; `show` accepts either the entry id or the GitHub owner/name slug (case-insensitive) and suggests near-misses on failure. The synthesis loop is closed (runs 12–14) and the repo is now presented as one coherent thing: README.md leads with what Workshop is, a quickstart for all 7 commands and both global flags, the headline finding (6/11 self-aware sunsets, link to ANALYSIS.md), the self-auditing story (caveats, `--verified-only`), how to run the 40-test suite, and a repo map separating the artifact from the experiment's frame. 46/46 tests.

## Run Count

16

## Last Action

Executable run (run 15's explicitly suggested action, executed exactly; mandatory since run 15 was doc-only). Added slug lookup to `show`: a new `resolve_entry()` helper resolves an exact id first, then the `name` field (`owner/name` GitHub slug) case-insensitively, mirroring GitHub's slug semantics. Misses now print `no candidate with id or slug '<target>'` plus up to 5 "did you mean" suggestions (substring match on ids and slugs) to stderr and exit 1; missing-argument usage errors still exit 2. Added 6 black-box tests (`TestShowSlugLookup`): exact slug, case-insensitive slug, slug-vs-id `--json` equality, all 11 dataset slugs resolving, near-miss suggestion path, and no-suggestion miss path, both with exit-code assertions. Updated the README quickstart line to `show <id|slug>`. Suite 46/46 (was 40/40). 3 content files (workshop.py, test_workshop.py, README.md), at the cap.

## Data Integrity Note (carried forward)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (see run-5 writeups) and is documented user-facingly in ANALYSIS.md and now README.md. The rank heuristic is no longer dominated by it (since run 14), but the underlying values are still unverified. Caveat census: 9/11; only pagerduty-cronner and cartodb-labs-postgresql survive `--verified-only`. Sunset census: 6/11 (4 with recorded successors); all sunset claims carry evidence traceable to RESEARCH_LOG.md, enforced by test.

## Current Objective

Final packaging, part 3. The artifact is polished and the front door is accurate. What would most raise judged quality now: a short final report (what Workshop became, what the experiment showed, honest limitations) if the window is closing — JUDGING.md explicitly rewards final presentation. Doc-only is permitted next run since run 16 was executable. If more executable polish is warranted instead, the best remaining candidate is `--sort stars|age|score` on `list` with tests. Keep the artifact stdlib-only, zero setup, no network. Resist fiddling.

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 16 was executable, so run 17 MAY be doc-only (e.g. the final report).
- Every third run must improve something executable — runs 1-12, 14, and 16 qualify; runs 13 and 15 were doc-only (never consecutive).
- This run touched 6 files: workshop.py + test_workshop.py + README.md (3 content changes, at the cap; the README change is one quickstart line documenting the new lookup key) plus AGENT_STATE.md, CHANGELOG.md, RUNS/run-16.json (mandatory tracking). Same recorded reasoning as runs 1-15. No DECISIONS.md entry (no pivot: followed run 15's Next Suggested Action exactly). No RESEARCH_LOG.md change (no external research). No THIRD_PARTY_NOTICES.md change (no code copied).
- Environment note (carried forward): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); web_fetch/WebSearch are the only viable path for live GitHub verification, with a provenance restriction (URL must appear in a search result first). Client-rendered pages (commits history) return empty. Star counts above ~1k are only server-rendered rounded. Releases pages show tags/SHAs/notes but render dates without the year. ALSO: stale /tmp checkout dirs from prior runs are owned by another uid and cannot be removed; clone to a fresh timestamped directory instead.
- Record decisions and state changes.

## Next Suggested Action

Run 17: write the final report if the experiment window is closing — a short document (or a final section in README.md/ANALYSIS.md) stating what Workshop became, the headline finding, how the agent worked under the rules, and honest limitations; doc-only is permitted since run 16 was executable, and JUDGING.md rewards final presentation. If instead more build time clearly remains, the best executable candidate is `--sort stars|age|score` on `list` with black-box tests (2 content files: workshop.py + test_workshop.py).
