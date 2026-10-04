# Repository connection and release preparation

GitHub owner confirmed by the user: `UravAdvanced`. Proposed repository name: `TaipeiSignRAG`. `PHIT2026Team` remains the project team label, not the GitHub owner.
Affiliation: Urav Advanced Learning Systems Pvt Ltd. Individual paper authors remain pending.

## Local Git connection

The project folder is initialised as a Git repository on `main`, with the planned remote:

```text
https://github.com/UravAdvanced/TaipeiSignRAG.git
```

The user has successfully created this private repository, authenticated `UravAdvanced` with HTTPS and pushed the initial commits. The Codex Windows sandbox runs under a different account and still receives HTTP 401 from gh and SEC_E_NO_CREDENTIALS from Git HTTPS. Do not repeat browser authentication in the user's terminal merely because of that sandbox error. No token is stored in this project. Codex can commit locally; the user's terminal can push those commits.

To push newly prepared commits from the user's authenticated PowerShell terminal:

```powershell
Set-Location 'E:\UrbanLensMCP\TaipeiMainStation_SighBoad_Annotation_Relational_Dataset'
git push -u origin main
```

The repository already exists and the remote is set. Unauthenticated requests cannot distinguish a missing repository from a private one. No new repository-creation command is needed.

For future changes, review, commit and push:

```powershell
git status --short
git add README.md CITATION.cff .gitignore .gitattributes requirements.txt paper docs scripts release annotations demo
git commit -m 'Update TaipeiSignRAG documentation and annotations'
git push -u origin main
```

Use your own Git author identity if Git requests it. The raw archives, full `data/` and historical `research/` trees are kept locally and ignored by Git; the curated `release/` folder is tracked. The source files remain available in the same project folder. The repository can be made public when its intended release contents are ready.

## Hugging Face, later and user-managed

The user will handle Hugging Face after preparation is complete. The current upload candidate is `release/huggingface/`; it includes a dataset card, eight whole-scene records, two locker observations, privacy-transformed image evidence and attribution. Do not describe it as the full annotation release.

When ready, create a dataset repository in the selected namespace and upload the contents of that folder at the dataset repository root. The card declares a JSONL `amenity_pilot` configuration. The full dataset card and record counts must be updated as reviewed records are added. Hugging Face credentials are not needed for local preparation.

References: https://huggingface.co/docs/hub/datasets-cards and https://huggingface.co/docs/hub/datasets-adding .

## Working paper

Read `paper/draft.md`. Edit `paper/manuscript.source.md` and `paper/references.json`, then run:

```powershell
C:/Python313/python.exe scripts/render_paper.py
```

This regenerates the numbered paper, BibTeX and citation-order mapping. The abstract is checked for citation numbers; repeated references retain their first assigned number. Title/abstract describe an initial audit and planned system, not completed field results.
