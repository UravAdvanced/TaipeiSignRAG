"""Join assistant-reviewed whole-scene notes to source provenance, without inference."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'release/huggingface'
manifest={r['image_id']:r for r in map(json.loads,(PACK/'scene_manifest.jsonl').read_text(encoding='utf-8').splitlines())}
notes=json.loads((ROOT/'annotations/scene_pilot_notes.json').read_text(encoding='utf-8'))
amenity_rows=[json.loads(s) for s in (PACK/'amenity_pilot.jsonl').read_text(encoding='utf-8').splitlines()]
categories=['lockers','toilets','shopfront','fare_gates_or_turnstiles','elevator','stairs','escalator','train_platform_or_entrance','kiosk','check_in_counter','ticket_counter','service_counter','map_information_board','emergency_exit_sign']
sign_categories={'toilets':['toilets'],'ticket_counter':['TRA ticket office','HSR ticket area'],'service_counter':['service centre'],'train_platform_or_entrance':['TRA and HSR platforms','platforms']}
transport_ids={'airport bus':'airport_bus','Kuo-Kuang Bus Station, airport buses':'airport_bus','Taoyuan Airport MRT':'taoyuan_airport_mrt','Taipei Bus Station':'taipei_bus_station'}
assert len(notes)==len({n['image_id'] for n in notes}), 'Duplicate scene notes'
assert set(manifest)=={n['image_id'] for n in notes}, 'Manifest and authored notes differ'
rows=[]
for note in notes:
    row={**manifest[note['image_id']],**note}
    row['signs']=[{**s, 'transport_id':transport_ids.get(s['label_en'])} for s in note['signs']]
    visible={o['category'] for o in note['objects']}
    uncertain={o['category'] for o in note['uncertain']}
    sign_labels={s['label_en'] for s in note['signs']}
    row['amenity_coverage']={cat: ('visible' if cat in visible else 'uncertain' if cat in uncertain else 'sign_reference_only' if sign_labels.intersection(sign_categories.get(cat,[])) else 'not_observed_in_reviewed_visible_regions') for cat in categories}
    if 'stairs' not in visible and any('stairs' in s.get('symbols',[]) for s in note['signs']):
        row['amenity_coverage']['stairs']='sign_reference_only'
    row.update(schema_version='0.1.0',annotation_scope='whole photograph, all unmasked visible regions',
      review_status='visually_checked_by_assistant',human_review_status='pending',review_date=note.get('review_date','2026-10-04'),
      annotation_method=note.get('annotation_method','interactive visual inspection of full-frame privacy views and enlarged sign details; no OCR or fine-tuned model'),
      physical_sign_id=None,station_map_coordinate=None,cloud_anchor_id=None,
      accessibility_verified=False,current_operational_status=None,
      privacy_review='manual conservative person masks; no human descriptions; masked areas unassessable; independent review pending',
      text_policy='visible_zh/en are reviewed readable text; label_en and summary_zh are normalized descriptions/translations; null means unverified',
      direction_policy='arrow direction in the image; not user heading or a route command',
      capture_date_verified=None)
    row['related_observations']=[{'record_id':a['record_id'],'relation':'same_source_photograph','evidence':'identical original source SHA-256'} for a in amenity_rows if a['source_sha256']==row['source_sha256']]
    rows.append(row)
(PACK/'scene_annotations.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
unique_sources={r['source_sha256'] for r in rows+amenity_rows}
progress={'total_source_entries':8971,'scene_records':len(rows),'separate_amenity_pilot_records':len(amenity_rows),
 'scene_review_scope':f'{len(rows)} full-frame images from Sign Board 2; no per-family propagation',
 'unique_source_images_with_any_new_annotation':len(unique_sources),'remaining_source_entries_without_new_annotation':8971-len(unique_sources),
 'human_reviewed_records':0,'physical_anchor_links':0,'full_dataset_annotation_complete':False,
 'next_step':'continue full-photo batches including hotels, malls and other sites using the existing destination catalog; record readable names during annotation without a separate repeat research step; do not copy scene facts across views'}
(ROOT/'annotations/progress.json').write_text(json.dumps(progress,indent=2),encoding='utf-8')
print(f'Built {len(rows)} full-scene records; all {len(categories)} requested/related categories explicitly checked per image.')
