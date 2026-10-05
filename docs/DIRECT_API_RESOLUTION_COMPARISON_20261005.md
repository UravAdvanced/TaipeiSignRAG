# Four-photo API input comparison — 5 October 2026

The same four photos completed at **1536×864 in 80.918 seconds**, compared with **97.393 seconds** for native 512×288 inputs: 16.916% less elapsed time in these two runs. Annotation quality was mixed: substantial destination-reading improvements in scenes 003 and 029, a new wrong destination in scene 006, and partial equipment-coverage improvement in blurred scene 190. This is a descriptive paired pilot, not evidence that enlargement always improves accuracy or speed.

## Inputs and controls

The exact dimensions are **1536×864**, not 1535×864 or 1535×86. The source photographs are 512×288 JPEGs. The enlarged files are the exact PNGs previously viewed in Codex, verified by SHA-256 and pixel equality with the original decoded RGB images resized to 1536×864 using Pillow's default resize. Enlargement supplies no additional captured detail; it can affect the model's image processing.

Both API runs used scenes 003, 006, 029 and 190, the same short baseline instruction and strict six-field schema (byte-identical), requested/returned model `gpt-6-astra`, medium reasoning, image detail `high`, maximum output 8,000 tokens, `store=False`, and concurrency three. Each photo received one request in each condition; all succeeded on the first attempt. Historical annotations and comparison findings were not supplied to either API run. The rejected exhaustive prompt was not used.

The experiment changes both dimensions and encoding: native JPEG versus enlarged PNG. Requests also ran at different times with independently generated answers. It therefore compares two input representations; it does not isolate a causal resolution effect. The service reports a model name, not a pinned underlying snapshot. No repeated trials, randomization, blinded scoring or expert reference set were used.

## Measured timing and usage

| Scene | 512×288 JPEG request | 1536×864 PNG request |
| --- | ---: | ---: |
| 003 | 61.440 s | 44.077 s |
| 006 | 51.469 s | 39.147 s |
| 029 | 39.178 s | 37.351 s |
| 190 | 55.121 s | 42.364 s |
| **Whole four-photo run** | **97.393 s** | **80.918 s** |

Requests overlap: three start first and scene 190 starts when scene 029 finishes. Individual durations are not additive wall time. The enlarged run started at 2026-10-05T12:19:07.417064+00:00 and finished at 2026-10-05T12:20:28.334977+00:00. Wall time includes client setup, local image verification/encoding, request scheduling, network/service time, parsing and saving. Offline preparation (0.284 s), implementation, permission waits before launch, subsequent visual comparison and reporting are excluded. Four request durations sum to 162.939 s; this is not a measured sequential benchmark. Parsing and annotation-file saving totalled 0.0178 s, with other file writes included in whole-run time.

| Reported usage | 512×288 | 1536×864 |
| --- | ---: | ---: |
| Input tokens | 4,032 | 8,296 |
| Output tokens, including reasoning | 10,549 | 8,425 |
| Reasoning tokens, already included above | 4,829 | 3,182 |
| Total tokens | 14,581 | 16,721 |
| Cached input tokens | 0 | 0 |

The enlarged run used 105.754% more input tokens, 20.135% fewer output tokens and 14.677% more total tokens. Less generated output/reasoning is a possible contributor to lower latency; service/network variability is also unresolved. These measurements do not support blaming larger images for the earlier slowdown. Token totals are not billed cost; no invoice was retrieved.

A simple throughput extrapolation gives **80.918 / 4 × 19 = 384.361 seconds, approximately 6 min 24 s for 19 photos**, assuming comparable images, answers, concurrency and service conditions. This estimate includes the four-photo sample's scheduling overhead; it is not a measured 19-photo run or a confidence bound, and excludes later comparison/reporting.

## Annotation comparison

The saved outputs were compared with the same four source-derived inspection images and historical concise annotations. This was post-run assistant inspection, not Chinese-expert validation; no numeric accuracy score is justified. Earlier records were references, not assumed complete ground truth.

| Scene | Change from native API output to enlarged API output | Assessment |
| --- | --- | --- |
| **003 — board and gates** | Recovers 廁所, 車站大廳 and 台鐵售票處; replaces the incorrect elevator interpretation with toilet/accessibility symbols. Groups TRA/HSR platforms without the earlier reversed individual positions. Drops the unsupported extinguisher beside the right door. Retains gates, display, clock and door; adds background gate notice/information panels. | Substantial improvement in the main destinations and symbols, closer to the original concise record. Still omits the small ticket-panel qualifier/floor wording. Added English transcripts and shared-arrow associations are not all certified as exact readings. |
| **006 — locker corridor** | Changes the correctly read 臺北轉運站 / Taipei Bus Station into **臺北車站 / Taipei Main Station**, and the bus pictogram into a train pictogram. Keeps the line, both malls, toilet/parking symbols, lockers and emergency-right arrow. Drops the proposed left locker bank and treats the cropped yellow foreground as storefront/advertising rather than a destination sign. | Material regression in destination identity, contradicted by the visible bus-station wording and historical annotation. Dropping the left-bank claim is not scored as a confirmed correction because that equipment interpretation remains uncertain. |
| **029 — stairs/escalators** | Recovers 車站大廳 and changes the incorrect Taipei Bus Station to **台鐵售票[unreadable] / TRA ticketing**. Preserves service centre, North 3/Civic Boulevard, stairs and both escalators. Adds safety stickers; omits separately listed wall cladding. | Substantial destination improvement. The final ticket-office character and some English remain explicitly unreadable. New shared up-left associations go beyond the conservative historical annotation and are not independently validated route facts. |
| **190 — blurred board** | Retains platform-up, exit-left and taxi-up. Central white-panel destinations remain unknown. Now records red equipment at the centre-left column as **possibly fire extinguishers**; native output omitted it. Separates the pink advertisement and far-right illuminated display, dropping the previous uncertain yellow-equipment interpretation and distant parking assertion. | Partial improvement in secondary coverage and caution. Extinguishers are still uncertain in the API output despite stronger historical identification; a distant shopfront interpretation remains unconfirmed. Enlargement did not resolve the badly blurred white-panel text. |

The enlarged outputs have 25 sign entries, 24 object entries and one uncertain-equipment entry, versus 26, 28 and two respectively for native inputs. These counts are not recall/accuracy scores: outputs group facts differently and include different categories. The enlarged run still emits categories such as `fare_control` and `storage` instead of production vocabulary; shape validation does not establish direct compatibility with the exact-label coverage mapper.

Compared with the earlier concise Codex annotations, the enlarged API answers contain more secondary scene descriptions, but scene 006 is worse on a major destination and scene 190 is less definite about extinguishers. No same-four-photo timing exists for the historical concise method. The rejected exhaustive Codex run (678.189 s) changed instructions/context/output requirements and cannot isolate the API's speed advantage.

## Artifacts and preservation

- Native run: `data/direct-api-pilot-20261005/`; original report: [DIRECT_API_PILOT_20261005.md](DIRECT_API_PILOT_20261005.md).
- Enlarged run: `data/direct-api-pilot-1536-20261005/`, including exact input hashes/dimensions in `manifest.json`, usage/timing in `summary.json`, and unchanged raw responses and annotations.
- Offline validation: `python scripts/run_annotation_api_pilot.py report --image-mode inspection`. Do not rerun completed inference to reproduce the report.
- The four production-data files remain byte-identical to their pre-test hashes. Trial outputs are separate; no trial annotation was imported and no new image published.

Credentials are read from the existing environment and are not saved in request arguments, annotations or reports. Local trial folders are ignored by Git. Azure necessarily received the images and prompt; `store=False` is not a guarantee of no service/admin/billing logs. Human expert review remains deferred, with no new publication gate introduced by this experiment.
