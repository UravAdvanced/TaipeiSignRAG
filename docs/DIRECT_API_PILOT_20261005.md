# Direct Azure API four-photo pilot — 5 October 2026

The four original photographs completed through Azure in **97.393 seconds wall time**, with concurrency 3 and no retries. All responses reported `gpt-6-astra`. JSON structure passed, but the annotations contain material semantic regressions compared with the original images and earlier records. These trial outputs have not replaced production annotations.

## What ran

User explicitly requested direct-API testing of the same four photos after rejecting the exhaustive prompt and asking to keep the earlier annotation approach. The runner used a short [baseline instruction](prompts/BASELINE_API_ANNOTATION_V1.md), the six earlier semantic fields, and a strict JSON Schema. The instruction is a new standalone encoding of the earlier rules; there was no byte-identical historical standalone API prompt to reuse. It does not use the exhaustive v1 prompt or its extra coverage/relationship fields.

- Originals: scenes 003, 006, 029 and 190, each SHA-256 verified against the source manifest.
- Input: original JPEG bytes at 512×288, one image per independent request, image detail `high`.
- Provider: locally configured Azure HTTPS Responses endpoint; requested model/deployment `gpt-6-astra` and medium reasoning.
- Output: `summary_en`, `summary_zh`, `signs`, `objects`, `uncertain`, `unknowns`; typed legacy-style sign/object fields.
- Scheduling: three requests initially, fourth starts when one slot is free; SDK automatic retries disabled, explicit attempts recorded.
- `store=False`, no external tools, no historical annotations, no neighbouring images, and no conversation history supplied to the model.
- All four requests succeeded on their first attempt; no incomplete, refused or structurally invalid result.

The model name is now returned by the Azure API response, not inferred only from local settings. This does not expose an underlying version/snapshot beyond what the service reports.

## Timing and usage

| Scene | API request duration | Queue delay | Input tokens | Output tokens, including reasoning | Reasoning tokens within output |
| --- | ---: | ---: | ---: | ---: | ---: |
| 003 | 61.440 s | 0 s | 1,008 | 2,933 | 1,552 |
| 006 | 51.469 s | 0 s | 1,008 | 2,799 | 1,034 |
| 029 | 39.178 s | 0 s | 1,008 | 1,973 | 936 |
| 190 | 55.121 s | 39.195 s | 1,008 | 2,844 | 1,307 |
| Total reported usage | | | **4,032** | **10,549** | **4,829** |

Reported total tokens: **14,581**, with zero cached input tokens. Reasoning tokens are already included in output/total tokens; do not count them twice. These are response-reported usage figures, not an invoice or verified Azure bill. Actual billed cost was not retrieved.

The timed run began 2026-10-05T11:53:02.185669+00:00 and ended 2026-10-05T11:54:39.578949+00:00. Its **97.393 s** includes client setup, image encoding, request scheduling, network/API time, parsing and saving. Individual request durations overlap and sum to 207.208 s; that sum is not elapsed batch time or a measured sequential-run benchmark. Parsing and annotation-file writing totalled 0.031 s; raw-response and metrics writes are outside that smaller submeasurement but within whole-run time. Offline preparation took 0.076 s. Coding, permission waits before launch, documentation, later structural checks and comparison inspection are outside the timed run.

The prior exhaustive Codex trial on these four photos took 678.189 s (11 min 18 s), versus 97.393 s (1 min 37 s) here. That is about 6.96 times less elapsed time for these two workflows, but the instruction, output contract, image presentation, conversation context and execution method changed. Do not attribute the entire difference to API transport or concurrency.

Against the **original concise workflow**, the current sample does not establish a material speed advantage: direct wall time averaged 24.35 s/photo, while historical 19-photo batch averages were 18.79 s (explicit pre-annotation gap excluded), 22.79 s and 28.80 s. The same four photos have no original per-photo timestamps. Sample/workflow differences preclude a controlled speed ratio or a full-dataset completion promise.

## Annotation comparison against previous records and original images

Post-run visual comparison was performed separately from annotation/request timing. It is assistant inspection, not expert Chinese-language ground truth. The older records were not assumed infallible; plausible additions remain distinguished from confirmed corrections.

| Scene | Agreement/additions | Material discrepancy or limitation |
| --- | --- | --- |
| 003: overhead board and gates | Captures gates, display, clock-like features, door, platform right arrow and small green emergency marker. | Fails to transcribe the visible 廁所 and 車站大廳 labels fully; turns the ticket-office label into a partly unreadable Taipei destination, labels toilet-related symbols as an elevator, and reverses the panel locations of 台鐵/高鐵. It asserts a fire extinguisher beside the far-right door that is not established in the assessable source image. |
| 006: locker corridor | Retains Tamsui-Xinyi Line, Taipei Bus Station, both underground-mall names, right-side lockers and the separate right-pointing emergency arrow. Additional English transcripts agree broadly with the in-session trial. | Adds a left locker bank and shared parking-up association where earlier records were more limited. The left blue panel plausibly suggests storage equipment, but the full physical bank/compartment claim needs confirmation; it is not automatically a false positive merely because the old record omitted it. The cropped yellow area is called a destination sign although its function is not clearly established. |
| 029: stairs and escalators | Correctly recognizes stairs, flanking escalators, service/information label and North 3/Civic Boulevard exit. | Reads the ticket-office panel as **台北轉運站 / Taipei Bus Station**, including an asserted English transcript, where the source/earlier record support **台鐵售票處 / TRA ticket office**. It also fails to recover 車站大廳 at left. This is a substantive wrong destination, not just different phrasing. |
| 190: blurred overhead board | Preserves platform-up, exit-left, taxi-up, and unknown white-panel destinations; adds Chinese taxi-stand wording. | Omits the visible red extinguishers at the dividing column. Adds shopfront and yellow illuminated-equipment interpretations not securely established by the image, and a distant parking symbol that remains uncertain. The central blurred destination names remain unresolved. |

The API result has 26 sign entries, 28 object entries and two uncertain-equipment entries. More entries are not proof of better accuracy. The clearer parts of scene 006 fare better than the small-text boards in 003/029; no numeric semantic-accuracy score was assigned.

The typed JSON Schema did not constrain the full semantic category vocabulary. Consequently outputs include `fare_gate` instead of the existing `fare_gates_or_turnstiles`, and `emergency_sign` instead of `emergency_exit_sign`. Normalized labels also differ in wording/case. Passing the shape check is not enough to feed the current exact-label coverage mapper unchanged. A category enum or deterministic adapter is needed before production integration; it would not repair the Chinese transcription errors.

## Interpretation and next technical step

Direct API execution and concurrent scheduling work. This particular four-photo configuration is not yet equivalent in annotation quality to the earlier in-session work, and the results should remain trial records. The findings do not establish that direct APIs inherently have lower quality.

An important unresolved difference is image presentation: this API test sent native 512×288 JPEGs, while Codex inspection used 1536×864 resized views. Enlargement creates no new source detail, but it can change how an image is represented/processed by a vision system. The short standalone instruction and absence of conversation context are additional changes. None has been isolated as the cause of the observed errors.

Before scaling this configuration, the most focused next experiment would hold the short baseline instruction, schema and model settings fixed and test the same inspection-size image presentation. That would be a separate, explicitly reported inference test, not secretly repeated annotation of the production corpus. No such extra API calls were made in this pilot. The exhaustive prompt remains rejected; no human-review publication gate is introduced.

## Credential and publication handling

The API key is read from the existing configured environment variable. It is not passed in command-line arguments, hard-coded, printed, or written into annotations. Request headers and image data URLs are not saved. Normal HTTP/client debug logging is disabled. Local output strings are also scrubbed against the credential value before writing. A post-run scan of 19 pilot/source/prompt files found no occurrence of the credential.

Requests went to the configured Azure HTTPS endpoint with normal TLS verification and automatic redirects disabled. The original images and instructions necessarily reached Azure. `store=False` was requested and echoed as false in all four responses. This does not establish absence of provider-side abuse-monitoring, account/admin, billing or infrastructure logs. Account-specific retention policies were not audited. “Not public or committed to GitHub” is the supported assurance; “secret from Azure” is not.

Raw API responses, request/response IDs, annotations and timing records remain under `data/direct-api-pilot-20261005/`, which Git ignores. The public-safe runner reads the endpoint from local configuration rather than embedding the account endpoint. No API key, new photographs or raw test responses were added to the release package. No commit/push/deployment occurred in this test turn.

## Artifacts and checks

- `scripts/run_annotation_api_pilot.py`: bounded four-photo runner; `prepare` is offline, `run` makes the authorized requests and skips already successful photos, `report` checks saved results without inference.
- `docs/prompts/BASELINE_API_ANNOTATION_V1.md`: short baseline instruction used by the API pilot.
- `data/direct-api-pilot-20261005/manifest.json`: exact source, schema and prompt hashes, source dimensions and production file hashes.
- `data/direct-api-pilot-20261005/summary.json`: measured durations, attempts, returned model and reported usage.
- `data/direct-api-pilot-20261005/tps-scene-*.annotation.json`: unmodified API semantic outputs.
- `data/direct-api-pilot-20261005/tps-scene-*.response-1.json`: local raw responses, never public release inputs.

All four sources and annotation hashes, strict six-field output parsing, production-file hashes and Git ignore checks passed. The four production data files remain byte-identical to their pre-test state. Functional shape checks do not validate the semantics described above.
