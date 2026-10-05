# Taipei Main Station Signboard Annotation and Relational Dataset

**TaipeiSignRAG** is a proof of concept for turning station sign photographs into bilingual, evidence-linked annotations that can support indoor-navigation search.

## POC status

The annotation POC is closed at **204 whole-scene records** and **two separate locker-evidence observations**, covering **205 unique source photographs**. The source archives contain 8,971 image entries; repeated views and crops mean these are not 8,971 independent signs or locations. The curated JSONL release contains the 204-scene checkpoint.

The POC demonstrates the annotation and retrieval workflow, but it is not a complete station inventory or an evaluated navigation system. Full-collection annotation is not planned in this POC.

Different-angle photographs of the same apparent sign or area are retained as separate image observations, not collapsed by repeated exit text or filename family. This preserves angle-specific text and surroundings. RAG can retrieve complementary records with separate image provenance; after human verification and confirmed cross-view links, these views could provide view-diverse examples for model training. 

## Why annotate the images?

A detection box or class label does not tell a navigation assistant which destination matches an arrow, what text is readable in Traditional Chinese or English, or whether a facility is visible in the scene versus only mentioned on a sign. Our records connect text, arrows, surrounding objects, uncertainty, and source-image evidence so retrieval can return a grounded explanation rather than an isolated label.

The data keep Taipei Bus Station, Taoyuan Airport MRT, and airport buses as separate destinations. Scene 011 contains different arrows for Taipei Bus Station and airport buses on the same board. Printed “Airport Express” on a bus panel is preserved as text and is not treated as an MRT identity.

## Demonstrated workflow

The POC demonstrates a repeatable, checkpointed workflow:

1. Audit source archives, image dimensions, filenames, and hashes.
2. Inspect one full-scene photograph at a time and record readable text, destination-arrow relations, visible facilities, and unknowns.
3. Save structured records with source and evidence references.
4. Export JSONL annotations and browser-search data, then run structural and search-parity checks.

The repository includes the records, schemas, prompts, runner scripts, comparison reports, and progress ledger needed to reproduce the process. Generative wording can vary; reproducibility here means the inputs, instructions, record structure, provenance, and validation steps are documented, not that another run produces byte-identical prose.

- [Whole-scene annotation schema and policy](docs/WHOLE_SCENE_ANNOTATION.md)
- [Annotation workflow](docs/ANNOTATION_WORKFLOW.md)
- [Current counts and review status](annotations/progress.json)
- [Scene annotation records](release/huggingface/scene_annotations.jsonl)
- [Source-linked file records](release/huggingface/dataset_file_annotations.jsonl)

### Prompts and comparison reports

The prompts and comparison records are part of this repository:

- [Expanded single-pass scene prompt](docs/prompts/SINGLE_PASS_SCENE_ANNOTATION_V1.md)
- [Short API baseline prompt](docs/prompts/BASELINE_API_ANNOTATION_V1.md)
- [Expanded-prompt comparison](docs/PROMPT_COMPARISON_20261005.md)
- [Native and enlarged API input comparison](docs/DIRECT_API_RESOLUTION_COMPARISON_20261005.md)
- [Native-image API pilot, usage, and semantic findings](docs/DIRECT_API_PILOT_20261005.md)
- [Interactive baseline process demonstration](docs/INTERACTIVE_BASELINE_PROCESS_20261005.md)

The prompt comparison used four photographs and is descriptive, not an accuracy study. The expanded interactive prompt took **678.189 seconds (11 min 18 s)** and produced more entries, but some entries split or reorganized existing facts. Entry counts do not establish higher recall or accuracy. In the four-image API pilot, the same concise prompt took **97.393 s** with native 512×288 JPEGs and **80.918 s** with resized 1536×864 PNGs. Enlargement adds no captured detail; the format also changed, and this four-image sample cannot establish a general speed or accuracy benefit.

## Time and cost evidence

At published GPT-6 Astra standard rates of USD 10 per million input tokens and USD 50 per million output tokens, the API usage provides a reference-price estimate:

| Four-image API input | Input / output tokens | Elapsed time | Estimated gross price |
|---|---:|---:|---:|
| Native 512×288 JPEG | 4,032 / 10,549 | 97.393 s | **USD 0.57** |
| Resized 1536×864 PNG | 8,296 / 8,425 | 80.918 s | **USD 0.50** |

Reasoning tokens are included in output usage. Azure's actual billed tariff and invoices were not available as a Microsoft Startup Hub sponsorship was used. The 204-record POC was completed interactively in Codex, for which per-request usage and marginal subscription cost were not recorded; these API trial estimates are not the cost of producing all 204 records. Earlier 19-photo planning scenarios of USD 0.80–3.20 are in [batch timing and cost notes](docs/ANNOTATIONS_ONLY_TIMING.md); they are assumed token budgets, not measured charges.

## Supplemental search examples

The browser demo also includes three user-provided photographs outside the 204-scene TibaMe POC dataset: an M3 Cosmos Hotel sign, an M6 Caesar Park Hotel listing, and an E5 exit scene. Search for **Cosmos Hotel** to retrieve the M3 photograph. These examples do not change the core annotation count or enter the curated dataset JSONL; the existing E5 mask is retained.

## Search demo

The [browser demo](demo/index.html) searches the released scene records in Chinese and English using lexical matching and bilingual aliases. It runs without a backend, API key, or live language model. It distinguishes physically visible evidence from sign references; it does not establish current availability, precise locations, accessible routes, or positioning accuracy.

To rebuild and preview the curated GitHub Pages site locally:

```powershell
python scripts/build_browser_search.py
python scripts/build_pages_site.py
python -m http.server 8767 --bind 127.0.0.1 --directory _site
```

Open http://127.0.0.1:8767/demo/catalog.html for the destination catalogue or http://127.0.0.1:8767 for the demo. The optional local retrieval API can be started with:

```powershell
C:/Python313/python.exe scripts/scene_rag_demo.py serve --port 8766
```

## Future development

The next phase is human verification of Chinese and English transcripts, translations, destination-arrow associations, facility descriptions, uncertainty, and privacy handling. **After that review**, verified records can be connected to the 3rDi4All app and linked to separately confirmed map waypoints. Semantic search will supply candidates and evidence; map or anchor associations still need separate verification. App integration, a station walkthrough, localization improvement, and accessibility outcomes are not part of this POC.

## Data sources and attribution

The three TibaMe exports used for the audit are the Sign Board V3 [COCO export](https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board), Sign Board CLS [classification export](https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-cls), and Sign Board 2 [COCO export](https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2). Their metadata declares CC BY 4.0; retain attribution and modification notices in derivatives.

**Masking:** image-coordinate rectangles are specified while inspecting photographs in OpenAI Codex, then drawn locally by scripts/prepare_scene_pilot.py using Pillow ImageDraw.rectangle and RGB (45, 45, 45). This is CPU image processing. From scene 072, each original receives one annotation/basic-masking pass. Expert/privacy review remains pending. These masks were applied to derived release images after visual inspection; they did not redact originals before model viewing.

**Acknowledgements:** We thank [Microsoft for Startups Hub](https://www.microsoft.com/en-us/startups) for subscription support and acknowledge [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry), [Azure OpenAI GPT-6 Astra](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models), and [OpenAI Codex](https://developers.openai.com/codex/) among the resources supporting this work. The API cost table uses published OpenAI reference rates, not a verified Azure bill.

**Team:** PHIT 2026 Finalist Team: 3rdEye4All, Urav Advanced Learning Systems Pvt Ltd.  
**Working paper:** [Concise preprint draft and references](paper/draft.md).  
**Public repository:** [UravAdvanced/TaipeiSignRAG](https://github.com/UravAdvanced/TaipeiSignRAG).
