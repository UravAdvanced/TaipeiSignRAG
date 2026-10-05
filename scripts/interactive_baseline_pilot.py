"""Offline timing/integrity ledger for four interactive annotations; no inference."""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/interactive-baseline-20261005'
CP = OUT / 'checkpoint.json'
IDS = ['003', '006', '029', '190']
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

action = sys.argv[1]
if action == 'prepare':
    assert not CP.exists(), 'Existing trial must not be overwritten'
    manifest = read(ROOT/'data/direct-api-pilot-1536-20261005/manifest.json')
    for row in manifest['selected']:
        p = ROOT/row['input_image_path']
        assert sha(p) == row['input_sha256']
        with Image.open(p) as im: assert im.size == (1536, 864)
    OUT.mkdir(parents=True, exist_ok=True)
    write(CP, dict(prepared_at_utc=now(), selected=manifest['selected'],
        production_sha256=manifest['production_sha256'], images={},
        protocol='Sequential interactive Codex inspection and concise six-field authoring; one view per photo in this trial; prior exposure to images and answers; not blinded or independent.',
        timing_scope='From before first image tool call through final annotation validation/save; includes reasoning, authoring, tools and between-image overhead; excludes helper preparation and later comparison.',
        serving_model='Not independently verified against historical Codex or API serving model',
        workflow_policy_sha256=sha(ROOT/'docs/WHOLE_SCENE_ANNOTATION.md')))
    print('Prepared exact four inspection images; production and prior trials untouched.')
elif action == 'start':
    cp = read(CP); scene = sys.argv[2]
    assert scene in IDS and scene not in cp['images']
    assert all('saved_at_utc' in r for r in cp['images'].values())
    stamp = now(); tick = time.perf_counter()
    cp.setdefault('started_at_utc', stamp); cp.setdefault('start_monotonic', tick)
    cp['images'][scene] = dict(started_at_utc=stamp, start_monotonic=tick)
    write(CP, cp); print('Started scene '+scene+' at '+stamp)
elif action == 'save':
    cp = read(CP); scene = sys.argv[2]; row = cp['images'][scene]
    assert 'saved_at_utc' not in row
    p = OUT/('tps-scene-'+scene+'.annotation.json'); annotation = read(p)
    assert set(annotation) == {'summary_en','summary_zh','signs','objects','uncertain','unknowns'}
    assert isinstance(annotation['summary_en'], str) and isinstance(annotation['summary_zh'], str)
    assert all(isinstance(annotation[k], list) for k in ['signs','objects','uncertain','unknowns'])
    row.update(saved_at_utc=now(), elapsed_seconds=round(time.perf_counter()-row['start_monotonic'],3), annotation_sha256=sha(p))
    if len(cp['images']) == 4:
        cp.update(finished_at_utc=now(), wall_seconds=round(time.perf_counter()-cp['start_monotonic'],3))
    write(CP, cp); print(json.dumps(row))
elif action == 'report':
    cp = read(CP); assert 'finished_at_utc' in cp
    assert all(sha(ROOT/p)==h for p,h in cp['production_sha256'].items())
    for scene, row in cp['images'].items(): assert sha(OUT/('tps-scene-'+scene+'.annotation.json'))==row['annotation_sha256']
    print(json.dumps(dict(wall_seconds=cp['wall_seconds'], images=cp['images'], production_unchanged=True), indent=2))
else: raise ValueError(action)
