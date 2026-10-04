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
 'A04N_HH_001': [(45,194,153,288),(161,187,214,288),(228,192,253,247),(416,182,488,288)],
 'A06W_HH_001': [(0,193,113,288),(143,177,199,249),(196,187,315,288),(308,199,359,288),(461,163,512,288)],
 'A07E_HH_001': [(0,186,57,288),(62,185,127,288),(168,181,271,288),(302,185,501,288)],
 'A15E_HH_001': [(186,193,205,236),(209,181,280,217),(289,194,305,231)],
 'A15W_HH_001': [(110,192,150,281),(144,193,161,240),(165,196,180,235),(181,189,318,259)],
 'A02E_HH_001': [[36,210,173,288],[176,205,232,288],[236,194,301,280],[333,199,397,288],[445,202,474,277]],
 'A02W_HH_001': [[0,190,84,288],[57,206,176,288],[173,190,290,276],[362,191,420,250],[129,190,158,218]],
 'A03E_HH_001': [[68,195,85,240],[109,195,173,288],[171,188,194,250],[194,195,218,250],[232,194,256,249],[243,190,323,288],[343,180,468,288],[476,205,512,288]],
 'A03W_HH_001': [[104,191,185,288],[192,184,381,288],[374,211,456,288],[475,190,512,273]],
 'A05N_HH_001': [[64,182,97,225],[83,199,121,257],[116,181,188,288],[195,188,273,288],[272,187,407,288]],
 'A07W_HH_001': [[0,211,40,288],[153,213,178,288],[197,213,209,245],[221,215,237,246],[319,211,372,271],[396,215,454,288]],
 'A08N_HH_001': [[99,216,161,288],[241,240,273,274]],
 'A08S_HH_001': [[18,206,151,288],[151,214,242,288]],
 'A09E_HH_001': [[0,226,42,288],[54,208,116,288],[153,203,209,267],[215,205,286,288],[291,202,330,260],[384,209,421,285],[451,221,512,288]],
 'A10W_HH_001': [[49,188,81,288],[81,187,116,288],[150,197,225,275],[223,188,260,253],[254,190,294,288],[303,191,381,288],[470,197,512,288]],
 'A11E_HH_001': [[35,232,85,288],[98,199,168,288],[335,210,381,281],[360,229,479,288]],
 'A11W_HH_001': [[83,189,99,226],[144,180,166,203],[178,181,235,219],[348,179,384,230],[391,187,405,224],[344,206,391,288],[458,188,472,228]],
 'A12E_HH_001': [[41,199,75,256],[150,202,188,288],[219,199,241,258],[279,194,319,254],[377,187,413,259]],
 'A12W_HH_001': [[8,209,38,282],[70,207,113,288],[237,205,280,266],[301,205,354,288],[436,205,469,248]],
 'A13E_HH_001': [[59,201,98,272],[192,188,222,246],[222,185,244,216],[247,191,270,245],[298,189,327,234],[338,205,420,288]],
 'A13W_HH_001': [],
 'A14E_HH_001': [[108,229,153,288],[189,192,243,257],[234,197,283,267],[288,198,302,237],[339,201,401,288],[414,200,433,229]],
 'A14W_HH_001': [[0,208,29,288],[102,201,141,288],[159,199,177,261],[196,189,234,267],[226,187,321,288]],
 'A17W_HH_001': [[119,187,134,234],[170,185,195,232],[201,185,244,275],[237,189,293,288],[301,183,321,239],[321,197,356,286],[379,219,414,270],[392,190,407,218]],
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
          'privacy_masks_xyxy':boxes,'privacy_method':('conservative manual local masks; may hide adjacent objects' if boxes else 'full-frame inspection found no person regions requiring masks; independent privacy review pending'),
          'provided_sign_boxes_xywh':[a['bbox'] for a in coco['annotations'] if a['image_id']==meta['id']],
          'source_url':'https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2','license':'CC-BY-4.0'})
(PACK/'scene_manifest.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
sheet=Image.new('RGB',(1024,((len(rows)+1)//2)*315),'white');d=ImageDraw.Draw(sheet)
for i,r in enumerate(rows):
    x=i%2*512;y=i//2*315;sheet.paste(Image.open(PACK/r['evidence_image']),(x,y));d.text((x+4,y+291),r['image_id']+' '+r['filename_family'],fill='black')
(ROOT/'data/scene-pilot-review').mkdir(exist_ok=True)
sheet.save(ROOT/'data/scene-pilot-review/contact.jpg',quality=95)
for r in rows[8:]:
    im=Image.open(PACK/r['evidence_image'])
    im.resize((1536,864)).save(ROOT/'data/scene-pilot-review'/f"{r['image_id']}-detail.png")
print(f'Prepared {len(rows)} full-frame masked views; original archives unchanged.')
