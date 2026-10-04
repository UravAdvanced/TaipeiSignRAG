# Taipei Main Station Signboard Annotation and Relational Dataset

**PHIT 2026 Finalist Team: 3rdEye4All**

**AI Eye 4 All: AI Indoor Navigation for Inclusive Smart Cities.**

Urav Advanced Learning Systems Pvt Ltd.

TaipeiSignRAG is the Taipei Main Station whole-photograph annotation POC and bilingual evidence-search demo. Human review is pending. It does not establish precise positioning, current facilities or accessible routes.

## Whole-scene pilot and local demo

128 whole-photograph annotations now cover readable signs **and** surrounding objects. Observed examples include a locker bank, barrier gates, stairs/escalators, a shopfront, map boards and passage entrances. Fourteen amenity categories are explicitly checked per scene. A toilet mentioned on a sign is kept separate from a physically visible toilet. No lift or check-in counter is verified in this pilot.

**Airport buses / 機場巴士, Taoyuan Airport MRT / 桃園機場捷運, and Taipei Bus Station / 臺北轉運站 are separate destinations.** Scene 011 shows different arrows for Taipei Bus Station and airport buses on the same board. The printed English “Airport Express” on these bus panels is preserved as text, not treated as an MRT identity.

## Browser search of Annotations and Photographs (GitHub Pages)

The [destination inventory](docs/DESTINATION_CATALOG.md) lists three hotels and ten shopping names/candidates, including **Cosmos Hotel Taipei / 台北天成大飯店**. Four mall names and two shop names are readable in sampled images; other entries have explicit photo-match and web-verification status. The new shop records include **new balance** and **臺鐵便當本舖**. Browse and filter the list in Chinese/English at http://127.0.0.1:8767/demo/catalog.html after the build below. Source links and exact photo locators are included. This initial list is not exhaustive and does not itself increase the completed annotation count or add web-only candidates to scene evidence.

The [demo](demo/index.html) searches Chinese and English in the browser, with no backend, API key or live LLM. It uses lexical matching and bilingual aliases. Asset paths support the `/TaipeiSignRAG/` GitHub Pages prefix. To preview the exact curated Pages package locally:

```powershell
python scripts/build_browser_search.py
python scripts/build_pages_site.py
python -m http.server 8767 --bind 127.0.0.1 --directory _site
```

Open http://127.0.0.1:8767 . For publication, the manually triggered Pages workflow stages only the demo, generated search data, attributed records and masked evidence images. See [Pages setup](docs/GITHUB_PAGES.md).

Run the evidence-search demo locally:

```powershell
C:/Python313/python.exe scripts/scene_rag_demo.py serve --port 8766
```

Open http://127.0.0.1:8766 . Try `置物櫃`, `廁所`, `stairs`, `gates`, `map`, or `Airport MRT`; compare “Physically visible” with “Mentioned on signs.” `/api/search?q=...` returns evidence and instructions ready for the app's LLM. **No live LLM or positioning engine is connected to this demo.** Retrieval is local lexical matching with bilingual aliases, not a trained embedding model.

Records: [scene annotations](release/huggingface/scene_annotations.jsonl). [Schema and review policy](docs/WHOLE_SCENE_ANNOTATION.md). Progress: [annotation counts](annotations/progress.json). This is a 128-scene pilot, not the completed 8,971-entry annotation collection. All records are assistant-checked; expert review is pending.

**Team:** PHIT 2026 Finalist Team: 3rdEye4All, Urav Advanced Learning Systems Pvt Ltd.

- [Working paper and numbered references](paper/draft.md)
- [BibTeX bibliography](paper/references.bib)
- [Locker observation pilot and Hugging Face dataset card](release/huggingface/README.md)
- [GitHub connection and later Hugging Face upload](docs/GITHUB_AND_HUGGINGFACE.md)
- [Next steps](docs/NEXT_STEPS.md)

The public GitHub repository is [UravAdvanced/TaipeiSignRAG](https://github.com/UravAdvanced/TaipeiSignRAG). Raw archives, full image data and historical research stay in the local project folder and are excluded from Git; the curated release package is separate.

## Resources, masking, batch time and cost

Preparation and checks run on an **HP OMEN Laptop 15-en0xxx**, **AMD Ryzen 7 4800H (8 cores/16 threads)**, approximately **16 GB RAM** (15.36 GiB reported by Windows), and **Windows 11 Home Single Language, build 10.0.26200**. Installed graphics include **NVIDIA GeForce RTX 2060** and AMD Radeon graphics. Software: **Python 3.13.5, Pillow 12.0.0, Node.js 20.19.4, Git 2.56.0.windows.1**, with Microsoft Edge for browser checks and GitHub Pages for the static demo. Cloud hardware is provider-managed.

**Masking:** image-coordinate rectangles are specified while inspecting photographs in OpenAI Codex, then drawn locally by `scripts/prepare_scene_pilot.py` using Pillow `ImageDraw.rectangle` and RGB (45, 45, 45). This is CPU image processing. The downloaded **MobileNet-SSD model was not run and does not create the masks**; the exploratory Windows FaceDetector was not adopted. From scene 072, each original receives one annotation/basic-masking pass. Expert/privacy review remains pending.

**Measured batch:** scenes **091–109 (19 photos)** took **12 minutes 41 seconds**, approximately **40.1 seconds per photo**, including preparation, annotation/masking, saving, exports, documentation, checks and a Windows permission wait. All **375 search-parity cases** and source-hash, mask, count and route checks passed. The checkpoint reached **109 scenes / 110 unique originals**, with **8,861 entries remaining**. This historical timing excludes push/deployment and is one workflow observation.

**GPT-6 Astra planning cost:** [published standard OpenAI API rates](https://developers.openai.com/api/docs/models/gpt-6-astra), checked 5 October 2026, are **USD 10/million uncached input tokens** and **USD 50/million output tokens**. [Reasoning tokens count as output](https://developers.openai.com/api/docs/guides/reasoning). Using these as reference prices:

| Assumed total tokens per 19-photo batch | Estimated gross cost |
|---|---:|
| 30,000 input + 10,000 output/reasoning | **USD 0.80** |
| 60,000 input + 20,000 output/reasoning | **USD 1.60** |
| 120,000 input + 40,000 output/reasoning | **USD 3.20** |

Use **USD 1.60 per batch as a working budget**; USD 0.80–3.20 illustrates different token assumptions, not a measured bill or upper bound. Input includes images, prompts, tool text and repeated context; medium reasoning does not fix token use. These estimates assume each request stays within 272,000 input tokens and exclude caching, credits, taxes, subscription charges, tool fees and pricing-tier adjustments. The [Azure pricing page](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) returned dynamic price placeholders, so the applicable Azure deployment tariff and actual token usage remain unverified. A saved 19-photo batch is not automatically a discounted Batch API job. Details and formula are in the [paper](paper/draft.md).

**Time at collection scale:** 761 seconds per 19 photos projects to **89.0 hours for 8,000 photos**, or **98.6 hours for the 8,861 remaining entries at the timed checkpoint**—about **11.1–12.3 eight-hour working days**. This includes visual inspection, transcription, scene descriptions, mask-coordinate selection, saving, checks and waits. CPU rectangle drawing is only one operation; stages were not separately timed in that batch. The projection assumes comparable effort per entry, whereas the collection also includes narrow crops and repeated views. It excludes independent expert review and is not an unattended completion promise.

**Separate local stage timing at the 128-scene checkpoint:** regenerating **all 128 masked full frames, enlarged previews and the contact sheet took 16.902 seconds**; record/browser/site exports took **0.589 seconds**; integrity and search checks took **5.931 seconds** (**23.422 seconds total**). This run excludes image inspection, transcription, description writing, choosing mask coordinates, documentation edits and permission waits. It measures the full image-preparation script, not rectangle filling alone. The current script regenerates existing images as well as new ones, so rendering overhead grows with the saved corpus.

## Acknowledgements and related work

We thank **[Microsoft for Startups Hub](https://www.microsoft.com/en-us/startups)** for subscription support, and acknowledge **[Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)**, **[Azure OpenAI GPT-6 Astra](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models) at medium reasoning**, and **[OpenAI Codex](https://developers.openai.com/codex/)** among the resources supporting project development. The team-provided cloud configuration is recorded separately from local annotation checkpoints, which do not contain Azure request IDs or metered token usage.

We especially acknowledge **Chun-Chao Yeh, Ke-Jia Jhang and Chin-Chun Chang (2020), “An intelligent indoor positioning system based on pedestrian directional signage object detection: a case study of Taipei Main Station,” Mathematical Biosciences and Engineering, 17(1), 266–285, [doi:10.3934/mbe.2020015](https://www.aimspress.com/article/10.3934/mbe.2020015)**. Their study reports up to 98% sign-identification accuracy for 52 signs across three test datasets totalling 6,341 images. Those are their reported results; TaipeiSignRAG has not measured equivalent accuracy or established that these community exports are their experimental dataset. The paper discusses this predecessor explicitly and retains it as a numbered reference.

## Project contents

- Three original ZIP archives at this folder's root, preserved byte-for-byte.
- `data/taipei-station-sign-board/`: V3 COCO images, crops, manifests, reviews and audit.
- `data/taipei-station-sign-board-cls/`: CLS images, class inventory, reviews and audit.
- `data/taipei-station-sign-board-2/`: second COCO audit, annotation copy and review samples; full images remain available in its original ZIP.
- `research/`: related dataset, model, prior-art and competition research, including reproducible inspection scripts. Older recommendations are historical.
- `PROJECT_STATE.md`: current decisions followed by retained history.
- `docs/ANNOTATION_WORKFLOW.md`: annotation execution recommendation and intended records.
- `relocation_manifest.json` and `relocation_verification.json`: original paths and SHA-256 preservation checks for consolidation.

There are 8,971 image entries across the archives, not 8,971 independent photographs or physical signs. The second COCO export has 1,684 filename-stem matches with CLS; six sampled pairs visually correspond. Full matching verification remains to be done.

## Current status

Archive audits and sampled visual reviews are complete. 128 whole-scene records and two locker observations are prepared, covering 129 unique source photographs. Records were prepared in Codex; expert review is pending, and 8,842 source entries remain without new annotations. Browser search and the optional local API prepare evidence context for an LLM. Full annotation, a live LLM integration, geometric app integration and field testing remain incomplete. No task-specific model training has run. A small current station walkthrough is planned only after the annotation pipeline and app are ready.

The supplied annotations are bounding boxes or class-folder codes. They do not supply text transcripts, physical sign positions, camera poses or station map anchors. Reviewed sign IDs will be attached to the app's mapped anchors separately; retrieval scores are not spatial confidence estimates.

## Run retained scripts

Use this folder as the working directory. Existing audit scripts resolve the project root relative to their own location:

```powershell
C:/Python313/python.exe research/indoor_6h/audit_second_coco.py
```

`requirements.txt` lists dependencies for the retained Python inspection/research scripts. Create a project environment if needed; the parent workspace's service environment is separate.

The three TibaMe exports declare CC BY 4.0. Preserve their bundled attribution and source URLs. Other historical research downloads retain their own terms and are not automatically covered by those dataset licences.

## Execution choice

The user selected direct annotation and review in Codex, using saved batches and image-level checkpoints so work can continue across sessions. Azure API automation is optional if later needed; no Azure deployment is required for the selected workflow. A fresh Codex conversation provides fresh context, not automatically more account allowance. Azure deployment access and quota have not been checked here.

The later proposed sign-based drift-correction architecture was reviewed in `docs/SEMANTIC_RELOCALIZATION_REVIEW.md`. The current knowledge-base work supports sign recognition, retrieval and candidate anchor selection; actual camera relocalisation requires geometric observations or Cloud Anchor resolution.

References: [Azure model catalogue](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-6), [OpenAI image-input guide](https://developers.openai.com/api/docs/guides/images-vision), [Codex capabilities](https://developers.openai.com/codex/cli/features/).
