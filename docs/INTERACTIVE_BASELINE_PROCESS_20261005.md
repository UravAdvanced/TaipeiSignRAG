# Four-photo interactive annotation process demonstration

## Purpose and workflow decision

When annotation time became a practical concern, we investigated an expanded instruction and concurrent direct-API execution using native and enlarged image inputs. We selected the original concise, whole-photograph interactive workflow for continued dataset creation, prioritizing detailed scene evidence, bilingual annotations and explicit uncertainty for downstream retrieval. The four-photo exercise here demonstrates execution of that process. It is not a controlled study establishing inherent superiority of interactive execution over an API.

Detailed annotations make visible text, destinations, fixtures and surrounding scene evidence available to a RAG system. Their usefulness also depends on correctness, evidence links, retrieval and answer generation; annotation volume alone is not a measure of RAG quality. No downstream RAG accuracy comparison was performed in these pilots.

Human review is a planned part of the process: reviewers will compare each photograph with the Chinese and English annotations, check translations, destination/arrow associations, omissions and unsupported claims, and inspect privacy handling for missed faces, including faces missed in existing released-image masks. Original photographs used for annotations-only records are not thereby certified as face-free. This demonstration does not constitute completed human or privacy review. Dataset creation and the research demo proceed with review status recorded; specialist review is deferred, not an immediate publication gate.

## Execution

On 5 October 2026, scenes 003, 006, 029 and 190 were inspected sequentially as the exact 1536×864 PNGs used in the earlier inspection and enlarged API pilot. Their original files are 512×288 JPEGs; ordinary resizing adds no captured detail. Input hashes and production-data hashes were checked against the earlier manifest.

For each image, the assistant authored the established six semantic fields: `summary_en`, `summary_zh`, `signs`, `objects`, `uncertain` and `unknowns`. The instructions were the existing whole-photograph policy, without the rejected expanded checklist/relationship schema. Entries distinguish visible fixtures from facilities mentioned only on signs. No person descriptions were included. Records were saved separately, structurally checked, and hashed; existing production annotations were not replaced. No direct Azure inference request or second model reviewer was added for this demonstration.

There was one image view in each photo's timed annotation interval. Scene 003 was also displayed during an aborted start attempt before the ledger could be written; that extra pre-start exposure is disclosed. The session already contained these images, prior annotations and comparison findings. This is a fresh authoring pass using the original procedure, not an independent reconstruction of the historical model/context. The actual serving model and inference-token usage for interactive execution were not independently verified.

## Observed outputs and comparison

| Scene | Interactive demonstration | Relation to earlier direct-API outputs |
| --- | --- | --- |
| 003 | Records 廁所, 車站大廳, 台鐵售票處, TRA/HSR platform references, gate notice, gates, partitions, clock, display, background panels, door and green marker. Small English/qualifier text stays unknown. | Recovers major labels missed by native API; enlarged API also recovered them. Interactive answer is more conservative about English transcripts and station-hall arrow scope. |
| 006 | Records 淡水信義線, 臺北轉運站 / Taipei Bus Station, both underground malls, toilet/accessibility and parking symbols, right lockers, left shopfront/advertisement, emergency arrow and uncertain left equipment. | Avoids enlarged API's incorrect Taipei Main Station/train interpretation. Native API read the bus destination correctly too. |
| 029 | Records station hall, TRA ticket office, service centre, North 3/Civic Boulevard, stairs, escalators and safety notices. Ticket/service arrow scope stays unresolved. | Avoids native API's incorrect bus-station destination; enlarged API also recovered TRA ticketing but left the final Chinese character unreadable. The interactive full Chinese reading still awaits human confirmation. |
| 190 | Records platform-up, exit-left, taxi-up, unresolved white destinations, secondary sign, red extinguishers, advertisements, green markers, columns and passages. | Native API omitted extinguishers; enlarged API marked them possible. Interactive identification is more definite and must be checked by a human. All workflows leave central white-panel destinations unresolved. |

The examples show that the selected process produces inspectable bilingual drafts covering signs and surrounding objects. They do not establish exhaustive coverage, independent correctness, a universal method ranking, or that every more-definite reading is an improvement. Human review outcomes have not been measured.

## Timing record

The offline helper records monotonic elapsed time and UTC timestamps. Timing begins before each image view and ends after its authored JSON is validated and saved. It includes tool round trips, writing/approval delays, reasoning and authoring. Preparation and subsequent comparison/reporting are outside the interval.

| Scene | Raw interval |
| --- | ---: |
| 003 | 2,011.180 s |
| 006 | 106.501 s |
| 029 | 53.832 s |
| 190 | 52.308 s |
| **Whole run, including between-photo gaps** | **2,228.528 s (37 min 8.528 s)** |

Start: 2026-10-05T12:52:28.131742+00:00. Final annotation save: 2026-10-05T13:29:36.659200+00:00. A long interruption occurred around saving the first photo; local-write escalation and session interaction also occurred. The ledger does not separately measure active inference versus these delays. Consequently this is a raw session-duration record, not a clean normal-throughput baseline. No estimated subtraction, API speedup ratio or 19-photo extrapolation is derived from it.

Earlier measurements remain separate: native API 97.393 s, enlarged API 80.918 s (both concurrency three), expanded-prompt interactive trial 678.189 s. Historical concise 19-photo timings are documented elsewhere. Their different scopes and conditions must remain attached to the figures.

## Reproduction artifacts

- `scripts/interactive_baseline_pilot.py`: offline `prepare`, `start`, `save`, `report` ledger; it does not generate annotations or call an inference API.
- `data/interactive-baseline-20261005/checkpoint.json`: exact source/input hashes, UTC/monotonic timing, policy hash and production hashes.
- `data/interactive-baseline-20261005/tps-scene-*.annotation.json`: four freshly authored, unchanged trial drafts.
- [Whole-photograph policy](WHOLE_SCENE_ANNOTATION.md), [API representation comparison](DIRECT_API_RESOLUTION_COMPARISON_20261005.md) and [expanded-prompt trial](PROMPT_COMPARISON_20261005.md).

The saved procedure and provenance support reproducing the workflow, rather than guaranteeing identical generated text. An offline `report` verifies the completed ledger and unchanged production hashes without re-inspecting the photographs. Trial files remain local and Git-ignored. No new image, production annotation, commit or deployment was published by this demonstration.
