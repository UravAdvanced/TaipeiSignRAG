# Annotations-only pilot timing

Checked locally on 5 October 2026: three batches of 19 exact photographs, scenes 129–185. All 57 new records publish dataset, filename, source hash and annotations without new evidence images, thumbnails or crops. The 128 previously prepared scene images remain byte-identical. Human review remains pending.

| Scenes | Recorded wall time | Interpretation | Local export/check time |
| --- | ---: | --- | ---: |
| 129–147 | 905.154 s (15 min 5 s) | Includes a 548.115 s preparation-to-annotation gap; excluding that recorded gap gives 357.039 s (5 min 57 s). | 8.341 s |
| 148–166 | 432.961 s (7 min 13 s) | Continuous recorded workflow, including tool round trips and saving. | 8.303 s |
| 167–185 | 1771.828 s (29 min 32 s) | Interrupted between turns and includes permission waits. No comparable complete active-work measurement. | 8.904 s |

Times are workflow observations, not isolated model latency. Batch 8's resume timestamp was saved after four image views and a permission wait; its 996.795 s resumed segment omits some work and cannot stand in for the full batch. The original timestamps are preserved in `annotations/batch_progress.json` and the local batch checkpoint. The final timing/report write is outside the measurement.

The first two batches suggest roughly 6–7 minutes per 19 photos when the explicitly recorded pre-annotation gap is excluded. That is preliminary: the third batch does not confirm the estimate. Do not average all three as a throughput benchmark or extrapolate a completion promise. The earlier 761 s masked-image batch included setup and permission waits and is not a controlled baseline.

The recurring local export/check stages took 8.3–8.9 s per batch. One-off migration work is excluded. The earlier 23.422 s local masked-image workflow rebuilt all 128 retained views; the current workflow avoids that rendering. This supports a reduction in local processing, but does not isolate the effect of removing mask-coordinate authoring on annotation time.

Each batch saved 19 records with zero failed or structurally incomplete records; unreadable text remains explicitly unknown. Checks passed for source hashes, retained image hashes, annotations-only shape, coverage counts, 375 Python/JavaScript search-parity cases and static/API routes. These checks do not validate every transcription or replace expert review.

Saved session configuration requests Azure GPT-6 Astra with medium reasoning. Actual serving-model identifiers, provider request counts, billed tokens and observed costs are unavailable. No metered cost or confirmed serving-model claim is made.

The three-batch pilot ended at 185 scenes plus two locker observations, covering 186 unique source images; 8,785 source entries remained at that checkpoint. It was subsequently pushed and deployed in commit 41296b7, together with the requested destination catalogue removals. These publication actions were outside the timings above.

## Continuation after the pilot

On 5 October 2026 the user resumed work. Batch 9 (scenes 186–204) took 547.268 s wall time (9 min 7 s), including tool round trips and a Windows write-permission wait. Local preparation took 3.384 s, the preparation-to-annotation gap 5.033 s, annotation/saving 527.982 s, and export/check scripts 10.459 s. This is another workflow observation, not isolated model latency. All 19 records saved and passed structural checks; human review remains pending.

Current total: 204 scenes plus two locker observations, covering 205 unique originals; 8,766 source entries remain. All 128 retained scene images are unchanged. Next batch is 205–223. Publication remains at 185 pushed and deployed scenes; the next ordinary milestone is 285. Batch 9 is checked locally and has not been pushed or deployed.
