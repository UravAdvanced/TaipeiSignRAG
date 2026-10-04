"""Prepare a local-only candidate sheet; never part of the release package."""
import argparse
import io
import json
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/scene-pilot-review'
OUT.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--limit', type=int, default=19)
args = parser.parse_args()
if args.limit < 1:
    parser.error('--limit must be positive')
with zipfile.ZipFile(ROOT / 'Taipei Station Sign Board 2.v1i.coco.zip') as archive:
    names = sorted(n for n in archive.namelist() if n.endswith('.jpg'))
    families = sorted({Path(n).name.split('_')[0] for n in names})
    manifest = [json.loads(line) for line in (ROOT/'release/huggingface/scene_manifest.jsonl').read_text(encoding='utf-8').splitlines()]
    completed = {row['filename_family'] for row in manifest}
    completed_images = {row['source_image'] for row in manifest if row['source_archive'] == 'Taipei Station Sign Board 2.v1i.coco.zip'}
    selected = [next(n for n in names if Path(n).name.startswith(f + '_')) for f in families if f not in completed][:args.limit]
    if not selected:
        selected = [name for name in names if name not in completed_images][:args.limit]
    if not selected:
        raise SystemExit('All exact photographs in this archive already have records.')
    sheet = Image.new('RGB', (1024, ((len(selected)+1)//2)*315), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, name in enumerate(selected):
        im = Image.open(io.BytesIO(archive.read(name))).convert('RGB')
        stem = Path(name).name.split('_png')[0]
        im.resize((1536,864)).save(OUT / (stem + '-review.png'))
        x, y = i % 2 * 512, i // 2 * 315
        sheet.paste(im, (x, y))
        draw.text((x+4, y+291), Path(name).name.split('_png')[0], fill='black')
    sheet.save(OUT / 'next-candidates.jpg')
    (OUT / 'next-selected.json').write_text(json.dumps(selected, indent=2), encoding='utf-8')
    print('\n'.join(selected))
