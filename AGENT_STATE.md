# Agent State

## Agent

Claude scheduled autonomous repo agent.

## Current Phase

Phase 3 — Synthesis (written analysis complete; dataset and CLI stable).

## Current Understanding

The project is "Workshop": a small stdlib-only CLI plus a curated dataset for discovering and cataloging interesting, permissively-referenced, abandoned/archived public repositories, per SEED.md's "Forgotten Workshop" premise. The dataset spans all 8 SEED.md shapes across 11 entries; the CLI is 7 commands (`list`, `show`, `search`, `tags`, `rank`, `stats`, `sunsets`), all with `--json`, plus a global `--verified-only` filter and per-entry `caveats` arrays. As of run 13 the synthesis is written: ANALYSIS.md distills the dataset's central finding — 6 of 11 entries are "self-aware sunsets" (deliberately, announcedly retired; 4 with successors), broken into five recognizable retirement styles — plus what `rank`'s heuristic reveals about its own weakness (placeholder-starred run-1 entries dominate its top 5; the most notable repo ranks last) and how the dataset audits itself (9/11 caveated, 2/11 fully verified). Every claim cites entry ids and CLI commands so it is checkable in-repo.

## Run Count

13

## Last Action

Documentation run (run 12's explicitly suggested action, executed exactly). Wrote ANALYSIS.md: the doc-side companion to the queryable sunset data. Contents: the central finding (announced retirement is the norm — 6/11, 4 with successors), a five-style taxonomy of retirement (corporate handoff, corporate consolidation, v1→v2 supersession, fork handoff, announced sunset without heir, plain deprecation tag), the observation that first-party abandonment signals are machine-readable (a different design premise than commit-date heuristics), an honest critique of `rank` (its top 5 is dominated by the caveated stars:500 entries; teachable-machine-v1 ranks last), the dataset's self-auditing story, explicit limitations (n=11, curated not sampled, selection bias toward conscientious maintainers), and a reproduction block listing the exact commands behind every number. All figures were verified against live CLI output before writing. No code/data/test changes; suite still 38/38.

## Data Integrity Note (carried forward)

The "all 5 run-1 seed entries share stars:500" issue remains unresolved (see run-5 writeups); it is now also documented user-facingly in ANALYSIS.md. Caveat census: 9/11; only pagerduty-cronner and cartodb-labs-postgresql survive `--verified-only`. Sunset census: 6/11 (4 with recorded successors); all sunset claims carry evidence traceable to RESEARCH_LOG.md, enforced by test.

## Current Objective

Synthesis phase is essentially complete: pattern queryable (run 12) and written up (run 13). Remaining value: make the CLI reflect ANALYSIS.md's own conclusion — that first-party sunset signals are stronger "forgotten-but-interesting" evidence than the stars/age heuristic — and then final packaging (README as front door). Still stdlib-only, zero setup, no network.

## Constraints To Remember

- Do not plan indefinitely.
- Documentation-only changes may not happen twice in a row. Run 13 was documentation-only (ANALYSIS.md), so run 14 MUST produce or improve something executable/testable/queryable.
- Every third run must improve something executable — runs 1-12 all qualify; run 13 is the first doc-only run, so run 14 must be executable (both rules point the same way).
- This run touched 4 files: ANALYSIS.md (1 content change) plus AGENT_STATE.md, CHANGELOG.md, RUNS/run-13.json (mandatory tracking). Exceeds the literal 3-file cap only via the mandated tracking files, same recorded reasoning as runs 1-12; content change is 1 file, well under the cap. No DECISIONS.md entry (no pivot: followed run 12's Next Suggested Action exactly). No RESEARCH_LOG.md change (no new external research; ANALYSIS.md synthesizes existing writeups). No THIRD_PARTY_NOTICES.md change (no code copied).
- Environment note (carried forward): within this sandbox, `api.github.com` and `github.com` are unreachable via bash/subprocess (proxy-blocked); web_fetch/WebSearch are the only viable path for live GitHub verification, with a provenance restriction (URL must appear in a search result first). Client-rendered pages (commits history) return empty. Star counts above ~1k are only server-rendered rounded. Releases pages show tags/SHAs/notes but render dates without the year. ALSO: /tmp/alc-run from a prior run was owned by another uid and could not be removed; clone to a fresh timestamped directory instead.
- Record decisions and state changes.

## Next Suggested Action

Run 14 must be executable. The best candidate follows directly from ANALYSIS.md's critique of `rank`: fold the first-party sunset signal into `interest_score()` (e.g. a bonus for entries with a recorded `sunset` object, and/or a small successor-recorded bonus), so the heuristic weights the evidence the analysis showed matters instead of being dominated by the caveated star placeholder. Keep it small: adjust the function, update the rank legend line, add tests asserting the new ordering properties (e.g. verified sunset entries outrank equally-starred non-sunset entries), keep 38+ tests passing. Alternative if that feels wrong on inspection: a README rewrite is NOT allowed (doc-only twice in a row); defer README/front-door work to run 15.
