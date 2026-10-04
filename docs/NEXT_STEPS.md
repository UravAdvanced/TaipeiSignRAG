# Next steps

1. Expand the completed eight-scene Codex pilot to more groups and both full-frame source exports. Include scene/crop pairs and useful amenities. Keep the two locker observations as evidence records; one shares an original photo with scene 006.
2. Independently review the pilot's readable text, arrow associations, physical-object labels and privacy masks. The current schema separates sign-only references, visible objects, uncertainty and not-observed regions. Assistant checking is not human review.
3. Connect the running local retrieval/context demo to the app's existing LLM. The current demo shows evidence and prepares a context payload but does not execute generation. No fine-tuning is needed for this step.
4. Continue annotation in checkpointed batches. Leave coordinates and Cloud Anchor IDs empty until the actual environment is mapped. Class codes and retrieval scores are not coordinates.
5. When the pipeline and app are ready, perform the user-proposed small Taipei Main Station walkthrough. Confirm current signs and lockers, their physical identities and their association with registered app anchors. This is future work, not scheduled or executed now.
6. Update the working paper with actual implementation/results and final authors. GitHub is connected and the initial commits were pushed; use the user's terminal for new pushes while the sandbox cannot access its keyring. The user will publish the Hugging Face dataset when ready.

The first practical deliverable is a working knowledge-base demo; a new trained model is optional later. No station test, exact-location accuracy or accessibility benefit is claimed yet.
