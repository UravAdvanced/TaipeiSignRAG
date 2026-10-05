"""Checkpoint one-pass cloud annotations without publishing new image pixels.

prepare N extracts local-only inspection views; save N ingests authored observations;
finish N builds exports, validates them, and records elapsed workflow time.
No OCR, semantic inference, masking, or remote API call is performed by this helper.
The observations are authored in the configured Codex cloud session.
"""
import argparse
import hashlib
import io
import json
import subprocess
import sys
import time
import tomllib
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'release/huggingface'
ARCHIVE = 'Taipei Station Sign Board 2.v1i.coco.zip'
POLICY = ROOT / 'annotations/publication_policy.json'
MANIFEST = PACK / 'scene_manifest.jsonl'
NOTES = ROOT / 'annotations/scene_pilot_notes.json'
LEDGER = ROOT / 'annotations/batch_progress.json'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def now():
    return datetime.now(timezone.utc).isoformat()

def load_manifest():
    return [json.loads(s) for s in MANIFEST.read_text(encoding='utf-8').splitlines()]

def image_digest():
    files=sorted((PACK/'scene_images').glob('*'))
    payload='\n'.join(p.name+':'+hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file())
    return len(files), hashlib.sha256(payload.encode()).hexdigest()

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('action', choices=['prepare','annotate','save','finish'])
parser.add_argument('batch', type=int)
args=parser.parse_args()
out=ROOT/'data/metadata-batches'/f'{args.batch:03}'
checkpoint=out/'checkpoint.json'

if args.action=='prepare':
    started=now()
    assert not checkpoint.exists(), 'Existing batch must be resumed, not overwritten.'
    count,digest=image_digest()
    if not POLICY.exists():
        assert count==128
        write(POLICY, {'annotations_only_from_scene':129, 'legacy_scene_image_count':count,
                      'legacy_scene_image_digest':digest, 'new_image_publication':False,
                      'review_status':'human checks pending', 'source_images':'originals inspected in cloud context; not added to new published records'})
    policy=read(POLICY)
    assert (count,digest)==(policy['legacy_scene_image_count'],policy['legacy_scene_image_digest'])
    manifest=load_manifest()
    done={r['source_image'] for r in manifest if r['source_archive']==ARCHIVE}
    config=tomllib.loads((Path.home()/'.codex/config.toml').read_text(encoding='utf-8'))
    settings={key:config.get(key) for key in ['model','model_provider','model_reasoning_effort']}
    assert settings=={'model':'gpt-6-astra','model_provider':'azure','model_reasoning_effort':'medium'}, settings
    out.mkdir(parents=True, exist_ok=True)
    selected=[]
    with zipfile.ZipFile(ROOT/ARCHIVE) as z:
        coco=json.loads(z.read('train/_annotations.coco.json'))
        images={r['file_name']:r for r in coco['images']}
        names=[n for n in sorted(z.namelist()) if n.endswith('.jpg') and n not in done][:19]
        assert len(names)==19
        for idx,name in enumerate(names,len(manifest)+1):
            raw=z.read(name);im=Image.open(io.BytesIO(raw)).convert('RGB')
            stem=Path(name).name.split('_png')[0]
            # Inspection-only resizing, not recovered detail; no output enters release/.
            im.resize((1536,864)).save(out/(stem+'.png'))
            meta=images[Path(name).name]
            selected.append({'image_id':f'tps-scene-{idx:03}','stem':stem,'source_archive':ARCHIVE,
                'source_image':name,'source_sha256':hashlib.sha256(raw).hexdigest(),
                'source_image_size':list(im.size),'filename_family':stem.split('_')[0],
                'evidence_image':None,'privacy_masks_xyxy':[], 'publication_mode':'annotations_only',
                'privacy_method':'no image publication; no masks generated',
                'provided_sign_boxes_xywh':[a['bbox'] for a in coco['annotations'] if a['image_id']==meta['id']],
                'source_url':'https://universe.roboflow.com/tibame-4ueve/taipei-station-sign-board-2','license':'CC-BY-4.0'})
    write(checkpoint, {'batch':args.batch,'started_at_utc':started,'prepared_at_utc':now(),
                      'configuration':settings,'configuration_evidence':'local Codex config; provider request IDs and billed tokens not exposed',
                      'selected':selected,'status':'prepared'})
    print('\n'.join(r['image_id']+' '+r['stem'] for r in selected))

elif args.action=='annotate':
    cp=read(checkpoint)
    assert cp['status']=='prepared' and 'annotation_started_at_utc' not in cp
    cp['annotation_started_at_utc']=now()
    write(checkpoint,cp)
    print('Annotation timing started; earlier preparation-to-annotation gap is recorded separately.')

elif args.action=='save':
    cp=read(checkpoint)
    assert cp['status']=='prepared'
    observations=read(out/'observations.json')
    assert len(observations)==19
    assert [o['stem'] for o in observations]==[r['stem'] for r in cp['selected']]
    notes=read(NOTES);manifest=load_manifest()
    assert len(notes)==len(manifest)==int(cp['selected'][0]['image_id'].split('-')[-1])-1
    for source,observation in zip(cp['selected'], observations):
        assert not any(k in observation for k in ['masks','privacy_masks_xyxy','evidence_image'])
        for key in ['summary_en','summary_zh','signs','objects','uncertain','unknowns']:
            assert key in observation, key
        note={k:v for k,v in observation.items() if k!='stem'}
        note.update(image_id=source['image_id'],review_date=now()[:10],visual_review_passes=1,
                    annotation_method='single original-photograph annotation pass in Codex; saved configuration requests Azure GPT-6 Astra, medium reasoning, but actual serving model is not exposed; no local semantic model, masks or second visual review',
                    configured_model=cp['configuration']['model'],configured_provider=cp['configuration']['model_provider'],
                    configured_reasoning_effort=cp['configuration']['model_reasoning_effort'])
        notes.append(note)
        manifest.append({k:v for k,v in source.items() if k!='stem'})
    write(NOTES,notes)
    MANIFEST.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in manifest),encoding='utf-8')
    cp.update(status='saved',saved_at_utc=now());write(checkpoint,cp)
    print(f'Saved {len(observations)} annotations-only records; no published image files created.')

else:
    cp=read(checkpoint)
    assert cp['status']=='saved'
    stages={}
    for script in ['build_scene_records.py','build_browser_search.py','build_pages_site.py','check_poc.py']:
        start=time.perf_counter()
        subprocess.run([sys.executable,str(ROOT/'scripts'/script)],check=True)
        stages[script]=round(time.perf_counter()-start,3)
    finished=now()
    seconds=round((datetime.fromisoformat(finished)-datetime.fromisoformat(cp['started_at_utc'])).total_seconds(),3)
    preparation=round((datetime.fromisoformat(cp['prepared_at_utc'])-datetime.fromisoformat(cp['started_at_utc'])).total_seconds(),3)
    annotation_start=cp.get('annotation_started_at_utc',cp['prepared_at_utc'])
    annotation=round((datetime.fromisoformat(cp['saved_at_utc'])-datetime.fromisoformat(annotation_start)).total_seconds(),3)
    gap=round((datetime.fromisoformat(annotation_start)-datetime.fromisoformat(cp['prepared_at_utc'])).total_seconds(),3)
    result={'batch':args.batch,'date':finished[:10],'first_scene_id':cp['selected'][0]['image_id'],
        'last_scene_id':cp['selected'][-1]['image_id'],'photos':19,'status':'checked_locally','publication_mode':'annotations_only',
        'timing':{'started_at_utc':cp['started_at_utc'],'finished_at_utc':finished,'elapsed_seconds':seconds,
                  'local_preparation_seconds':preparation,'interactive_annotation_and_save_seconds':annotation,
                  'pre_annotation_gap_seconds':gap,'elapsed_excluding_pre_annotation_gap_seconds':round(seconds-gap,3),
                  'local_export_and_check_seconds':stages,
                  'scope':'wall time from local preparation through checked exports; includes tool round trips and waits; excludes one-time implementation, final documentation/publication; not isolated model latency'},
        'configured_model':cp['configuration'], 'actual_serving_model':None, 'failed_records':0, 'incomplete_records':0,
        'provider_request_count':None,'billed_token_usage':None,'actual_cost_usd':None,
        'validation':'375 search-parity cases, exact source hashes, 128 retained image hashes, no new image exports, annotations-only shape and static/API routes passed.'}
    if cp.get('resumed_at_utc'):
        result['timing'].update(
            interrupted=True,
            resumed_at_utc=cp['resumed_at_utc'],
            resumed_segment_seconds=round((datetime.fromisoformat(finished)-datetime.fromisoformat(cp['resumed_at_utc'])).total_seconds(),3),
            comparable_full_batch_seconds=None,
            comparison_note='Interrupted between turns. Original elapsed and annotation/save intervals include the interruption. Resume timestamp was saved after four image views and a permission wait, so the resumed segment is not a complete batch measurement. Do not infer active annotation time by subtracting this gap.')
    ledger=read(LEDGER)
    assert not any(b['batch']==args.batch for b in ledger['batches'])
    ledger['batches'].append(result)
    ledger['authorization']='From scene 129 publish dataset, filename and annotations only. Preserve existing images. One cloud annotation pass per original; no new masking or person descriptions. Measure three 19-photo batches before deciding scale.'
    ledger['last_documented_scene_count']=int(cp['selected'][-1]['image_id'].split('-')[-1])
    write(LEDGER,ledger)
    cp.update(status='checked',measurement=result);write(checkpoint,cp)
    print(json.dumps(result,ensure_ascii=False))
