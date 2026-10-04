"""Prepare a local-only candidate sheet; never part of the release package."""
import io
import json
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/scene-pilot-review'
OUT.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(ROOT / 'Taipei Station Sign Board 2.v1i.coco.zip') as archive:
    names = sorted(n for n in archive.namelist() if n.endswith('.jpg'))
    families = sorted({Path(n).name.split('_')[0] for n in names})
    completed = {json.loads(line)['filename_family'] for line in (ROOT/'release/huggingface/scene_manifest.jsonl').read_text(encoding='utf-8').splitlines()}
    selected = [next(n for n in names if Path(n).name.startswith(f + '_')) for f in families if f not in completed][:8]
    if not selected:
        raise SystemExit('All families have a pilot selection; choose additional exact views explicitly.')
    sheet = Image.new('RGB', (1024, ((len(selected)+1)//2)*315), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, name in enumerate(selected):
        im = Image.open(io.BytesIO(archive.read(name))).convert('RGB')
        x, y = i % 2 * 512, i // 2 * 315
        sheet.paste(im, (x, y))
        draw.text((x+4, y+291), Path(name).name.split('_png')[0], fill='black')
    sheet.save(OUT / 'next-candidates.jpg')
    print('\n'.join(selected))
