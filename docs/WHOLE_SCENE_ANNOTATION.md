# Whole-photograph annotation policy and pilot

The user explicitly requested the entire photograph, including surrounding visual clues, rather than only the supplied COCO box. An annotation examines overhead signage, left/right surroundings, the foreground and the visible background. It records useful physical objects even when the original dataset did not label them. A CLS file remains a narrow crop: it cannot inherit off-image context without an evidence-linked source relationship.

## Current files

- `annotations/scene_pilot_notes.json`: authored observations from interactive visual inspection; the source of semantic content.
- `release/huggingface/scene_manifest.jsonl`: original-image hashes, supplied sign boxes and local privacy masks.
- `release/huggingface/scene_annotations.jsonl`: eight enriched whole-scene records.
- `release/huggingface/scene_images/`: native-size full-frame views with conservative person masks.
- `annotations/progress.json`: exact completed and remaining counts.
- `scripts/build_scene_records.py`: combines notes and provenance; does not automatically invent annotations.
- `scripts/scene_rag_demo.py` and `demo/index.html`: local evidence search and LLM-context preparation.

## Observation levels

1. **Visible:** a physical facility or object is directly supported by the image, such as the locker bank in scene 006 or the barrier gates in scene 003.
2. **Sign reference only:** a readable word or pictogram mentions a facility, but its physical entrance or equipment is not established. Toilet references in scenes 003, 004 and 006 belong here.
3. **Uncertain:** equipment exists but its function is not reliably identifiable. Counter-like forms are not promoted to ticket/check-in counters.
4. **Not observed in reviewed visible regions:** not found in the assessable portion of this photograph. This does not mean the facility is absent from the station.

The checked category set includes lockers, toilets, shopfronts, fare gates/turnstiles, lifts, stairs, escalators, train platforms/entrances, kiosks, check-in counters, ticket counters, service counters, map/information boards and emergency-exit signs. Other stable scene cues may be included, such as handrails, ceiling patterns, pillars and passage openings.

## Text, geometry and uncertainty

- `visible_zh` / `visible_en` hold reviewed readable sign text. Brackets or separated label normalization is documented where used. `label_en` and bilingual summaries are authored descriptions/translations, not automatically verbatim text.
- Unknown text remains null or is explicitly listed under `unknowns`. Partial shop branding is not filled in from expectation.
- Arrow directions describe the printed image; they are not current phone headings or safe route instructions. Ambiguous per-destination arrow associations remain null.
- Object boxes and mask boxes are image-pixel regions. They are manually approximate, not physical coordinates or exhaustive segmentation.
- Coordinates, physical sign IDs, current operational status and Cloud Anchor IDs stay unknown until mapped and verified.
- A wheelchair pictogram is a sign observation, not proof of an accessible route. A printed map is not automatically an interactive kiosk. A transit destination does not establish a train entrance or airport check-in counter.
- `related_observations` records exact source-image hash links; scene 006 and the first locker pilot refer to the same original photograph. This must not be counted as two independent places.

## Privacy and review provenance

Pilot privacy regions are conservative manual masks. Coarsely pixelated local previews were used to refine the regions while preserving fixtures. Masks may cover objects adjacent to people; those parts are not assessable. Masked full-frame views and enlarged sign details were visually inspected by the assistant. No human identity or activity descriptions are included. Independent human review of both privacy and annotation remains pending.

A local Windows FaceDetector was investigated but found only one face in these low-resolution samples, so it is not considered a reliable privacy solution here. `scripts/detect_faces_windows.ps1` is an exploratory local helper, not the basis for claiming complete redaction. OpenCV installation could not complete in this environment; a downloaded MobileNet-SSD model was not executed. Neither is a trained project model or a requirement for the running retrieval demo. Local helper binaries/model files are excluded from Git.

## Reproduce and continue

```powershell
C:/Python313/python.exe scripts/prepare_scene_pilot.py
C:/Python313/python.exe scripts/build_scene_records.py
C:/Python313/python.exe scripts/scene_rag_demo.py serve --port 8766
```

The first command requires the original second COCO archive at the project root. Add new image selections and review their full privacy views before authoring notes. Never propagate all details from one image to every image in its filename family. Check the exact source image/crop before accepting a relationship.

The demo uses lexical retrieval and bilingual amenity aliases; it does not execute an LLM. Its returned `context_for_llm` and `llm_instructions` can be consumed by the app's existing generative model. Ranking scores are not confidence percentages. Ordinary functional checks verify, among other things, that toilet signs do not become visible toilet entrances and that an Airport MRT query is not matched to airport buses.
