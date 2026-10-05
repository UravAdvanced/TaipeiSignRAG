"""Functional transport/evidence checks, provenance checks, and static HTTP smoke test."""
import hashlib
import json
import subprocess
import threading
import zipfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen
from PIL import Image
from scene_rag_demo import ROOT, PACK, ALIASES, TRANSPORT_ALIASES, DESTINATION_ALIASES, records, search, Handler

policy_path=ROOT/'annotations/publication_policy.json'
if policy_path.exists():
    policy=json.loads(policy_path.read_text(encoding='utf-8'))
    files=sorted((PACK/'scene_images').glob('*'))
    digest='\n'.join(p.name+':'+hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file())
    assert len(files)==policy['legacy_scene_image_count']==128
    assert hashlib.sha256(digest.encode()).hexdigest()==policy['legacy_scene_image_digest'], 'Previously published image changed'

rows=records()
data=json.loads((ROOT/'demo/search-data.json').read_text(encoding='utf-8'))
assert data['records']==rows
progress=json.loads((ROOT/'annotations/progress.json').read_text(encoding='utf-8'))
assert data['progress']==progress
amenities=[json.loads(line) for line in (PACK/'amenity_pilot.jsonl').read_text(encoding='utf-8').splitlines()]
unique={r['source_sha256'] for r in rows+amenities}
notes=json.loads((ROOT/'annotations/scene_pilot_notes.json').read_text(encoding='utf-8'))
assert progress['scene_records']==len(rows)==len(notes)
assert {r['image_id'] for r in rows}=={n['image_id'] for n in notes}
assert len(rows)==len({r['source_sha256'] for r in rows}), 'Duplicate source photographs'
assert progress['unique_source_images_with_any_new_annotation']==len(unique)
assert progress['remaining_source_entries_without_new_annotation']==8971-len(unique)
with zipfile.ZipFile(ROOT/'Taipei Station Sign Board 2.v1i.coco.zip') as archive:
    for row in rows:
        assert hashlib.sha256(archive.read(row['source_image'])).hexdigest()==row['source_sha256']
        assert row['human_review_status']=='pending'
        assert row['station_map_coordinate'] is None and row['cloud_anchor_id'] is None
        assert len(row['amenity_coverage'])==14
        if row.get('publication_mode')=='annotations_only':
            assert row['evidence_image'] is None and row['privacy_masks_xyxy']==[]
            assert int(row['image_id'].split('-')[-1])>=129
            assert row['visual_review_passes']==1
            assert row['review_status']=='single_cloud_annotation_pass'
            assert not (PACK/'scene_images'/f"scene_{row['image_id'].split('-')[-1]}.png").exists()
        else:
            with Image.open(PACK/row['evidence_image']) as im:
                assert list(im.size)==row['source_image_size']
                for x1,y1,x2,y2 in row['privacy_masks_xyxy']:
                    assert 0<=x1<x2<=im.width and 0<=y1<y2<=im.height
                    assert im.crop((x1,y1,x2,y2)).getextrema()==((45,45),(45,45),(45,45))
        for obj in row['objects']:
            if 'bbox_xyxy' not in obj:
                assert row.get('publication_mode')=='annotations_only' and obj.get('region')
                continue
            x1,y1,x2,y2=obj['bbox_xyxy']
            assert 0<=x1<x2<=512 and 0<=y1<y2<=288
plain=[json.loads(line) for line in (PACK/'dataset_file_annotations.jsonl').read_text(encoding='utf-8').splitlines()]
assert len(plain)==len(rows)
for entry,row in zip(plain,rows):
    assert set(entry)=={'dataset','file_name','source_sha256','annotations'}
    assert entry['dataset']==row['source_archive'] and entry['file_name']==row['source_image']
    assert entry['source_sha256']==row['source_sha256']
    assert entry['annotations']['signs']==row['signs'] and entry['annotations']['objects']==row['objects']
    assert 'evidence_image' not in entry['annotations']
assert progress['annotations_only_records']==sum(r.get('publication_mode')=='annotations_only' for r in rows)
queries=['','AIRPORT-MRT','where are the airport buses','台北轉運站','機場捷運報到','none','nonexistentdestination','airport','Taipei City Mall','台北地下街','West Parking','西停車場','new balance','臺鐵便當本舖','K區地下街','K Underground Mall']
queries += [alias for terms in {**ALIASES,**TRANSPORT_ALIASES,**DESTINATION_ALIASES}.values() for alias in terms]
cases=[]
for query in queries:
    for mode in ('all','visible','signs'):
        result=search(query,mode)
        cases.append({'query':query,'mode':mode,'total_count':result['total_count'],'hits':[[h['record']['image_id'],h['ranking_score'],h['matched_categories'],h['matched_transport']] for h in result['results']]})
subprocess.run(['node',str(ROOT/'scripts/check_browser_search.mjs')],input=json.dumps(cases,ensure_ascii=False),encoding='utf-8',check=True)
class QuietStatic(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
for handler, paths in [
    (partial(QuietStatic,directory=str(ROOT/'_site')),['/','/demo/','/demo/catalog.html','/annotations/destination_catalog.json','/demo/app.js','/demo/search.mjs','/demo/search-data.json','/release/huggingface/scene_images/scene_011.png','/release/huggingface/ATTRIBUTION.md']),
    (Handler,['/','/catalog.html','/annotations/destination_catalog.json','/app.js','/search.mjs','/search-data.json','/release/huggingface/scene_images/scene_011.png','/release/huggingface/ATTRIBUTION.md','/api/search?q=airport%20buses'])
]:
    server=ThreadingHTTPServer(('127.0.0.1',0),handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        paths=paths+['/release/huggingface/dataset_file_annotations.jsonl']
        for path in paths:
            with urlopen(f'http://127.0.0.1:{server.server_port}{path}') as response:
                assert response.status==200 and response.read()
                if path.endswith(('.js','.mjs')): assert 'javascript' in response.headers['Content-Type']
    finally:
        server.shutdown();server.server_close();thread.join()
print('Source hashes, masks, counts, static site routes and local API routes passed. Expert review remains pending.')
