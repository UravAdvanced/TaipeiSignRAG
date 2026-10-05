# Four-photo prompt comparison — 5 October 2026

The expanded prompt elicited broader secondary-scene coverage in this in-session comparison, but its exhaustive output was slower to author and save. It did not establish reliable recovery of the blurred white-panel destinations. This is a descriptive comparison, not an independent accuracy evaluation or an Azure API speed measurement.

## Scope and method

The user explicitly selected **Compare here in Codex**, requested four already completed photos including outliers, and requested processing-time comparison. Four original 512×288 photographs were verified against their recorded SHA-256 and enlarged to 1536×864 for inspection, matching the recent interactive batch's inspection scale. Resizing adds no source detail. One fresh view per selected original was used for this trial.

The [v1 prompt](prompts/SINGLE_PASS_SCENE_ANNOTATION_V1.md) was applied as an in-session annotation checklist. It was not submitted as a fresh isolated API request. Earlier annotations had appeared in the conversation, so the exercise was neither blinded nor independent. The first three records also come from the historical image/masking workflow; scene 190 comes from the newer annotations-only workflow. These differences prevent attributing every change to the prompt alone.

New records were saved separately before the helper reopened the four old records for comparison. Earlier conversation exposure still remains a limitation. No original dataset record was replaced. No Azure inference, second external reviewer, publication, dependency installation, or model training was performed.

## Observed differences

| Scene / source stem | Earlier record | Expanded-prompt trial | Interpretation |
| --- | --- | --- | --- |
| 003 / A05S_HH_001 | Four main sign groups and barrier gates; ticket arrow unresolved. | Adds clock, electronic display, closed door, a low green emergency marker, ceiling/concourse cues, and a possible information panel marked uncertain. Assigns the ticket panel's arrow upper-right. | Secondary objects are useful additions. The changed ticket-arrow association is a new interpretation, not an expert-confirmed correction. Small floor/English text remains unresolved. |
| 006 / A10E_HH_001 | Six main sign groups, lockers and left shopfront. Locker wording was already captured in the object record. | Adds the separate hanging green right-arrow emergency marker, explicit corridor/display cues and additional candidate English transcriptions. Makes the locker label a linked sign entry. | The emergency marker is a substantive added observation. Moving LOCKERS/置物櫃 into a sign record is restructuring, not newly recovered text. Complete shop name remains unknown. |
| 029 / A13W_HH_001 | Four destination groups, broad stairs with central handrail and flanking escalators. | Main interpretation unchanged; records two unreadable escalator-side notices, separates the handrail as an object, adds ceiling detail and partial English North 3. | The handrail was already described. Most expansion is granularity and localized uncertainty, not a new navigation finding. Notice wording and ticket/service arrow associations remain unresolved. |
| 190 / A02W_SS_013 | Platform/Exit/taxi signs, extinguishers, advertisements and green markers. White-panel arrows already mentioned in unknowns. | Represents the unreadable white groups as explicit sign entries; adds the distant direction board, column/corridor/ceiling structure and candidate Chinese taxi-stand wording. | More explicit inventory of unreadable regions, but the white destination names remain unknown. Taxi transcription is a new reading awaiting later expert assessment, not proof that blur was reversed. |

Counts rose from 17 to 25 sign entries and 9 to 24 object entries across four images. These are **not recall or accuracy scores**: entries were split, existing facts moved into new fields, and generic scene detail was added. Several new English/Chinese readings and the changed arrow association need eventual expert assessment before they can count as verified improvements.

The six shared semantic fields grew from 7,356 to 17,740 JSON characters in total (about 2.41×), even before the new coverage/relationship fields. Character counts are not token or billing measurements. The new records also contain local IDs, six region assessments, 14 amenity coverage entries, relations and image-quality information.

## Measured time

Each interval begins immediately before its image-view call and ends after its new JSON is saved and passes basic local shape checks. It includes model reasoning/generation, image-tool round trips, progress messages during the interval, JSON authoring, patch-tool waits and saving. It is not isolated image-inference time.

| Scene | Recorded seconds | Rounded time |
| --- | ---: | ---: |
| 003 | 222.112 | 3 min 42 s |
| 006 | 230.514 | 3 min 51 s |
| 029 | 148.590 | 2 min 29 s |
| 190 | 75.786 | 1 min 16 s |
| Four-photo wall interval, including between-photo gaps | **678.189** | **11 min 18 s** |

The four-photo interval ran from 2026-10-05T10:53:07.553675+00:00 to 2026-10-05T11:04:25.742260+00:00. Average was 169.547 seconds per photo. Local preparation took 0.603 seconds; earlier prompt-writing, helper setup and a directory-permission wait are outside the four-photo interval. Subsequent comparison, additional reference/hash checks and report writing are also outside it. Their complete wall durations were not instrumented; do not call 11 min 18 s the total conversation/task time. Parsing, writing and model time within each interval were not separately measured.

The earlier ledger contains no matching per-photo timings for these four originals:

| Historical batch | Photos | Recorded workflow time | Batch-average seconds/photo |
| --- | ---: | ---: | ---: |
| 129–147 | 19 | 357.039 s after excluding an explicitly recorded 548.115 s pre-annotation gap; raw wall 905.154 s | 18.79, gap-adjusted |
| 148–166 | 19 | 432.961 s | 22.79 |
| 186–204 | 19 | 547.268 s, including a permission wait | 28.80 |

The exhaustive trial was slower per photo in this session. These are different workloads, output sizes, interaction patterns and historical contexts; no controlled speed ratio or 19-photo projection is justified. It provides **no measured direct-API latency**. Actual serving-model metadata, token usage and billed cost are unavailable for this Codex trial.

## Can relaxing the prompt recover unreadable details?

Some previously omitted text may be legible and can be noticed with more careful attention; that is extraction of existing evidence. Details destroyed by low source resolution, blur, clipping, occlusion or cropping cannot be reliably reconstructed by deleting a no-guessing instruction. A model may supply a plausible completion from language or station knowledge, but that is a hypothesis, not a visible transcript.

The prompt already distinguishes difficult text from genuinely unreadable text: it asks for readable fragments and localized gaps, rather than automatically discarding small text. Better original-resolution source material can help. Enlarging the same 512×288 image or generating a sharpened/super-resolved version does not certify newly formed characters as authentic. A genuinely higher-resolution source would be new evidence and should retain its own provenance.

This trial did not compare a no-guessing prompt against an unrestricted prompt. It therefore makes no measured claim about how removing that instruction changes accuracy. The severely blurred white destinations in scene 190 remained unresolved under the expanded prompt.

## Recommended revision before an API throughput trial

Keep the systematic whole-image checklist, literal-transcript/translation separation, arrow association rules, transport distinctions and explicit unknowns. These address the project's recurring failure modes.

Make output compact: prioritize readable signs, identifiers, arrows, meaningful facilities and distinctive spatial cues; omit generic ceiling/floor prose unless it adds identification value. Avoid repeating the same limitations on every entry. Use sparse evidence-ID lists and explicit coverage states, with local code expanding mechanical schema structure. Local code must not invent a semantic assessment that the model never made.

Retain the 14-category coverage as a concise structured checklist rather than a long explanation for each category. Do not reprocess the existing 204 records just to add these fields. Human review is deferred and is not a publication gate.

A direct API runner could return this compact JSON in one independent request per original, with concurrency 3 initially. It would log real request durations and usage and avoid authoring JSON through interactive patch calls. That architecture is still a proposal; this user-selected Codex comparison does not establish its speed or accuracy.

## Local artifacts and validation

- `data/prompt-comparison-20261005/checkpoint.json`: source provenance, prompt hash and exact timing.
- `data/prompt-comparison-20261005/tps-scene-*.new.json`: four trial annotations.
- `data/prompt-comparison-20261005/tps-scene-*.previous.json`: snapshots of the earlier records.
- `data/prompt_comparison_20261005.py`: local preparation/checkpoint helper; no semantic inference or network requests.

Four original source hashes were checked during preparation. Subsequent checks passed for the four saved annotation hashes, unique local IDs, relationship references, correct evidence-array references, prompt hash and equality of all four production records with their saved prior snapshots. These are structural/provenance checks, not Chinese-language verification. Inspection images remain under the ignored local data directory.
