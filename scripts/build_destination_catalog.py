"""Render the authored destination inventory without changing scene evidence."""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
PHOTO = {'readable_in_sample': 'Readable in sampled image / 樣本可讀', 'pending_photo_match': 'Photo match pending / 待照片對照', 'unresolved_candidate': 'Unresolved historical candidate / 歷史名稱待查'}
WEB = {'official_page_read': 'Official page read', 'secondary_page_read': 'Secondary page read; official check incomplete', 'secondary_and_official_search_listing': 'Secondary page + official search listing; official page blocked', 'unresolved': 'Online identity unresolved', 'historical_identity_unresolved': 'Historical identity unresolved', 'not_checked': 'Not checked online; photo evidence recorded'}
e = html.escape


def build():
    data = json.loads((ROOT / 'annotations/destination_catalog.json').read_text(encoding='utf-8'))
    sources = {s['id']: s for s in data['sources']}
    rows = data['destinations']
    scenes = {r['image_id']: r for r in map(json.loads, (ROOT / 'release/huggingface/scene_annotations.jsonl').read_text(encoding='utf-8').splitlines())}
    assert len(sources) == len(data['sources'])
    assert len({r['id'] for r in rows}) == len(rows)
    assert all(s['url'].startswith('https://') for s in sources.values())
    for row in rows:
        assert row['photo_status'] in PHOTO and row['web_status'] in WEB
        assert row['category'] in ('hotel', 'shopping')
        assert set(row['source_ids']) <= sources.keys()
        assert bool(row['photo_evidence']) == (row['photo_status'] == 'readable_in_sample')
        for ref in row['photo_evidence']:
            if 'scene_id' in ref:
                scene = scenes[ref['scene_id']]
                visible_text = ' '.join(str(item.get(key) or '') for item in scene['signs'] + scene['objects'] for key in ('visible_zh', 'visible_en', 'visible_text_zh', 'visible_text_en')).replace('臺', '台')
                assert row['name_zh'].replace('臺', '台') in visible_text, (row['id'], ref)
            else:
                assert re.fullmatch('[a-f0-9]{64}', ref['sha256'])
                assert not Path(ref['path']).is_absolute() and '..' not in Path(ref['path']).parts
    for group in data['sign_checklist']:
        assert set(group['source_ids']) <= sources.keys()

    def links(ids):
        return ' · '.join(f'<a href="{e(sources[i]["url"], quote=True)}">{e(sources[i]["title"])}</a>' for i in ids) or 'No confirming web source yet.'

    def is_supplemental_photo(ref):
        return ref.get('path', '').startswith('demo/supplemental_images/')

    def photo_label(row):
        if any(is_supplemental_photo(ref) for ref in row['photo_evidence']):
            return 'Readable in supplemental demo photo / 補充示範照片可讀'
        return PHOTO[row['photo_status']]

    cards = []
    md = ['# Destination and sign-name inventory', '', f'**{data["team"]}**', '', f'**{data["project"]}**', '', f'Researched {data["review_date"]}.', '', data['scope'], '', data['limitations'], '', data['review_method'], '', '## Hotels and shopping', '', '| Name | Photo evidence | Online check |', '| --- | --- | --- |']
    for row in rows:
        evidence = []
        photo_figures = []
        for ref in row['photo_evidence']:
            if 'scene_id' in ref:
                scene = scenes[ref['scene_id']]
                if scene.get('evidence_image'):
                    evidence.append(f'<a href="../release/huggingface/{e(scene["evidence_image"], quote=True)}">{e(ref["scene_id"])}: masked whole photograph</a>')
                else:
                    evidence.append(f'{e(ref["scene_id"])}: annotations only<br><code>{e(scene["source_archive"])} → {e(scene["source_image"])}</code>')
            elif is_supplemental_photo(ref):
                image_name = Path(ref['path']).name
                image_file = ROOT / ref['path']
                assert image_file.is_file(), image_file
                image_url = './supplemental_images/' + quote(image_name)
                photo_figures.append(f'<figure class="evidence-photo"><a href="{image_url}"><img src="{image_url}" loading="lazy" alt="User-supplied photo evidence for {e(row["name_en"], quote=True)}"></a><figcaption>User-supplied supplemental demo photo; excluded from the core TibaMe POC dataset.</figcaption></figure>')
                evidence.append(f'<a href="{image_url}">View supplemental photograph: {e(image_name)}</a><br>{e(ref["archive"])}<br>SHA-256: <code>{ref["sha256"]}</code>')
            else:
                evidence.append(f'{e(ref["archive"])}<br><code>{e(ref["path"])}</code><br>SHA-256: <code>{ref["sha256"]}</code>')
        evidence_html = '<ul>' + ''.join(f'<li>{item}</li>' for item in evidence) + '</ul>' if evidence else '<p>No exact photo evidence linked yet.</p>'
        search_text = ' '.join([row['name_zh'], row['name_en'], *row['aliases'], 'hotels 飯店 酒店' if row['category'] == 'hotel' else 'malls shopping 商場 購物'])
        image_search = './index.html?q=' + quote(row['name_en'], safe='')
        cards.append(f'''<article id="{e(row['id'])}" data-category="{row['category']}" data-status="{row['photo_status']}" data-search="{e(search_text, quote=True)}">
<h2>{e(row['name_en'])}<br><span lang="zh-Hant">{e(row['name_zh'])}</span></h2>
<p class="badge {row['photo_status']}">{photo_label(row)}</p>
<p><strong>Online check:</strong> {WEB[row['web_status']]}</p><p>{e(row['note'])}</p>{''.join(photo_figures)}<p><a class="search-link" href="{image_search}">Search image evidence / 搜尋照片證據</a></p>
<details><summary>Evidence, aliases and sources / 證據與來源</summary><p>Aliases: {e(', '.join(row['aliases']))}</p>{evidence_html}<p>{links(row['source_ids'])}</p></details></article>''')
        md.append(f'| {row["name_en"]} / {row["name_zh"]} | {photo_label(row)} | {WEB[row["web_status"]]} |')
    md += ['', '## Entry notes and evidence', '']
    for row in rows:
        md += [f'### {row["name_en"]} / {row["name_zh"]}', '', row['note'], '', 'Aliases: ' + ', '.join(row['aliases']) + '.', '']
        for ref in row['photo_evidence']:
            if 'scene_id' in ref:
                scene=scenes[ref['scene_id']]
                if scene.get('evidence_image'):
                    md.append(f'- [{ref["scene_id"]}](../release/huggingface/{scene["evidence_image"]}) — existing masked photograph.')
                else:
                    md.append(f'- {ref["scene_id"]}: annotations only; `{scene["source_archive"]}` → `{scene["source_image"]}`.')
            elif is_supplemental_photo(ref):
                md.append(f'- ![Supplemental photo evidence for {row["name_en"]}](../demo/supplemental_images/{Path(ref["path"]).name}) — user-supplied demo photograph, outside the TibaMe POC dataset.')
            else:
                md.append(f'- `{ref["archive"]}` → `{ref["path"]}`; SHA-256 `{ref["sha256"]}`. Exact CLS crop, not a whole-photo record.')
        md += [f'- [{sources[i]["title"]}]({sources[i]["url"]}) — {sources[i]["access"]}' for i in row['source_ids']]
        md.append('')
    checklist = []
    md += ['## Broader sign checklist', '', 'These are review targets, not additional completed scene records.', '']
    for group in data['sign_checklist']:
        checklist.append(f'<section><h3>{e(group["category"])}</h3><p>{e(group["status"])}</p><ul>' + ''.join(f'<li>{e(label)}</li>' for label in group['labels']) + '</ul>' + (f'<p>{links(group["source_ids"])}</p>' if group['source_ids'] else '') + '</section>')
        md += [f'### {group["category"]}', '', group['status'], '', *[f'- {label}' for label in group['labels']], '']
    progress = json.loads((ROOT / 'annotations/progress.json').read_text(encoding='utf-8'))
    readable_tibame = sum(r['photo_status'] == 'readable_in_sample' and not any(is_supplemental_photo(ref) for ref in r['photo_evidence']) for r in rows)
    readable_supplemental = sum(any(is_supplemental_photo(ref) for ref in r['photo_evidence']) for r in rows)
    counts = (f'{readable_tibame} destination records have readable evidence in audited TibaMe images; {readable_supplemental} have evidence in separately supplied supplemental demo photographs; {sum(r["photo_status"] == "pending_photo_match" for r in rows)} candidates await photo matches, and {sum(r["photo_status"] == "unresolved_candidate" for r in rows)} historical candidate remains unresolved. The annotation checkpoint is {progress["scene_records"]} whole-photo records covering {progress["unique_source_images_with_any_new_annotation"]} unique originals together with the locker pilot. {progress["remaining_source_entries_without_new_annotation"]:,} TibaMe source entries remain without new annotations.')
    md += ['## Coverage and continuation', '', counts, '', 'The 204-scene annotation POC is closed; no more core annotation batches are planned. Future work begins with human verification, then app integration with separately confirmed map or anchor links. Keep current online names and historical printed text separate. Preserve the three separate transport categories: airport buses, Taoyuan Airport MRT and Taipei Bus Station.', '', 'Generated by `python scripts/build_destination_catalog.py` from [the authored JSON](../annotations/destination_catalog.json). Research responses and enlarged crops remain local; this page republishes authored findings, source links and the separately attributed supplemental demo photographs.', '']
    page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TaipeiSignRAG · Destination inventory</title><style>
:root{font-family:system-ui,sans-serif;color:#152a37;background:#f3f6f5}body{max-width:1150px;margin:auto;padding:24px}p,li{line-height:1.6}a{color:#075e57}.credit{background:#073f3b;color:white;padding:22px;border-radius:12px}.credit p{margin:4px 0}.credit strong{font-size:1.2rem}.notice{background:#e7efef;padding:16px;border-radius:8px}form{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}input,select{font:inherit;padding:12px;border:1px solid #91aaa7;border-radius:8px}input{flex:1;min-width:0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(330px,100%),1fr));gap:20px}article{background:white;border:1px solid #d4dfdd;border-radius:12px;padding:20px}article h2{font-size:1.2rem}article[hidden]{display:none}.badge{padding:8px;border-radius:5px;background:#fff0d1}.readable_in_sample{background:#dff1e7}.unresolved_candidate{background:#eee5f4}.evidence-photo{margin:14px 0}.evidence-photo img{display:block;width:100%;max-height:420px;object-fit:contain;background:#e7efef;border-radius:8px}.evidence-photo figcaption{font-size:.85rem;color:#425d59;margin-top:6px}.search-link{display:inline-block;font-weight:600;margin:8px 0}code{overflow-wrap:anywhere;font-size:.8rem}summary{cursor:pointer;font-weight:600}section{border-top:1px solid #c4d2cf;margin-top:24px}:focus-visible{outline:3px solid #bb6900;outline-offset:3px}footer{margin-top:32px}
</style></head><body>
'''
    page += f'''<header><div class="credit"><p><strong>{e(data['team'])}</strong></p><p>{e(data['project'])}</p><p>Urav Advanced Learning Systems Pvt Ltd.</p></div>
<p><a href="./">← Whole-photograph annotations / 全景照片標註</a></p><h1>Destination inventory / 目的地名稱清單</h1>
<p>Hotels, malls, shops and other sign names. Researched {data['review_date']}. {e(data['scope'])}</p></header>
<div class="notice"><strong>POC complete · expert review pending / 概念驗證完成 · 專家審核待完成</strong><p>{e(data['limitations'])}</p><p>{e(counts)}</p></div>
<form id="filters" role="search"><input id="q" type="search" aria-label="Search hotel and mall names in Chinese or English" placeholder="Cosmos, 天成, 京站, 地下街…">
<select id="category" aria-label="Destination category"><option value="">Hotels and shopping / 飯店與商店</option><option value="hotel">Hotels / 飯店</option><option value="shopping">Shopping / 購物</option></select>
<select id="status" aria-label="Photo evidence"><option value="">All photo statuses / 全部</option><option value="readable_in_sample">Readable in sample / 樣本可讀</option><option value="pending_photo_match">Photo match pending / 待對照</option><option value="unresolved_candidate">Unresolved candidate / 待查</option></select></form>
<p id="count" role="status" aria-live="polite">{len(rows)} destinations</p><noscript>All entries are shown below. Enable JavaScript to filter.</noscript>
<main class="grid">{''.join(cards)}</main><p id="empty" hidden>No matching name in this initial catalogue. Try another name or clear the filters.</p>
<h2>Other signs to inspect / 其他待檢視標誌</h2><p>This checklist guides the next image review; it does not add photo annotations. Airport buses, Taoyuan Airport MRT and Taipei Bus Station remain separate destinations.</p>{''.join(checklist)}
<details><summary>Research method and source-access limits</summary><p>{e(data['review_method'])}</p><ul>{''.join(f'<li><a href="{e(s["url"], quote=True)}">{e(s["title"])}</a>: {e(s["access"])}</li>' for s in sources.values())}</ul></details>
<footer><a href="../annotations/destination_catalog.json">Download catalogue JSON</a> · <a href="./">Review scene evidence</a> · <a href="../release/huggingface/ATTRIBUTION.md">Photo attribution</a><p>Photo-supported records link to scene search. Supplemental user-provided photos remain outside the core dataset. Search runs in your browser.</p></footer>
'''
    page += '''<script>
const q=document.querySelector('#q'),category=document.querySelector('#category'),status=document.querySelector('#status');
const cards=[...document.querySelectorAll('article')];
function normalize(value){return value.normalize('NFKC').toLowerCase().replaceAll('臺','台').replace(/\\s+/g,' ').trim();}
function filter(){const terms=normalize(q.value).split(' ').filter(Boolean);let count=0;
for(const card of cards){const match=(!category.value||category.value===card.dataset.category)&&(!status.value||status.value===card.dataset.status)&&terms.every(t=>normalize(card.dataset.search).includes(t));card.hidden=!match;if(match)count++;}
document.querySelector('#count').textContent=`${count} of ${cards.length} destinations / 目的地`;
document.querySelector('#empty').hidden=count!==0;}
q.value=new URLSearchParams(location.search).get('q')||'';
document.querySelector('#filters').addEventListener('submit',event=>{event.preventDefault();filter();});
q.addEventListener('input',filter);category.addEventListener('change',filter);status.addEventListener('change',filter);filter();
</script></body></html>
'''
    (ROOT / 'demo/catalog.html').write_text(page, encoding='utf-8')
    (ROOT / 'docs/DESTINATION_CATALOG.md').write_text('\n'.join(md), encoding='utf-8')
    print(f'Built destination catalogue: {len(rows)} names; scene evidence unchanged.')


if __name__ == '__main__':
    build()
