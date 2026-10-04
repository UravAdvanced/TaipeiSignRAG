# Next steps

1. Start a Codex annotation pilot across several distinct sign layouts, with scene/crop pairs and useful amenities. Keep the two existing locker observations as a schema example; do not count them as complete sign transcriptions.
2. Fix the schema after inspecting the pilot: visible multilingual text, destination-arrow relations, observed amenities, evidence regions, image links, uncertainty and review provenance. Distinguish assistant checking from human review.
3. Build a small local retrieval demo over accepted records. Return evidence images and sign IDs alongside generated answers. No fine-tuning is needed for this step.
4. Continue annotation in checkpointed batches. Leave coordinates and Cloud Anchor IDs empty until the actual environment is mapped. Class codes and retrieval scores are not coordinates.
5. When the pipeline and app are ready, perform the user-proposed small Taipei Main Station walkthrough. Confirm current signs and lockers, their physical identities and their association with registered app anchors. This is future work, not scheduled or executed now.
6. Update the working paper with actual implementation/results and final authors. Connect GitHub after renewing authentication; the user will publish the Hugging Face dataset when ready.

The first practical deliverable is a working knowledge-base demo; a new trained model is optional later. No station test, exact-location accuracy or accessibility benefit is claimed yet.
