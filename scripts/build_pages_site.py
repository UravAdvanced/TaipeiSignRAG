"""Stage an explicit curated file list for Pages, excluding local raw data."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
files = ['index.html','.nojekyll','demo/index.html','demo/app.js','demo/search.mjs','demo/search-data.json',
         'release/huggingface/ATTRIBUTION.md','release/huggingface/scene_annotations.jsonl']
import json
records = [json.loads(line) for line in (ROOT/'release/huggingface/scene_annotations.jsonl').read_text(encoding='utf-8').splitlines()]
files += ['release/huggingface/'+row['evidence_image'] for row in records]
for name in files:
    destination = OUT / name
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/name,destination)
expected = {Path(name).as_posix() for name in files}
actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}
assert actual == expected, 'Staging contains unexpected files; inspect _site before publishing'
print(f'Staged {len(files)} curated files in _site. No deployment performed.')
