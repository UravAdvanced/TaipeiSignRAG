# TaipeiSignRAG: Evidence-Linked Sign and Amenity Annotations for Indoor Navigation Assistance

**Preprint draft | 5 October 2026**  
**3rdEye4All team, Urav Advanced Learning Systems Pvt Ltd**  
**Corresponding author:** Team

## Abstract

Indoor navigation assistants need more than sign-detection boxes: they need readable destination names, associated arrows, visible facilities, and evidence for each statement. We present a small proof of concept (POC) that turns public Taipei Main Station signboard images into structured, bilingual scene annotations for retrieval. The source archives contain 8,971 image entries. The POC records 204 whole-scene observations and two additional locker-evidence observations, covering 205 source photographs. We demonstrate a checkpointed annotation and export workflow, a browser-based lexical search prototype, and a four-image comparison of annotation prompts and API image inputs. Broader instructions increase output detail, while API outputs vary across input representations and can still misidentify destinations; these trials do not establish an accuracy ranking. API usage supports a reference-price estimate of USD 0.50–0.57 for the four-image runs, but the actual Azure bill and the interactive POC's per-request usage are unavailable. The POC is closed as a pipeline demonstration, not as a complete or human-verified station dataset. Human verification and app integration are future work.

**Keywords:** indoor navigation; sign annotation; Traditional Chinese; evidence retrieval; scene description.

## 1. Motivation and contribution

Directional sign datasets commonly provide image boxes or class labels. Those labels do not say which destination belongs to which arrow, whether a facility is physically visible or only mentioned on a sign, or how uncertain a small-text reading is. These distinctions matter when a navigation assistant retrieves evidence for a user's question. Our annotations connect bilingual text, destination-arrow relations, surrounding objects, uncertainty, and source-image provenance.

Sign-based navigation has prior work at Taipei Main Station, including pedestrian-sign positioning by Yeh et al. [1]. Sign understanding for navigation and semantic visual navigation are active research areas [2]. TaipeiSignRAG does not claim a new localization method. Its contribution is an inspectable annotation and evidence-retrieval workflow that can supply structured context to a later retrieval-augmented assistant [3].

## 2. Data and annotation workflow

We audited three community-published TibaMe exports: Sign Board V3 (1,900 images), Sign Board CLS V1 (5,140), and Sign Board 2 V1 (1,931), for 8,971 entries in total [4][5][6]. The entries include repeated views and crops; they are not 8,971 independent signs or locations. The source releases declare CC BY 4.0, so attribution and modification notices must be retained [7].

The POC annotated 204 full-frame images from Sign Board 2 and created two separate locker-evidence observations linked to source photographs. Together these records cover 205 unique source photographs, not 205 unique physical signs. Different-angle photographs of the same apparent sign or area remain separate observations rather than being collapsed by repeated exit text or filename family. Complementary views can give retrieval multiple provenance-linked evidence items; after human verification and confirmed cross-view links, they could provide view-diverse examples for model training. This POC did not train a model or evaluate that benefit. Each scene record captures readable Traditional Chinese and English text, supported arrow associations, relevant visible objects or facilities, and explicit unknowns. It distinguishes a facility shown in the photograph from one merely named on a sign, and keeps translations separate from literal transcription. Source filenames, hashes, evidence references, and review status accompany the records.

The workflow audits source files, inspects one photograph at a time, saves structured records at image-level checkpoints, then exports JSONL records and browser-search data. The release contains 128 records with derived image evidence and 76 metadata-only records. Structural and search-parity checks were recorded; they do not verify Chinese readings or prove every semantic interpretation. The annotations were visually checked by the assistant; the human-reviewed record count is zero.

The local browser prototype searches Chinese and English with lexical matching and aliases. It also indexes three separately supplied demo photographs, including an M3 sign reading Cosmos Hotel; these examples are outside the 204-scene core dataset and do not change its count. It distinguishes Taipei Bus Station, Taoyuan Airport MRT, and airport buses, and can return evidence about visible facilities separately from sign references. It has no live generative model and has not been evaluated for retrieval accuracy.

## 3. Four-image prompt and API comparison

Four photographs (scenes 003, 006, 029, and 190) were used in prompt and API trials. Results are descriptive: the interactive prompt comparison was not blinded or independent, and no expert ground truth was prepared. Exact prompts, settings, per-image findings, and reproducibility artifacts are published in the [GitHub prompt and comparison documentation](https://github.com/UravAdvanced/TaipeiSignRAG/tree/main/docs).

| Trial | Four-image elapsed time | Observed result |
|---|---:|---|
| Expanded prompt, interactive Codex annotation | 678.189 s (11 min 18 s) | Sign entries rose from 17 to 25 and object entries from 9 to 24; shared-field text grew about 2.41 times. Some facts were split or reorganized, so counts are not recall or accuracy. |
| Short baseline prompt, Azure API, 512×288 JPEG | 97.393 s | 4,032 input and 10,549 output tokens, including reasoning. |
| Same short prompt and API settings, 1536×864 resized PNG | 80.918 s | 8,296 input and 8,425 output tokens, including reasoning. |

The API runs used three concurrent requests and the same short prompt, schema, requested model, and reasoning setting. Resizing adds no captured detail, and the comparison also changes JPEG to PNG. With four images and no repeated or expert-scored trials, the 16.9% lower elapsed time in the enlarged-input run is not evidence of a general speed or quality benefit. Outputs were mixed: the enlarged run recovered major labels in scenes 003 and 029, misread Taipei Bus Station as Taipei Main Station in scene 006, and still could not read the blurred central destinations in scene 190.

At published standard reference rates of USD 10 per million input tokens and USD 50 per million output tokens [8], the token totals correspond to estimated gross prices of **USD 0.57** for the native-input run and **USD 0.50** for the enlarged-input run. Reasoning tokens are included in output usage [9]. These are price-equivalent estimates, not Azure invoices. The interactive annotation POC ran in Codex; per-request usage and marginal subscription cost were not recorded, so a total billed cost for creating the 204 records cannot be reported.

The expanded prompt required more interactive authoring time than the short API runs, but the workloads and execution methods differ. No controlled speed ratio between prompting styles or annotation systems is claimed. The detailed reports preserve timing definitions and limitations.

## 4. Status, limitations, and future development

The POC is closed at 204 scene records and two locker-evidence observations. It demonstrates converting source images into structured evidence and exposing it through a small search prototype. It does not complete the 8,971-entry collection, establish station-wide facility coverage, or measure annotation accuracy, navigation success, accessibility benefit, or localization performance. Images are low resolution, some text is blurred, and repeated views limit conclusions about distinct physical locations.

The next development phase is human verification of Chinese and English text, translations, arrow associations, facility descriptions, uncertainty, and privacy handling. After verification, reviewed records can be connected to the 3rDi4All app as semantic descriptions for user-confirmed mapped waypoints. Map or anchor associations must be verified separately. Semantic retrieval alone does not establish a user's position, correct map drift, or prove an accessible route. No app integration or field evaluation is reported here.

## Acknowledgements

We acknowledge Microsoft for Startups Hub for subscription support, and the use of Microsoft Foundry, Azure OpenAI GPT-6 Astra, and OpenAI Codex in project development. We thank the authors of the Taipei Main Station sign-positioning study for related work and acknowledge TibaMe as the source of the audited image exports.


## References

[1] Chun-Chao Yeh, Ke-Jia Jhang, Chin-Chun Chang. **An intelligent indoor positioning system based on pedestrian directional signage object detection: a case study of Taipei Main Station**. Mathematical Biosciences and Engineering, 17(1): 266–285. 2020. DOI: 10.3934/mbe.2020015.  https://www.aimspress.com/article/10.3934/mbe.2020015

[2] Jian Sun, Yuming Huang, He Li, Shuqi Xiao, Shenyan Guo, Maani Ghaffari, Qingbiao Li, Chengzhong Xu, Hui Kong. **SignNav: Leveraging Signage for Semantic Visual Navigation in Large-Scale Indoor Environments**. 2026. arXiv:2603.16166.  https://arxiv.org/abs/2603.16166

[3] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**. 2020. arXiv:2005.11401. NeurIPS 2020. https://arxiv.org/abs/2005.11401

[4] TibaMe. **Taipei Station Sign Board Dataset, version 3, COCO export**. Roboflow Universe. n.d.. CC BY 4.0. Local archive audited 4 October 2026. Acquisition date not verified. https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board

[5] TibaMe. **Taipei Station Sign Board - CLS Dataset, version 1**. Roboflow Universe. 2023. CC BY 4.0. Local archive audited 4 October 2026. Version date 30 July 2023; acquisition date not verified. https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-cls

[6] TibaMe. **Taipei Station Sign Board 2 Dataset, version 1, COCO export**. Roboflow Universe. 2023. CC BY 4.0. Local archive audited 4 October 2026. Version date 28 July 2023; acquisition date not verified. https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2

[7] Creative Commons. **Attribution 4.0 International (CC BY 4.0)**. n.d.. Accessed 4 October 2026. https://creativecommons.org/licenses/by/4.0/

[8] OpenAI. **GPT-6 Astra model: capabilities, reasoning settings and pricing**. n.d.. Standard short-context reference pricing: USD 10 per million uncached input tokens and USD 50 per million output tokens. Accessed 5 October 2026. https://developers.openai.com/api/docs/models/gpt-6-astra

[9] OpenAI. **Reasoning models**. n.d.. Reasoning tokens are billed as output tokens. Accessed 5 October 2026. https://developers.openai.com/api/docs/guides/reasoning
