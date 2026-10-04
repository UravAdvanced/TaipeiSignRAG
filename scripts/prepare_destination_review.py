"""Local-only enlarged source crops for exact destination text review."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/destination-review';OUT.mkdir(parents=True,exist_ok=True)
rows=[json.loads(line) for line in (ROOT/'data/taipei-station-sign-board-cls/manifest.jsonl').read_text(encoding='utf-8').splitlines()]
families=['C17S','D02E','C15S','C13E','E07S','C05S','C19S','A16N','A01N','A02E','A03E','E08N']
selected=[]
for family in families:
    group=sorted([r for r in rows if r['class']==family],key=lambda r:r['filename'])
    for index in [len(group)//3,len(group)-1]:
        r=group[index];selected.append(r)
        with Image.open(ROOT/'data/taipei-station-sign-board-cls/raw'/r['path']) as im:
            im.resize((1536,345)).save(OUT/(r['original_stem']+'.png'))
(OUT/'selected.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
for offset in range(0,len(selected),6):
    sheet=Image.new('RGB',(1536,6*375),'white');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(selected[offset:offset+6]):
        sheet.paste(Image.open(OUT/(r['original_stem']+'.png')),(0,i*375))
        draw.text((5,i*375+349),r['original_stem'],fill='black')
    sheet.save(OUT/f'detail_{offset//6+1}.png')
print(f'Prepared {len(selected)} local-only exact source crops.')
