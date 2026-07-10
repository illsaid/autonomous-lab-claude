# Analysis: What the Forgotten Workshop Dataset Shows

*Run 13. Every claim below is checkable against this repo: the cited entry ids resolve via `python3 workshop.py show <id>`, and the cited numbers come from `python3 workshop.py stats` and `python3 workshop.py sunsets`. No claim here relies on data that is not in `data/candidates.jsonl`.*

## The dataset in one paragraph

`data/candidates.jsonl` holds 11 hand-curated, individually researched public GitHub repositories that fit SEED.md's "forgotten workshop" premise: all 11 are archived, 9 of 11 are permissively licensed, and they span ops tooling, libraries, a chat bot, teaching workshops, a game engine, a data-access wrapper, a creative ML experiment, and an IoT simulator — the full range of shapes SEED.md names. Last-push dates run from 2011 (`django-deployment-workshop`) to 2024 (`dmarx-psaw`). The dataset was collected over runs 1–10 (see `RESEARCH_LOG.md` for the per-entry verification writeups) and made queryable by the `workshop.py` CLI.

## Central finding: abandonment is usually announced, not silent

The seed's framing — and the common intuition — is that abandoned repos simply rot: commits stop, issues pile up, nobody says anything. The dataset says otherwise for repos interesting enough to catalog. **6 of 11 entries (55%) are "self-aware sunsets": the maintainers explicitly retired the repo**, via a deprecation notice, an archive announcement, or a handoff. **4 of the 6 point users at a successor.** Run `python3 workshop.py sunsets` to list them; each entry's `sunset.evidence` string traces to a dated writeup in `RESEARCH_LOG.md`, and a test (`TestSunsets`) enforces that traceability.

The six break into recognizable retirement styles rather than one pattern:

| Style | Entry | What happened | Successor |
|---|---|---|---|
| Corporate handoff to community | `pagerduty-cronner` | PagerDuty archived its ops CLI in favor of the maintainer's personal fork | theckman/cronner |
| Corporate consolidation | `azure-device-simulation` | Microsoft archived the repo with a banner redirecting to the wider PCS solution repo | Azure/azure-iot-pcs-device-simulation |
| v1 → v2 supersession | `teachable-machine-v1` | Repo is *named* v1; README redirects to the live v2 product and a boilerplate spin-off | g.co/teachablemachine |
| Fork handoff | `dmarx-psaw` | README opens with "THIS REPOSITORY IS STALE — Please consider using PMAW instead" | PMAW |
| Announced sunset, no heir | `redpoint-protogame` | Maintainers publicly announced the engine's end when archiving (Mar 2018) | none |
| Plain deprecation tag | `mozilla-notes` | Description and topics self-tag the repo DEPRECATED / abandoned / unmaintained | none |

The interesting implication: for this class of repo, "abandoned" metadata is often *first-party and machine-readable* — archive flags, README banners, description tags, successor links. A future discovery tool would not need to infer abandonment from commit-date heuristics; it could harvest what maintainers already declared. That is a genuinely different design premise than the one `rank`'s age-based heuristic started from.

The five remaining entries (`sorentwo-readthis`, `candybar-library`, `kanjielu-jeeves`, `django-deployment-workshop`, `cartodb-labs-postgresql`) carry no recorded retirement statement — though all are archived, so even these took the deliberate step of flipping GitHub's archive switch rather than going silent entirely.

## What `rank` reveals — mostly about itself

`python3 workshop.py rank` orders entries by `interest_score()` (star sweet-spot + age + permissive license + topic richness). Its output is honest in an unflattering way: 4 of the top 5 slots go to run-1 entries whose star counts carry the unresolved `stars:500` caveat (see below) — the placeholder value happens to sit squarely in the heuristic's sweet spot. Meanwhile the two fully verified entries (`pagerduty-cronner`, `cartodb-labs-postgresql`) rank 6th and 10th, and the most objectively notable repo (`teachable-machine-v1`, ~3.9k stars, a Google Creative Lab product with a shipped v2) ranks *last*, because the heuristic penalizes high star counts. The lesson: a "forgotten-but-interesting" score built on stars and age is easy to compute and easy to fool; the sunset signals above are stronger evidence of the thing the seed actually cares about.

*Update (run 14): this critique was addressed — `interest_score()` now weights the first-party sunset signal (+4.0, +1.0 more with a recorded successor), so the top 5 is led by evidence-backed sunset entries rather than the caveated `stars:500` placeholders, and `teachable-machine-v1` no longer ranks last.*

## The dataset audits itself

9 of 11 entries carry at least one `*_note` caveat (`stats` reports this; `--verified-only` filters on it). The largest is the run-1 `stars:500` anomaly: all five seed entries report exactly 500 stars. Run 5 re-fetched all five live pages (each still returned 500) and ran a control fetch (`torvalds/linux`, ~236k, correct), so the value can be neither confirmed nor corrected with this sandbox's tools — it is flagged in-band via `stars_note` instead of silently kept or invented. Two census corrections happened the same way (caveats 6→8 in run 9, sunsets 5→6 in run 12), both recorded rather than papered over. Only 2 of 11 entries survive `--verified-only`. A dataset this small that visibly tracks its own uncertainty is more useful than a larger one that doesn't.

## Limitations

n=11 and curated, not sampled: entries were found by searching for *interesting* abandoned repos, which plausibly over-selects maintainers conscientious enough to announce a sunset. The 55% figure describes this catalog, not GitHub. Star counts above ~1k are rounded (recorded as such). All of this is queryable rather than buried: `stats` for the censuses, `sunsets` for the evidence, `show <id>` for any single claim.

## Reproducing every number in this document

```
python3 workshop.py stats            # 11 total; 11/11 archived; 9/11 permissive; 9/11 caveated; 6/11 sunsets
python3 workshop.py sunsets          # the 6 sunset entries, successors, and [!] caveat markers
python3 workshop.py rank             # the heuristic ordering discussed above
python3 workshop.py show <id>        # per-entry fields, caveats, and sunset evidence
python3 -m unittest test_workshop    # 54 tests, including evidence-traceability enforcement
```
