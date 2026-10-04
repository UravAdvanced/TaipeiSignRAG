"""Prepare native-size full-frame pilot views with explicit local privacy masks.

Masks are conservative, manually specified regions, not detector ground truth.
They can obscure nearby objects; annotations must account for masked areas.
"""
import hashlib
import io
import json
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'release/huggingface'
OUT = PACK / 'scene_images'
OUT.mkdir(parents=True, exist_ok=True)
ARCHIVE = 'Taipei Station Sign Board 2.v1i.coco.zip'
SELECTION = {
 'A01N_HH_001': [(138,195,190,288),(235,235,279,288),(278,205,333,288),(345,205,391,288),(396,212,477,288)],
 'A04S_HH_001': [(57,174,124,288),(224,171,394,288),(420,163,504,288)],
 'A05S_HH_001': [(58,192,110,288),(275,174,347,288),(210,174,254,229)],
 'A06E_HH_001': [(0,173,111,288),(105,190,160,288),(150,181,259,288),(254,161,318,288),(322,177,374,288),(417,165,480,288)],
 'A09W_HH_001': [(0,188,51,288),(77,209,126,288),(134,164,181,260),(300,153,363,278),(378,190,431,288)],
 'A10E_HH_001': [(0,217,48,288),(75,188,122,288),(121,179,177,288),(175,176,244,248),(243,167,310,288),(347,182,416,288)],
 'A16N_HH_001': [(125,204,210,288),(205,183,273,288),(287,175,352,288),(467,174,512,288)],
 'A18W_HH_001': [(141,190,215,288),(211,187,252,288),(252,178,304,288),(395,218,441,288),(460,205,512,288)],
}

rows = []
with zipfile.ZipFile(ROOT / ARCHIVE) as z:
    coco = json.loads(z.read('train/_annotations.coco.json'))
    images = {r['file_name']:r for r in coco['images']}
    for idx,(stem,boxes) in enumerate(SELECTION.items(),1):
        name = next(n for n in z.namelist() if n.endswith('.jpg') and Path(n).name.startswith(stem+'_png.'))
        b = z.read(name)
        im = Image.open(io.BytesIO(b)).convert('RGB')
        draw = ImageDraw.Draw(im)
        for box in boxes:
            draw.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=(45,45,45))
        filename = f'scene_{idx:03}.png'
        im.save(OUT/filename)
        meta = images[Path(name).name]
        rows.append({'image_id':f'tps-scene-{idx:03}','source_archive':ARCHIVE,'source_image':name,
          'source_sha256':hashlib.sha256(b).hexdigest(),'source_image_size':list(im.size),
          'filename_family':stem.split('_')[0],'evidence_image':f'scene_images/{filename}',
          'privacy_masks_xyxy':boxes,'privacy_method':'conservative manual local masks; may hide adjacent objects',
          'provided_sign_boxes_xywh':[a['bbox'] for a in coco['annotations'] if a['image_id']==meta['id']],
          'source_url':'https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2','license':'CC-BY-4.0'})
(PACK/'scene_manifest.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
sheet=Image.new('RGB',(1024,4*315),'white');d=ImageDraw.Draw(sheet)
for i,r in enumerate(rows):
    x=i%2*512;y=i//2*315;sheet.paste(Image.open(PACK/r['evidence_image']),(x,y));d.text((x+4,y+291),r['image_id']+' '+r['filename_family'],fill='black')
(ROOT/'data/scene-pilot-review').mkdir(exist_ok=True)
sheet.save(ROOT/'data/scene-pilot-review/contact.jpg',quality=95)
print(f'Prepared {len(rows)} full-frame masked views; original archives unchanged.')
