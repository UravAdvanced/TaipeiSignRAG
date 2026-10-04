# Annotation and immediate RAG workflow

**Selected execution, updated 2026-10-04:** the user confirmed direct Codex annotation/review with file checkpoints. The Azure comparison below is an optional alternative, not a required next step. Before annotation starts, the user requested discussion of a semantic relocalisation extension; see `SEMANTIC_RELOCALIZATION_REVIEW.md` for verified papers and corrections.

## Selected scope

Build a reviewed relational sign knowledge base from the three supplied Taipei station exports. Use it immediately for camera-conditioned or conversational retrieval in 3rDi4All; reuse accepted records for later VLM training. A specific Taiwan-first or worldwide-first claim is not established.

## Intended preparation

1. Preserve archive, filename and annotation provenance; identify exact duplicates and candidate scene/crop pairs.
2. Crop or mask people locally before any cloud inference when people must be excluded. A prompt to ignore people does not remove them from the input.
3. Present full scene and readable sign crops to the annotator. Record visible text verbatim, languages, arrows associated with individual destinations, symbols, and relevant non-person scene clues. Mark unreadable text unknown; distinguish visible English from newly translated English.
4. Propose cross-image relationships separately: same source photograph/crop, matching message/layout, and same physical board. Accept physical identity only with sufficient evidence. Class codes alone are not proof.
5. Review representative sign records and uncertain cases; record review status and evidence. Model-generated labels are drafts, not automatically verified ground truth.
6. Index accepted records for retrieval. Return source images, sign IDs and evidence along with answers.
7. During app mapping, attach confirmed physical sign IDs to registered map anchors. Location and routes come from the app's map/anchor system, not the RAG score.

## Intended record fields

`image_id`, source archive/path and hash, original class/code, bounding box, candidate/verified `sign_id`, verbatim text by panel, language, translated text with provenance, destination-arrow relations, symbols, scene description, related-image IDs with relation/evidence, model/deployment/version, annotation status, review notes, optional app map/anchor ID.

All schema and pipeline work above is planned; no full annotation collection exists yet.

## Azure versus Codex

- Azure GPT-6 Astra: recommended for the full annotation run. An API script can save one record per image, resume failures, enforce an output schema and keep a reproducible model/deployment record. Managed API inference does not use the user's T4. Actual runtime, cost and account quota are unmeasured.
- Codex session: suitable for preparing code, interactive image inspection, designing the schema and manually reviewing a pilot. It should not be described as an unlimited unattended inference endpoint or assumed to have the user's Azure deployment credentials. The session's selected model and the Azure deployment are separate execution contexts.
- The source images contain small/blurred text. Neither path guarantees exact transcription. Do not invent characters, directions or physical coordinates to complete a record.

Next implementation step: a small reviewed pilot that fixes the schema and matching rules before starting the complete run. No model fine-tuning is necessary for the initial knowledge-base demo.
