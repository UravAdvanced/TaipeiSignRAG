# Taipei Main Station Signboard Annotation and Relational Dataset

**PHIT 2026 Finalist Team: 3rdEye4All**

**AI Eye 4 All: AI Indoor Navigation for Inclusive Smart Cities.**

Urav Advanced Learning Systems Pvt Ltd.

TaipeiSignRAG is the Taipei Main Station whole-photograph annotation POC and bilingual evidence-search demo. Expert review is pending. It does not establish precise positioning, current facilities or accessible routes.

## Whole-scene pilot and local demo

Thirty-two whole-photograph annotations now cover readable signs **and** surrounding objects. Observed examples include a locker bank, barrier gates, stairs/escalators, a shopfront, map boards and passage entrances. Fourteen amenity categories are explicitly checked per scene. A toilet mentioned on a sign is kept separate from a physically visible toilet. No lift or check-in counter is verified in this pilot.

**Airport buses / 機場巴士, Taoyuan Airport MRT / 桃園機場捷運, and Taipei Bus Station / 臺北轉運站 are separate destinations.** Scene 011 shows different arrows for Taipei Bus Station and airport buses on the same board. The printed English “Airport Express” on these bus panels is preserved as text, not treated as an MRT identity.

## Browser search of Annotations and Photographs (GitHub Pages)

The [destination inventory](docs/DESTINATION_CATALOG.md) lists three hotels and ten shopping names/candidates, including **Cosmos Hotel Taipei / 台北天成大飯店**. Four mall names and two shop names are readable in sampled images; other entries have explicit photo-match and web-verification status. The new shop records include **new balance** and **臺鐵便當本舖**. Browse and filter the list in Chinese/English at http://127.0.0.1:8767/demo/catalog.html after the build below. Source links and exact photo locators are included. This initial list is not exhaustive and does not itself increase the completed annotation count or add web-only candidates to scene evidence.

The [demo](demo/index.html) searches Chinese and English in the browser, with no backend, API key or live LLM. It uses lexical matching and bilingual aliases. Asset paths support the `/TaipeiSignRAG/` GitHub Pages prefix. To preview the exact curated Pages package locally:

```powershell
python scripts/build_browser_search.py
python scripts/build_pages_site.py
python -m http.server 8767 --bind 127.0.0.1 --directory _site
```

Open http://127.0.0.1:8767 . For publication, the manually triggered Pages workflow stages only the demo, generated search data, attributed records and masked evidence images. See [Pages setup](docs/GITHUB_PAGES.md). Pages has not been deployed in this iteration.

Run the evidence-search demo locally:

```powershell
C:/Python313/python.exe scripts/scene_rag_demo.py serve --port 8766
```

Open http://127.0.0.1:8766 . Try `置物櫃`, `廁所`, `stairs`, `gates`, `map`, or `Airport MRT`; compare “Physically visible” with “Mentioned on signs.” `/api/search?q=...` returns evidence and instructions ready for the app's LLM. **No live LLM or positioning engine is connected to this demo.** Retrieval is local lexical matching with bilingual aliases, not a trained embedding model.

Records: [scene annotations](release/huggingface/scene_annotations.jsonl). [Schema and review policy](docs/WHOLE_SCENE_ANNOTATION.md). Progress: [annotation counts](annotations/progress.json). This is an thirty-two-scene pilot, not the completed 8,971-entry annotation collection. All records are assistant-checked; expert review is pending.

**Team:** PHIT 2026 Finalist Team: 3rdEye4All, Urav Advanced Learning Systems Pvt Ltd.

- [Working paper and numbered references](paper/draft.md)
- [BibTeX bibliography](paper/references.bib)
- [Locker observation pilot and Hugging Face dataset card](release/huggingface/README.md)
- [GitHub connection and later Hugging Face upload](docs/GITHUB_AND_HUGGINGFACE.md)
- [Next steps](docs/NEXT_STEPS.md)

The private GitHub repository is `UravAdvanced/TaipeiSignRAG`; the user successfully pushed the initial commits. New local commits still require `git push` from the user's authenticated terminal because the current Codex Windows sandbox cannot access its keyring credentials. Raw archives, full image data and historical research stay in this local folder and are excluded from Git; the curated release package is separate.

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

Archive audits and sampled visual reviews are complete. Thirty-two whole-scene records and two locker observations are prepared, covering thirty-three unique source photographs. They are assistant-checked, with expert review pending; 8,938 source entries remain without new annotations. Browser search and the optional local API prepare evidence context for an LLM. Full annotation, a live LLM integration, geometric app integration and field testing remain incomplete. No training or Azure inference has run. A small current station walkthrough is planned only after the annotation pipeline and app are ready.

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
