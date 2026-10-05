"""Four-photo Azure Responses pilot; prepare is offline, run sends four originals.

Keeps the six baseline annotation fields. Does not modify production records.
Credentials come from the configured environment variable, never CLI arguments.
Raw responses and metrics stay under the git-ignored data/ directory.
"""
import argparse
import asyncio
import base64
import hashlib
import io
import json
import logging
import os
import time
import tomllib
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

import httpx
from openai import AsyncOpenAI, APIConnectionError, APIStatusError
from PIL import Image
from pydantic import BaseModel, ConfigDict

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/direct-api-pilot-20261005'
NATIVE_OUT = OUT
IMAGE_MODE = 'native'
PROMPT = ROOT/'docs/prompts/BASELINE_API_ANNOTATION_V1.md'
IDS = ['tps-scene-003', 'tps-scene-006', 'tps-scene-029', 'tps-scene-190']
PRODUCTION = ['annotations/scene_pilot_notes.json', 'release/huggingface/scene_manifest.jsonl',
              'release/huggingface/scene_annotations.jsonl', 'release/huggingface/dataset_file_annotations.jsonl']
DIRECTION = Literal['up','down','left','right','up_left','up_right','down_left','down_right','u_turn']

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

class Sign(StrictModel):
    visible_zh: str | None
    visible_en: str | None
    label_en: str
    direction: DIRECTION | None
    panel: str
    symbols: list[str]
    note: str | None

class SceneObject(StrictModel):
    category: str
    label_en: str
    label_zh: str
    region: str
    visible_text_en: str | None
    visible_text_zh: str | None
    shop_name: str | None
    note: str | None

class Annotation(StrictModel):
    summary_en: str
    summary_zh: str
    signs: list[Sign]
    objects: list[SceneObject]
    uncertain: list[SceneObject]
    unknowns: list[str]

def stamp(): return datetime.now(timezone.utc).isoformat()
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def digest(raw): return hashlib.sha256(raw).hexdigest()
def write(path, value):
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    tmp.replace(path)

def source_bytes(row):
    with zipfile.ZipFile(ROOT/row['source_archive']) as archive:
        raw=archive.read(row['source_image'])
    assert digest(raw)==row['source_sha256'], 'Original hash mismatch'
    with Image.open(io.BytesIO(raw)) as im:
        assert list(im.size)==row['source_image_size']
    return raw

def api_image(row):
    original=source_bytes(row)
    if IMAGE_MODE=='native': return original,'image/jpeg'
    path=ROOT/row['input_image_path']
    raw=path.read_bytes()
    assert digest(raw)==row['input_sha256'], 'Inspection image hash mismatch'
    with Image.open(io.BytesIO(raw)) as image:
        assert list(image.size)==[1536,864]==row['input_image_size']
        actual=image.convert('RGB').tobytes()
    with Image.open(io.BytesIO(original)) as image:
        expected=image.convert('RGB').resize((1536,864)).tobytes()
    assert actual==expected, 'Inspection pixels differ from the earlier resize procedure'
    return raw,'image/png'

def prepare():
    begin=time.perf_counter()
    if (OUT/'manifest.json').exists():
        validate_local();print('Existing prepared pilot validated; no changes.');return
    OUT.mkdir(parents=True,exist_ok=True)
    all_rows=[json.loads(s) for s in (ROOT/'release/huggingface/scene_manifest.jsonl').read_text(encoding='utf-8').splitlines()]
    selected=[]
    for scene in IDS:
        r=next(x for x in all_rows if x['image_id']==scene)
        r={k:r[k] for k in ['image_id','source_archive','source_image','source_sha256','source_image_size']}
        original=source_bytes(r)
        if IMAGE_MODE=='inspection':
            path=ROOT/'data/prompt-comparison-20261005'/(scene+'.png')
            raw=path.read_bytes()
            r.update(input_image_path=path.relative_to(ROOT).as_posix(),input_sha256=digest(raw),
                input_image_size=[1536,864],input_mime_type='image/png',input_bytes=len(raw))
            api_image(r)
        selected.append(r)
    schema=Annotation.model_json_schema()
    def inspect_schema(node):
        if isinstance(node,dict):
            if node.get('type')=='object':
                assert node.get('additionalProperties') is False
                assert set(node['required'])==set(node['properties'])
            for value in node.values(): inspect_schema(value)
        elif isinstance(node,list):
            for value in node: inspect_schema(value)
    inspect_schema(schema)
    write(OUT/'schema.json',schema)
    (OUT/'instructions.txt').write_bytes(PROMPT.read_bytes())
    write(OUT/'manifest.json',dict(created_at_utc=stamp(),selected=selected,
        prompt_sha256=digest(PROMPT.read_bytes()),schema_sha256=digest((OUT/'schema.json').read_bytes()),
        concurrency=3,reasoning_effort='medium',image_detail='high',max_output_tokens=8000,image_mode=IMAGE_MODE,
        production_sha256={p:digest((ROOT/p).read_bytes()) for p in PRODUCTION},
        preparation_seconds=round(time.perf_counter()-begin,3)))
    validate_local();print('Prepared four hash-verified '+IMAGE_MODE+' inputs and strict six-field schema; no network requests.')

def validate_local():
    manifest=read(OUT/'manifest.json')
    assert [r['image_id'] for r in manifest['selected']]==IDS
    assert digest(PROMPT.read_bytes())==manifest['prompt_sha256']==digest((OUT/'instructions.txt').read_bytes())
    assert digest((OUT/'schema.json').read_bytes())==manifest['schema_sha256']
    assert manifest.get('image_mode','native')==IMAGE_MODE
    if IMAGE_MODE=='inspection':
        baseline=read(NATIVE_OUT/'manifest.json')
        for key in ['prompt_sha256','schema_sha256','concurrency','reasoning_effort','image_detail','max_output_tokens','production_sha256']:
            assert manifest[key]==baseline[key], 'Uncontrolled setting change: '+key
        assert (OUT/'instructions.txt').read_bytes()==(NATIVE_OUT/'instructions.txt').read_bytes()
        assert (OUT/'schema.json').read_bytes()==(NATIVE_OUT/'schema.json').read_bytes()
        for row in manifest['selected']: api_image(row)
    for p,h in manifest['production_sha256'].items():
        assert digest((ROOT/p).read_bytes())==h, 'Production records changed since preparation'
    return manifest

async def run():
    manifest=validate_local()
    cfg=tomllib.loads((Path.home()/'.codex/config.toml').read_text(encoding='utf-8'))
    assert cfg['model_provider']=='azure' and cfg['model']=='gpt-6-astra'
    provider=cfg['model_providers']['azure']
    endpoint=provider['base_url'].rstrip('/')+'/'
    parsed=urlparse(endpoint)
    assert parsed.scheme=='https' and not parsed.username and not parsed.password
    assert parsed.hostname and parsed.hostname.endswith('.azure.com')
    assert provider['wire_api']=='responses'
    secret=os.environ.get(provider['env_key'])
    assert secret, 'Configured API credential is unavailable'
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    def safe(value):
        if isinstance(value,str): return value.replace(secret,'[REDACTED]')
        if isinstance(value,list): return [safe(x) for x in value]
        if isinstance(value,dict): return {k:safe(v) for k,v in value.items()}
        return value
    prompt=(OUT/'instructions.txt').read_text(encoding='utf-8')
    schema=read(OUT/'schema.json')
    sem=asyncio.Semaphore(manifest['concurrency'])
    run_start=time.perf_counter();started=stamp();events=[]
    # SDK retries disabled so every explicit attempt is recorded.
    async with httpx.AsyncClient(timeout=240,follow_redirects=False) as transport:
      async with AsyncOpenAI(api_key=secret,base_url=endpoint,max_retries=0,http_client=transport) as client:
        async def worker(row):
            scene=row['image_id'];result_path=OUT/(scene+'.result.json')
            if result_path.exists() and read(result_path).get('status')=='completed':
                print(scene+' already completed; skipped.',flush=True);return
            queued=time.perf_counter()
            async with sem:
                item=dict(image_id=scene,source_sha256=row['source_sha256'],queued_at_utc=started,
                    queue_seconds=round(time.perf_counter()-queued,3),attempts=[],requested_model=cfg['model'],
                    requested_reasoning='medium',provider='azure',status='running')
                write(result_path,item)
                raw,mime=api_image(row)
                url='data:'+mime+';base64,'+base64.b64encode(raw).decode('ascii')
                item.update(input_image_size=row.get('input_image_size',row['source_image_size']),
                    input_sha256=digest(raw),input_mime_type=mime,input_bytes=len(raw))
                write(result_path,item)
                for attempt in range(1,4):
                    sent=stamp();begin=time.perf_counter()
                    print(scene+' request '+str(attempt)+' started.',flush=True)
                    try:
                        response=await client.responses.create(
                            model=cfg['model'],reasoning={'effort':'medium'},store=False,
                            instructions=prompt,
                            input=[{'role':'user','content':[
                                {'type':'input_text','text':'Annotate this exact photograph using the established six-field format.'},
                                {'type':'input_image','image_url':url,'detail':'high'}]}],
                            text={'format':{'type':'json_schema','name':'station_scene_annotation','strict':True,'schema':schema}},
                            max_output_tokens=manifest['max_output_tokens'])
                        received=stamp();elapsed=round(time.perf_counter()-begin,3)
                        attempt_meta=dict(attempt=attempt,sent_at_utc=sent,received_at_utc=received,
                            request_seconds=elapsed,response_status=response.status)
                        item['attempts'].append(attempt_meta)
                        # Store response only, never request headers, credential or image payload.
                        write(OUT/(scene+f'.response-{attempt}.json'),safe(response.model_dump(mode='json')))
                        item.update(returned_model=response.model,response_id=response.id,
                            provider_request_id=getattr(response,'_request_id',None),
                            usage=response.usage.model_dump(mode='json') if response.usage else None)
                        if response.status!='completed' or not response.output_text:
                            item.update(status='incomplete_or_refused',saved_at_utc=stamp())
                            write(result_path,safe(item));break
                        save_begin=time.perf_counter()
                        annotation=Annotation.model_validate_json(response.output_text)
                        write(OUT/(scene+'.annotation.json'),safe(annotation.model_dump(mode='json')))
                        item.update(status='completed',saved_at_utc=stamp(),
                            annotation_sha256=digest((OUT/(scene+'.annotation.json')).read_bytes()),
                            parse_and_annotation_save_seconds=round(time.perf_counter()-save_begin,4))
                        write(result_path,safe(item))
                        print(scene+' completed in '+str(elapsed)+' s; tokens '+str(item['usage']['total_tokens'] if item['usage'] else 'unavailable')+'.',flush=True)
                        break
                    except (APIStatusError,APIConnectionError) as exc:
                        status=getattr(exc,'status_code',None)
                        error=dict(attempt=attempt,sent_at_utc=sent,failed_at_utc=stamp(),
                            request_seconds=round(time.perf_counter()-begin,3),error_type=type(exc).__name__,http_status=status)
                        body=getattr(exc,'body',None)
                        if isinstance(body,dict):
                            detail=body.get('error',body)
                            if isinstance(detail,dict):
                                error['provider_error_code']=detail.get('code')
                                error['provider_error_message']=safe(str(detail.get('message','')))[:600]
                        item['attempts'].append(error);item['status']='failed';write(result_path,safe(item))
                        print(scene+' failed: '+type(exc).__name__+' HTTP '+str(status)+'.',flush=True)
                        if isinstance(exc,APIConnectionError):
                            # Surface connection/sandbox failure for review rather than blind replay.
                            break
                        if attempt==3 or status not in [429,500,502,503,504]: break
                        retry=getattr(exc,'response',None)
                        retry_value=retry.headers.get('retry-after','') if retry is not None else ''
                        try: delay=min(60,max(1,float(retry_value)))
                        except ValueError: delay=2**attempt
                        error['retry_wait_seconds']=delay;write(result_path,safe(item))
                        await asyncio.sleep(delay)
                    except Exception as exc:
                        item.update(status='local_validation_or_save_error',error_type=type(exc).__name__,saved_at_utc=stamp())
                        write(result_path,safe(item));print(scene+' local failure: '+type(exc).__name__,flush=True);break
                events.append({'image_id':scene,'status':item['status']})
        await asyncio.gather(*(worker(r) for r in manifest['selected']))
    run_record=dict(started_at_utc=started,finished_at_utc=stamp(),wall_seconds=round(time.perf_counter()-run_start,3),
        concurrency=3,events=events,scope='client setup, local source encoding, API queue/request/retry time, parsing and saving; excludes preparation and later comparison')
    history=read(OUT/'runs.json') if (OUT/'runs.json').exists() else []
    history.append(run_record);write(OUT/'runs.json',history)
    validate_local();print(json.dumps(run_record),flush=True)

def report():
    manifest=validate_local();results=[];totals={k:0 for k in ['input_tokens','output_tokens','total_tokens','reasoning_tokens','cached_input_tokens']}
    for row in manifest['selected']:
        scene=row['image_id'];item=read(OUT/(scene+'.result.json'))
        if item['status']=='completed':
            raw=(OUT/(scene+'.annotation.json')).read_bytes()
            assert digest(raw)==item['annotation_sha256'];annotation=Annotation.model_validate_json(raw)
            usage=item.get('usage') or {}
            for k in ['input_tokens','output_tokens','total_tokens']:totals[k]+=usage.get(k,0)
            totals['reasoning_tokens']+=(usage.get('output_tokens_details') or {}).get('reasoning_tokens',0)
            totals['cached_input_tokens']+=(usage.get('input_tokens_details') or {}).get('cached_tokens',0)
            results.append(dict(image_id=scene,status=item['status'],returned_model=item.get('returned_model'),
                attempts=item['attempts'],queue_seconds=item['queue_seconds'],usage=usage,
                signs=len(annotation.signs),objects=len(annotation.objects),uncertain=len(annotation.uncertain),
                parse_and_annotation_save_seconds=item['parse_and_annotation_save_seconds']))
        else:results.append(item)
    summary=dict(results=results,usage_totals=totals,runs=read(OUT/'runs.json'),
        production_unchanged=True,preparation_seconds=manifest['preparation_seconds'],image_mode=IMAGE_MODE)
    write(OUT/'summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run','report'])
    parser.add_argument('--image-mode',choices=['native','inspection'],default='native')
    args=parser.parse_args()
    action=args.action
    IMAGE_MODE=args.image_mode
    if IMAGE_MODE=='inspection': OUT=ROOT/'data/direct-api-pilot-1536-20261005'
    if action=='prepare':prepare()
    elif action=='run':asyncio.run(run())
    else:report()
