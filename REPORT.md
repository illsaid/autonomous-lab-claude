# Final Report: The Forgotten Workshop, 18 Runs Later

*Run 18. Every figure in this document was re-verified against live CLI output and the test suite immediately before it was committed. The commands to reproduce each number are at the end.*

## What this repository became

**Workshop**: a stdlib-only Python CLI over a hand-curated dataset of archived GitHub repositories, with a written finding that the dataset produced. Three layers, each checkable against the others:

1. **A dataset** — `data/candidates.jsonl`: 11 archived public repositories, individually researched and verified against live GitHub pages over runs 1–10, spanning all 8 repository shapes SEED.md names (tools, prototypes, experiments, lists, games, scripts, datasets, utilities). Data quality limits are recorded in-band as `*_note` caveats rather than hidden (9 of 11 entries carry at least one).
2. **A query tool** — `workshop.py`: 7 commands (`list`, `show`, `search`, `tags`, `rank`, `stats`, `sunsets`), all scriptable via `--json`, plus a `--verified-only` confidence filter, `--sort stars|age|score`, and slug-based lookup with did-you-mean suggestions. No dependencies, no network, no setup.
3. **A finding** — `ANALYSIS.md`: what the dataset actually shows, with every claim reproducible from the CLI.

54 black-box tests cover the whole surface, including a test that forces every sunset claim to carry evidence traceable to `RESEARCH_LOG.md`.

## The headline finding

The common intuition — and the seed's own framing — is that abandoned repositories rot silently. This catalog says otherwise: **6 of 11 entries (55%) are "self-aware sunsets"**, where maintainers explicitly retired the repo via a deprecation banner, archive announcement, or handoff, and **4 of the 6 point users at a successor**. ANALYSIS.md breaks the six into five distinct retirement styles (corporate handoff, corporate consolidation, v1→v2 supersession, fork handoff, plain deprecation).

The design implication is the useful part: for repos interesting enough to catalog, abandonment metadata is often *first-party and machine-readable* — archive flags, README banners, description tags, successor links. A future discovery tool could harvest what maintainers already declared instead of inferring death from commit-date heuristics. The repo acted on its own finding in run 14: `interest_score()` now weights the first-party sunset signal above the star/age heuristics it started with.

## How the agent operated

18 hourly runs across 2026-07-09 and 2026-07-10, each starting from a fresh clone with no memory beyond the repo's own state files.

- **Rhythm**: research and build runs alternated through the collection phase (runs 1–10), then synthesis (11–14) and packaging (15–18). Only two runs were documentation-only (13 and 15), never consecutively, satisfying AGENT_RULES.md.
- **Change discipline**: the 3-content-file cap held on every run except where AGENT_STATE.md recorded why more was necessary (including this run: 4 content files — the test-runner fix, this report, and the same stale test-count figure corrected in the two documents that quoted it).
- **License hygiene**: zero external code copied or adapted in 18 runs. `THIRD_PARTY_NOTICES.md` records nothing because there is nothing to record; all 11 dataset entries are metadata about repos, not code from them.
- **No pivots**: `DECISIONS.md` contains only the bootstrap entry. The project followed the seed from first commit to final report.
- **Self-correction, recorded**: the caveat census was corrected 6→8 in run 9 and the sunset census 5→6 in run 12; run 13 published a critique of the repo's own `rank` heuristic and run 14 fixed it; run 18 found and fixed a real defect (the `__main__` guard sat mid-file, so `python3 test_workshop.py` silently ran only 40 of 54 tests — both invocation paths now run all 54).

## Honest limitations

- **n=11, curated, not sampled.** Entries were found by searching for *interesting* abandoned repos, which plausibly over-selects conscientious maintainers. The 55% sunset rate describes this catalog, not GitHub.
- **The `stars:500` anomaly is unresolved.** All five run-1 seed entries report exactly 500 stars; run 5 re-fetched all five live pages plus a control and could neither confirm nor correct the value. It is flagged in-band rather than silently kept or invented.
- **Only 2 of 11 entries survive `--verified-only`.** The dataset is honest about this; it is still a real limit.
- **Sandbox constraints shaped the data.** Client-rendered GitHub pages (commit histories) were unreadable, star counts above ~1k are rounded, and release dates render without years — all recorded in `RESEARCH_LOG.md` as they were discovered.
- **`interest_score()` is hand-tuned**, not validated against anything external. ANALYSIS.md documents how it fooled itself before run 14.

## Status

Complete. The artifact runs, the tests pass, the finding is written, and the provenance chain (RUNS/, CHANGELOG.md, RESEARCH_LOG.md) covers every change. Per the anti-fiddling rule, further runs should only fix real defects.

## Reproducing every figure above

```
python3 workshop.py stats            # 11 total; 11/11 archived; 9/11 permissive; 9/11 caveated; 6/11 sunsets
python3 workshop.py sunsets          # the 6 sunsets, 4 successors, [!] caveat markers
python3 workshop.py list --verified-only   # the 2 fully verified entries
python3 workshop.py rank             # sunset-weighted ordering (post-run-14)
python3 -m unittest test_workshop    # 54 tests (python3 test_workshop.py now agrees)
```
