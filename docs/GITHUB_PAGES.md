# Browser-side Chinese/English POC

**PHIT 2026 Finalist Team: 3rdEye4All**

**AI Eye 4 All: AI Indoor Navigation for Inclusive Smart Cities.**

The static page loads `demo/search-data.json` once and performs lexical retrieval in JavaScript. It needs no Python service, API key, embeddings or external inference. Queries stay in the browser. Chinese/English aliases distinguish airport buses, Taoyuan Airport MRT and Taipei Bus Station. Evidence filters preserve visible objects versus sign-only references. Full scene context remains available on each result card and in the LLM payload.

## Rebuild and preview

```powershell
python scripts/build_browser_search.py
python scripts/build_pages_site.py
python -m http.server 8767 --bind 127.0.0.1 --directory _site
```

Open http://127.0.0.1:8767 . Use HTTP rather than double-clicking the HTML file: module loading and JSON fetch require a web origin. The optional Python API still runs with `python scripts/scene_rag_demo.py serve --port 8766`.

After annotation changes, first run `prepare_scene_pilot.py` and `build_scene_records.py`, then regenerate browser data. The image preparation step requires the original archive and Pillow. Existing committed records and masked images are sufficient for a Pages build.

## Publish when ready

The prepared workflow has a manual `workflow_dispatch` trigger only; committing or pushing does not deploy it automatically. No Pages deployment was performed during this implementation.

1. Push the reviewed changes to `UravAdvanced/TaipeiSignRAG` from the user's authenticated terminal.
2. In repository **Settings → Pages**, select **GitHub Actions** as the source, if Pages is available for this private repository and account plan.
3. In **Actions**, run **Publish curated TaipeiSignRAG POC**. The workflow reports the actual site URL after deployment.

The build stages an explicit file list in `_site`: the landing page, browser demo, search data, attributed scene records and manually masked scene images. Original archives, `data/`, research, local previews and internal project state are excluded. Relative links support a repository prefix such as `/TaipeiSignRAG/`. No repository visibility change is required by this implementation or performed here.

## Validation and limits

Run `python scripts/check_poc.py` after building `_site` (requires Node and Pillow). Checks cover bilingual destination separation, visible/sign-only distinctions, Python/JavaScript retrieval parity, source hashes, mask pixels, annotation counts and local HTTP assets. These functional checks are not a measured retrieval-accuracy benchmark or independent privacy review. Actual hosted Pages behavior still requires a deployment check.

The current build also passed a local headless Microsoft Edge smoke check: all 11 evidence cards rendered, and the desktop page screenshot was visually inspected. This does not establish hosted Pages availability or a complete accessibility audit.

The UI prominently credits the team and labels the work as an AI-assisted POC. Human review is pending; coordinates, physical anchor links, current operations and accessible routes remain unverified. No precise positioning or full annotation completion is claimed.
