---
pretty_name: TaipeiSignRAG — draft amenity pilot
language:
  - en
  - zh
license: cc-by-4.0
size_categories:
  - n<1K
tags:
  - taipei-main-station
  - indoor-navigation
  - traditional-chinese
  - signage
  - amenities
  - draft
configs:
  - config_name: amenity_pilot
    data_files:
      - split: train
        path: amenity_pilot.jsonl
---

# TaipeiSignRAG: draft amenity pilot

**Prepared locally; not yet published.** PHIT2026Team, Urav Advanced Learning Systems Pvt Ltd.

This package currently contains **two assistant-checked locker observations**, each with a tightly cropped label image and provenance back to the source photograph. It is not the completed signboard knowledge base. The split name `train` is a Hub loading convention; no training or evaluation split has been designed and no model was trained on this pilot.

The source photographs are from [TibaMe's Taipei Station Sign Board 2, version 1](https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2), which declares CC BY 4.0. The photographs show locker signage, including the word “LOCKERS,” on the right side of the frame. Their original stems are A10E_HH_001 and A10E_YY_016. We provide cropped evidence and new structured observation records. Source photos and crops can show the same physical amenity; that identity is not established.

## Contents

- `amenity_pilot.jsonl`: two observation records.
- `images/locker_evidence_01.png` and `images/locker_evidence_02.png`: native-resolution label crops.
- `ATTRIBUTION.md`: original source, licence and modification notice.

The `evidence_image` field is a path relative to this package. A JSON loader may treat it as text unless explicitly converted to an image feature. No automatic image-viewer behaviour has been verified on the Hub.

## Annotation meaning

`visible_text` contains the visually read English label. `normalized_names` is an English/Traditional Chinese annotation vocabulary; it is not a verbatim multilingual transcription. `evidence_bbox_xyxy` locates the manually selected label crop in the original 512 × 288 photograph. It is not an original COCO sign box or a physical coordinate.

Source archive, filename, SHA-256, review date and review type are recorded. `review_status` is `visually_checked_by_assistant`; `human_review_status` remains `pending`. Both records have unknown physical amenity ID, map coordinate, Cloud Anchor ID, current availability, capture date and wheelchair accessibility.

## Intended use and limits

The pilot illustrates how an indoor assistant could retrieve image-supported amenity knowledge. It supports “a locker label appears in this historical photograph.” It does not establish exact user position, route safety, available locker capacity, pricing, current operations or accessibility. It is not sufficient to train or validate a navigation model.

No new scene photography was collected for this package. Tight local crops exclude people from these released evidence images; the original source archives may contain people and are not included here. The larger project's full annotation and current station walkthrough are pending.

## Citation

Until a paper or archived release is published, cite this as a working project and cite the original TibaMe source. No DOI, accepted paper or public repository is claimed.

```bibtex
@misc{tibame_signboard2,
  author = {{TibaMe}},
  title = {Taipei Station Sign Board 2 Dataset},
  year = {2023},
  howpublished = {Roboflow Universe},
  url = {https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2},
  note = {Version 1. CC BY 4.0. Cropped and annotated in TaipeiSignRAG.}
}
```

The user will choose the Hugging Face namespace and upload the package when the broader dataset is ready.
