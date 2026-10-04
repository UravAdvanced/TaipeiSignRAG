# TaipeiSignRAG: A Linked Multilingual Signboard and Amenity Knowledge Base for Indoor Navigation Assistance

**Working draft — dataset audit and system design; full annotation and field deployment are in progress.**

**PHIT 2026 Finalist Team: 3rdEye4All**

**AI Eye 4 All: AI Indoor Navigation for Inclusive Smart Cities.**

**Affiliation:** Urav Advanced Learning Systems Pvt Ltd

**Individual authors and corresponding author:** to be supplied before submission.

**Draft date:** 5 October 2026

## Abstract

Indoor navigation assistants need to connect what a user sees with reliable information about destinations and amenities. Public station image datasets often provide detection boxes or class codes without the textual and relational descriptions needed for conversational assistance. We present the design and initial audit of TaipeiSignRAG, a linked knowledge base derived from three public Taipei Station signboard dataset exports. The archives contain 8,971 image entries spanning full-scene detection photographs and classification crops. Our audit identifies 1,684 filename-stem correspondences between one detection export and the classification export; sampled visual inspection supports using these as candidate scene–crop links, without establishing every match or physical sign identity. The proposed annotation workflow records visible multilingual text, destination–arrow associations, scene amenities, source evidence and uncertainty. The POC comprises 128 whole-scene annotations and two locker-evidence observations, covering 129 unique source photographs; expert review remains pending. Accepted records are intended to support retrieval-augmented navigation assistance before model fine-tuning. Spatial coordinates and anchor associations are explicitly separated from image semantics and will require a later station walkthrough. This draft reports source auditing, whole-scene annotation, a small local evidence-retrieval prototype and the planned app integration; it does not claim measured retrieval accuracy, pose correction or accessibility outcomes.

**Keywords:** indoor navigation; Traditional Chinese; sign understanding; retrieval-augmented generation; relational image annotation; amenities.

## 1. Introduction

Taipei Main Station presents a useful setting for studying sign-based indoor assistance because transit destinations, exits and services appear on closely spaced directional boards. Prior work by Yeh et al. already investigated pedestrian signage for positioning in Taipei Main Station, using 52 known signs [1]. Consequently, this work does not claim the first use of Taipei station signs for recognition or navigation.

Our immediate objective is narrower: transform existing image exports into an evidence-linked knowledge base that an assistant can query before any task-specific model training. A useful record should explain what is visible, which arrow belongs to which destination, what amenities appear in the scene, and which source image supports each statement. It should also distinguish observations from inferred translations and unknown physical locations. The intended application is the existing 3rDi4All indoor-navigation app, whose mapping and spatial alignment components are separate from the proposed semantic knowledge base.

The intended contribution comprises a unified provenance-preserving representation of three source exports; cross-image relationships that distinguish crops, similar layouts and verified physical identities; and a retrieval workflow that can supply grounded sign and amenity information. At this stage, source auditing, a 128-scene annotation pilot, two locker-evidence observations and a local retrieval prototype have been completed. Full annotation, live LLM integration and field use remain planned.

## 2. Related Work

The closest location-specific predecessor is Yeh, Jhang and Chang's *An intelligent indoor positioning system based on pedestrian directional signage object detection: a case study of Taipei Main Station* [1]. Their system uses existing pedestrian directional signs as visual location landmarks and smartphone imagery for sign detection and identification. The publisher's abstract reports 52 signs in the test area and identification accuracy as high as 98% over three test datasets containing 6,341 images in total. These are results reported for their sign-identification experiment, not measured positioning accuracy or results of TaipeiSignRAG. Their work motivates retaining sign identity and source evidence; our present contribution concerns multilingual transcripts, destination-arrow associations, surrounding amenities and evidence retrieval. The relationship between their experimental images and the three community exports used here has not been established. The article was published online on 8 October 2019 and appears in the 2020 journal volume.

Sign Language studies sign understanding for robot autonomy, including relationships between sign content and navigational meaning [2]. SignNav introduces semantic visual navigation guided by signage and a large-scale indoor environment dataset; its dataset design deliberately uses directional arrows without text to isolate spatial reasoning from OCR and text association [3]. These works establish that navigational sign understanding is an existing research area.

TextSLAM combines the semantic meaning and geometric structure of planar text features within a SLAM system [4]. Its scope is closer to geometric relocalisation than text retrieval alone. TS-1M, introduced in Traffic Sign Recognition in Autonomous Driving: Dataset, Benchmark, and Field Experiment, provides a large traffic-sign recognition resource and diagnostic benchmark [5]. It is not a source of Taipei indoor sign coordinates, and its verified title is not “Mitigating Visual SLAM Odometry Drift using Semantic Landmark Relocalization.”

Retrieval-augmented generation combines retrieved external information with language generation [6]. We adopt this general pattern for evidence-linked station records, without assuming that retrieval itself establishes a camera pose. Unlike the positioning study of Yeh et al. [1], the present source exports do not include a verified sign-location map. Unlike TextSLAM [4], the proposed initial demo does not modify a SLAM optimiser. The project therefore targets semantic data preparation and grounded assistance, with geometric integration deferred.

## 3. Data Sources and Audit

The first source is the Taipei Station Sign Board version 3 COCO export [7]. The second is the version 1 classification-folder export, Taipei Station Sign Board - CLS [8]. The third is Taipei Station Sign Board 2 version 1 in COCO format [9]. All three are community-published TibaMe exports, not independently surveyed station inventories. Their bundled metadata declares CC BY 4.0, whose attribution and modification-notice requirements must be retained when redistributing adapted material [10].

| Export | Image entries | Dimensions | Supplied annotation |
|---|---:|---|---|
| Sign Board V3 | 1,900 | 512 × 288 | 1,900 boxes; one populated generic category |
| Sign Board CLS V1 | 5,140 | 512 × 115 | 95 class folders; 4,112 train and 1,028 validation entries |
| Sign Board 2 V1 | 1,931 | 512 × 288 | 1,932 boxes; one populated generic category |
| Total | 8,971 | Mixed | No supplied semantic transcripts or metric map coordinates |

Every image decoded successfully. The CLS archive contains 101 excess exact duplicate entries, leaving 5,039 distinct image files within that export. Across all three archives there are 8,870 distinct file hashes. This count does not remove cropped counterparts or visually similar views and must not be reported as the number of independent photographs or installed signs.

The second detection export and CLS share 1,684 original filename stems. Six manually selected pairs, inspected visually by the assistant, depict corresponding full-scene and cropped views. These checks justify candidate links; they do not validate all stem matches. All 32 filename families in the second detection export occur in CLS. The first detection export has no shared filename stems with the second detection export, although this does not rule out related locations or sign content.

The second detection archive has 1,928 images with one box, two with two boxes and one without a box. One annotation begins at x = −0.01, a small boundary overrun that can be clamped in a derived copy. Original exports are preserved. Median annotated sign height is approximately 56 pixels in the first detection export and 44 pixels in the second, limiting reliable transcription of small text.

Visual review coverage differs from automatic file validation. Previous inspection covered all 1,900 first-export sign crops and 75 full frames; the CLS review sampled four images per class, 380 in total; the second-export review sampled three full frames per family, 96 in total. These are inspection counts, not performance results or complete semantic labels.

## 4. Proposed Annotation and Relational Representation

The planned schema separates an image observation, a semantic sign record and a physical map entity. Each image retains its source archive, original path, hash, dimensions and supplied annotations. Text is transcribed by panel where legible, with an explicit language tag. Visible English is separated from an English translation generated from Chinese. Normalised amenity names are likewise distinguished from literal text. Unreadable content remains unknown.

Destination–arrow records associate a specific destination or panel with its visible direction. Scene descriptions include stable, useful objects such as locker banks, entrances or ticket machines only when supported by the source image. A directional sign mentioning an amenity and a photograph showing that amenity are different evidence types. Neither establishes service availability, pricing or an accessible route.

Relations between observations include candidate same-source crop pairs, matching sign layouts, possible signage revisions and physically verified landmark identities. Filename codes are retained as source labels and are not interpreted as coordinates. Identical codes across exports can show different layouts, while identical messages can occur at multiple locations. Physical identity therefore remains unresolved until adequate corroborating evidence is available.

Annotation will proceed interactively in Codex using saved batches and image-level checkpoints. The execution record should identify the model when verifiable, annotation instructions, source images, transformations and reviewer type. Model-generated drafts, assistant visual checks and expert review must remain distinguishable. The workflow does not treat an assistant's review as independent human validation.

Before submitting images to a remote model context, local crops or masking should remove people from the derived annotation inputs. Original source material is preserved privately with its provenance. Evidence crops in a public release must be checked separately, and the release must describe the transformations applied. This draft does not claim that all source images have already been redacted.

## 5. Initial Whole-Scene and Amenity Pilot

### Resources, masking and measured batch time

Local preparation, mask rendering, export generation and validation use an HP OMEN Laptop 15-en0xxx with an AMD Ryzen 7 4800H processor (8 cores, 16 logical processors), 16,495,308,800 bytes of OS-reported physical memory (approximately 15.36 GiB), and Windows 11 Home Single Language, build 10.0.26200. Installed graphics include an NVIDIA GeForce RTX 2060 and AMD Radeon graphics; the mask-rendering pipeline runs on the CPU and does not use GPU inference. Software versions recorded on 5 October 2026 are Python 3.13.5, Pillow 12.0.0, Node.js 20.19.4 and Git 2.56.0.windows.1. Microsoft Edge was used for browser checks, and GitHub/GitHub Pages host the repository and published static demo. Cloud serving hardware is provider-managed and was not measured.

OpenAI Codex is the interactive environment used to inspect exact photographs, specify image-coordinate mask rectangles and edit annotation records [11]. The team reports Microsoft Foundry and Azure OpenAI GPT-6 Astra with medium reasoning among its project resources [12][13]. This resource acknowledgement is separate from the saved local batch execution record; these checkpoints do not contain Azure request identifiers or metered token usage. Medium is a supported GPT-6 Astra reasoning setting [14]. Each new photograph receives one annotation/basic-masking pass, with no second visual pass from scene 072 onward. `scripts/prepare_scene_pilot.py` applies the recorded rectangles through Pillow `ImageDraw.rectangle`, replacing their pixels with RGB (45, 45, 45). The downloaded MobileNet-SSD model was not executed and did not generate these masks. A preliminary Windows FaceDetector experiment was not adopted. Mask coordinates, source hashes and review status are retained per image; independent expert/privacy review remains pending.

The timed 19-photo batch, scenes 091–109, took **761 seconds (12 minutes 41 seconds)** on 5 October 2026: 21:51:11–22:03:52 UTC on 4 October, corresponding to 03:21:11–03:33:52 IST on 5 October. This is approximately **40.1 seconds per photograph**, including preparation, single-pass annotation and masking, saving, exports, documentation, automated validation and a Windows permission wait. It excludes push/deployment and the final timing-entry write. Validation passed 375 Python/JavaScript search-parity cases plus source-hash, mask-pixel, count and HTTP-route checks. This is one observed workflow duration, not a controlled throughput benchmark or a full-collection completion forecast. The checkpoint reached 109 scenes and two locker observations covering 110 unique originals, leaving 8,861 source entries without new annotations.

### GPT-6 Astra batch-cost planning estimate

A subsequent instrumented local run at the 128-scene checkpoint measured **16.902 seconds** for `prepare_scene_pilot.py`, which regenerates all 128 masked full frames, enlarged previews and the contact sheet; **0.589 seconds** for record, browser and site exports; and **5.931 seconds** for integrity/search checks. The total was **23.422 seconds**. These timings exclude image inspection, transcription, scene-description writing, mask-coordinate selection, documentation edits and permission waits. They measure complete scripts, not rectangle filling in isolation. Existing images are regenerated too, so rendering overhead grows with corpus size. The original 761-second batch measurement remains an end-to-end workflow observation.

At the observed 761/19 seconds per photograph, a simple linear projection is **89.0 hours for 8,000 photographs** and **98.6 hours for the 8,861 remaining entries at that checkpoint** (approximately 11.1 and 12.3 eight-hour working days). This extrapolates the complete interactive workflow, not CPU rectangle-rendering time. The individual stages were not separately timed in that batch, so it does not establish a measured bottleneck. The remaining collection includes crops and repeated views with different workloads; interruptions, difficult text and independent expert review can change the total substantially. These figures assume comparable per-entry effort and are not an unattended completion schedule.

For a rough reproducible estimate, use the published OpenAI standard short-context GPT-6 Astra rates of **USD 10 per million uncached input tokens** and **USD 50 per million output tokens**, checked on 5 October 2026 [14]. Output budgets below include reasoning tokens, which are billed as output tokens [15]. These are reference API prices, not a verified Azure subscription tariff or an observed Codex charge: the retrieved Azure pricing page displayed dynamic price placeholders, and actual deployment-region pricing and startup-credit deductions were not available [16].

| Planning scenario for 19 photos | Total billable input tokens | Total output tokens, including reasoning | Estimated gross cost (USD) | Cost per photo (USD) |
|---|---:|---:|---:|---:|
| Compact requests | 30,000 | 10,000 | 0.80 | 0.042 |
| Working budget | 60,000 | 20,000 | 1.60 | 0.084 |
| Larger context/reasoning budget | 120,000 | 40,000 | 3.20 | 0.168 |

The formula is `cost_USD = input_tokens * 10 / 1,000,000 + output_tokens * 50 / 1,000,000`. Input budgets include images, instructions, returned tool text and any conversation context sent again across requests; they are illustrative assumptions, not measured image-token counts. Medium reasoning does not fix the number of reasoning tokens. **USD 1.60 per 19-photo batch is a working budget, with USD 0.80–3.20 shown as scenario sensitivity rather than a confidence interval or maximum.** Larger histories or retries can exceed it. No caching, credits, taxes, subscription allocation, tool fees, priority/Fast pricing or Batch/Flex discount is assumed. Each request is assumed to remain within 272,000 input tokens; the published long-context premiums apply above that threshold. An annotation batch here means a saved group of 19 photographs and does not imply use of a discounted Batch API. Replace these assumptions with measured usage and the applicable Azure tariff when available.

The 128 full-frame records inspect surroundings as well as the supplied sign box. Fourteen amenity categories are assigned explicit evidence statuses: visible, sign reference only, uncertain, or not observed in assessable regions. The records include directly observed barrier gates, stairs and escalator structures, shopfronts including two readable retail names, map boards and passage entrances. Toilet references occur on signs in six records, while an actual toilet entrance is not established. No lift or check-in counter is verified in these 128 images. These are pilot observations, not station-wide absence claims. Conservative manual person masks preserve much of the surrounding scene but make covered regions unassessable; independent privacy review remains pending.

Two inspected photographs in the A10E filename family of Sign Board 2 contain a blue label reading “LOCKERS,” with locker units visible in the surrounding scene. The relevant stems are A10E_HH_001 and A10E_YY_016. The local pilot contains two observation records and tight label crops, each linked to its original filename and hash. Their review status is “visually checked by assistant”; expert review is pending.

This supports an answer such as: “Lockers are visible in the historical photographs associated with this sign group.” It does not support “a locker is available now,” a metric locker position, or a verified wheelchair-accessible approach. The two views are candidate observations of the same amenity, not two confirmed separate locker locations. No attempt has yet been made to enumerate every locker image in the collection.

The pilot's normalised Chinese amenity name is an annotation vocabulary entry, not a claim that every Chinese character was transcribed from the cropped panel. Original and normalised text fields are separate to prevent this distinction from disappearing during retrieval or later training.

## 6. Immediate Retrieval and App Integration

The implemented browser-side Chinese/English retrieval prototype uses lexical matching and bilingual aliases over 128 scene records, with an optional local Python API. Static assets support a GitHub Pages repository prefix; the demo and destination catalogue are deployed, with subsequent updates published at annotation milestones. Airport buses, Taoyuan Airport MRT and Taipei Bus Station have separate semantic destination identifiers. In scene 011, Taipei Bus Station points left and airport buses point upward on the same board. Printed English “Airport Express” is retained on the bus panel without treating it as an MRT identity. Structured observation fields allow queries to distinguish physically visible facilities from sign references. Optional semantic embeddings and visual candidate matching remain future extensions. Accepted records, source evidence and uncertainty should be retrieved together. The prototype exports source-linked context and grounding instructions for a downstream language model; it does not itself execute a live generative model. A later app integration can use that evidence to answer questions about signs and amenities, following the broad retrieval-augmented generation pattern [6]. This functionality does not require fine-tuning a new VLM.

Map positions and Cloud Anchor IDs are nullable fields until they have been registered during mapping. ARCore camera poses represent session-relative estimates; the platform documentation warns that numerical world coordinates can change as environmental understanding is updated and recommends anchors or coordinates relative to nearby anchors for persistence [17]. The camera's capture position is also distinct from the position of an observed sign.

For a later integration, recognition can retrieve candidate registered Cloud Anchor IDs. Cloud Anchor resolution compares current visual features against a previously hosted 3D feature map [18]. Successful resolution can establish a spatial relationship for the app. Semantic retrieval selects candidates and supplies explanations; geometric resolution supplies spatial evidence. A sign match alone must not trigger a camera-pose correction or be described as a SLAM loop closure.

## 7. Planned Walkthrough and Release

A small Taipei Main Station walkthrough is planned after the annotation and app pipeline are ready. It will record current observations, confirm physical sign and amenity identities, and associate selected entities with the app's registered anchors. It has not been conducted. The walkthrough must preserve the difference between camera capture poses, mapped object positions and anchor-relative observations. A saved trajectory is not independent ground truth for its own drift.

The GitHub repository is public and the curated demo and destination catalogue are deployed on GitHub Pages. The local project now includes code, schema documentation, provenance, whole-scene pilot records and the working paper. A separately prepared Hugging Face dataset package will contain accepted records and appropriately attributed evidence assets. The current local package contains 128 whole-scene records and two locker observations; it is not the complete 8,971-entry annotation collection. A separate Hugging Face dataset publication has not been completed.

## 8. Limitations and Current Status

Source imagery is low resolution, historical capture dates are not independently established, and source codes are not surveyed positions. Repeated views and crop overlap limit claims about data diversity. Semantic records can become stale when signs or amenities change. Small characters, occlusion and perspective can produce incorrect model outputs, requiring explicit uncertainty and review.

The completed work is archive auditing, sampled visual inspection, 128 whole-scene annotations, two locker observations and a local evidence-retrieval demo. Full annotation, live LLM integration, model adaptation, station testing and user studies remain incomplete. No retrieval accuracy, on-device latency, navigation success, drift reduction or accessibility benefit is reported. The intended application includes assistance for visually impaired users, but suitability for that use has not been established by this draft.

The immediate next work is broader scene annotation, independent review of the pilot and connection of the exported retrieval context to the app's LLM. Any later paper claiming spatial improvement must report actual geometric implementation and measured evidence. The current contribution should be read as dataset curation and system design, not a demonstrated replacement for geometric localisation.

## Acknowledgements

We thank Microsoft for Startups Hub for subscription support [19], and acknowledge Microsoft Foundry, Azure OpenAI GPT-6 Astra at medium reasoning, and OpenAI Codex among the resources supporting project development [12][13][14][11]. We especially acknowledge the Taipei Main Station pedestrian-signage positioning work of Chun-Chao Yeh, Ke-Jia Jhang and Chin-Chun Chang [1], alongside the attributed TibaMe dataset sources.


## References

[1] Chun-Chao Yeh, Ke-Jia Jhang, Chin-Chun Chang. **An intelligent indoor positioning system based on pedestrian directional signage object detection: a case study of Taipei Main Station**. Mathematical Biosciences and Engineering, 17(1): 266–285. 2020. DOI: 10.3934/mbe.2020015.  https://www.aimspress.com/article/10.3934/mbe.2020015

[2] Ayush Agrawal, Joel Loo, Nicky Zimmerman, David Hsu. **Sign Language: Towards Sign Understanding for Robot Autonomy**. 2025. arXiv:2506.02556.  https://arxiv.org/abs/2506.02556

[3] Jian Sun, Yuming Huang, He Li, Shuqi Xiao, Shenyan Guo, Maani Ghaffari, Qingbiao Li, Chengzhong Xu, Hui Kong. **SignNav: Leveraging Signage for Semantic Visual Navigation in Large-Scale Indoor Environments**. 2026. arXiv:2603.16166.  https://arxiv.org/abs/2603.16166

[4] Boying Li, Danping Zou, Yuan Huang, Xinghan Niu, Ling Pei, Wenxian Yu. **TextSLAM: Visual SLAM With Semantic Planar Text Features**. IEEE Transactions on Pattern Analysis and Machine Intelligence. 2023. DOI: 10.1109/TPAMI.2023.3324320. Online publication 2023; issue metadata should be checked before submission. https://arxiv.org/abs/2305.10029

[5] Guoyang Zhao, Weiqing Qi, Kai Zhang, Chenguang Zhang, Zeying Gong, Zhihai Bi, Kai Chen, Benshan Ma, Ming Liu, Jun Ma. **Traffic Sign Recognition in Autonomous Driving: Dataset, Benchmark, and Field Experiment**. 2026. arXiv:2603.23034.  https://arxiv.org/abs/2603.23034

[6] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**. 2020. arXiv:2005.11401. NeurIPS 2020. https://arxiv.org/abs/2005.11401

[7] TibaMe. **Taipei Station Sign Board Dataset, version 3, COCO export**. Roboflow Universe. n.d.. CC BY 4.0. Local archive audited 4 October 2026. Acquisition date not verified. https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board

[8] TibaMe. **Taipei Station Sign Board - CLS Dataset, version 1**. Roboflow Universe. 2023. CC BY 4.0. Local archive audited 4 October 2026. Version date 30 July 2023; acquisition date not verified. https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-cls

[9] TibaMe. **Taipei Station Sign Board 2 Dataset, version 1, COCO export**. Roboflow Universe. 2023. CC BY 4.0. Local archive audited 4 October 2026. Version date 28 July 2023; acquisition date not verified. https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2

[10] Creative Commons. **Attribution 4.0 International (CC BY 4.0)**. n.d.. Accessed 4 October 2026. https://creativecommons.org/licenses/by/4.0/

[11] OpenAI. **Codex and ChatGPT developer documentation**. n.d.. Accessed 5 October 2026; URL redirects to current product documentation. https://developers.openai.com/codex/

[12] Microsoft. **What is Microsoft Foundry?**. n.d.. Accessed 5 October 2026. https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry

[13] Microsoft. **Foundry Models sold by Azure**. n.d.. Includes Azure OpenAI GPT-6 Astra. Accessed 5 October 2026. https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models

[14] OpenAI. **GPT-6 Astra model: capabilities, reasoning settings and pricing**. n.d.. Standard short-context reference pricing: USD 10 per million uncached input tokens and USD 50 per million output tokens. Accessed 5 October 2026. https://developers.openai.com/api/docs/models/gpt-6-astra

[15] OpenAI. **Reasoning models**. n.d.. Reasoning tokens are billed as output tokens. Accessed 5 October 2026. https://developers.openai.com/api/docs/guides/reasoning

[16] Microsoft. **Azure OpenAI Service pricing**. n.d.. Accessed 5 October 2026. Retrieved page displayed dynamic price placeholders; subscription-specific numerical rates were not established. https://azure.microsoft.com/en-us/pricing/details/azure-openai/

[17] Google. **ARCore SDK for Android: Pose**. n.d.. Developer documentation. Accessed 4 October 2026. https://developers.google.com/ar/reference/java/com/google/ar/core/Pose

[18] Google. **Introduction to Cloud Anchors**. n.d.. Developer documentation. Accessed 4 October 2026. https://developers.google.com/ar/develop/cloud-anchors

[19] Microsoft. **Microsoft for Startups**. n.d.. Programme information. Subscription support is team-reported. Accessed 5 October 2026. https://www.microsoft.com/en-us/startups
