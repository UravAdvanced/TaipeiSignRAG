# Attribution and modifications

Original creator/uploader: **TibaMe** on Roboflow Universe.

Original dataset: **Taipei Station Sign Board 2**, version 1 (version dated 28 July 2023; original camera acquisition date unverified).

Source: https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2

Licence: **Creative Commons Attribution 4.0 International**, https://creativecommons.org/licenses/by/4.0/ . The source export declares this licence. Attribution does not imply endorsement by TibaMe or any station operator.

Modifications by PHIT2026Team / Urav Advanced Learning Systems Pvt Ltd, 4 October 2026: selected and cropped two locker-label evidence regions; added source hashes, image-relative boxes, amenity vocabulary, relationship candidates and explicit uncertainty/review fields. The manually chosen crops are not supplied COCO annotation boxes. No super-resolution or image synthesis was applied. The derived evidence and records in this package are offered under CC BY 4.0.

Full original filenames and their SHA-256 hashes are included in `amenity_pilot.jsonl`. The original images contain broader context and may contain people; only the selected label crops are included in this pilot.

Whole-scene pilot extension: eight source photographs have also been transformed by applying conservative manual person masks at native 512 × 288 resolution. New scene descriptions, readable sign text, destination-arrow associations, physical object observations, image-relative boxes and explicit coverage/uncertainty fields are provided in `scene_annotations.jsonl`, with hashes and mask regions in `scene_manifest.jsonl`. These are assistant-checked annotations with human review pending. They are adapted material under CC BY 4.0; the original unredacted full photographs are not included in this package.
