# Attribution and modifications

Original creator/uploader: **TibaMe** on Roboflow Universe.

Original dataset: **Taipei Station Sign Board 2**, version 1 (version dated 28 July 2023; original camera acquisition date unverified).

Source: https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2

Licence: **Creative Commons Attribution 4.0 International**, https://creativecommons.org/licenses/by/4.0/ . The source export declares this licence. Attribution does not imply endorsement by TibaMe or any station operator.

Modifications by **PHIT 2026 Finalist Team: 3rdEye4All** / Urav Advanced Learning Systems Pvt Ltd, 4 October 2026, for **AI Eye 4 All: AI Indoor Navigation for Inclusive Smart Cities.** Selected and cropped two locker-label evidence regions; added source hashes, image-relative boxes, amenity vocabulary, relationship candidates and explicit uncertainty/review fields. The manually chosen crops are not supplied COCO annotation boxes. No super-resolution or image synthesis was applied. The derived evidence and records in this package are offered under CC BY 4.0.

Full original filenames and their SHA-256 hashes are included in `amenity_pilot.jsonl`. Its evidence uses selected label crops; whole-scene evidence below uses separately masked photographs.

Whole-scene pilot extension: thirty-two source photographs have also been transformed by applying conservative manual person masks at native 512 × 288 resolution. New scene descriptions, readable sign text, destination-arrow associations, physical object observations, image-relative boxes and explicit coverage/uncertainty fields are provided in `scene_annotations.jsonl`, with hashes and mask regions in `scene_manifest.jsonl`. These are assistant-checked annotations with expert and independent privacy review pending. Airport buses, Taoyuan Airport MRT and Taipei Bus Station are separate semantic categories, not physical coordinates. They are adapted material under CC BY 4.0; the original unredacted full photographs are not included in this package.
