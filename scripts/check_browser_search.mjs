import assert from 'node:assert/strict';
import fs from 'node:fs';
import {search} from '../demo/search.mjs';

const data = JSON.parse(fs.readFileSync(new URL('../demo/search-data.json', import.meta.url), 'utf8'));
// Stable, individually reviewed regression fixtures; later records participate
// in the full-corpus Python/JavaScript parity checks below.
const fixtureData = {...data, records: data.records.filter(r => Number(r.image_id.split('-').at(-1)) <= 32)};
const ids = (q, mode='all') => search(fixtureData,q,mode).results.map(h=>h.record.image_id).sort();
const scene = n => `tps-scene-${String(n).padStart(3,'0')}`;
for (const q of ['airport buses','機場巴士','Airport Express','机场巴士']) assert.deepEqual(ids(q),[1,2,11,14,16].map(scene).sort(),q);
for (const q of ['Taoyuan Airport MRT','AIRPORT-MRT','機場捷運','機捷','airport train']) assert.deepEqual(ids(q),[8,9,10,13,18,20,21,26,27,28,31,32].map(scene),q);
for (const q of ['Taipei Bus Station','臺北轉運站','台北轉運站','台北转运站']) assert.deepEqual(ids(q),[6,11,19].map(scene),q);
for (const q of ['airport buses','機場捷運','Taipei Bus Station','廁所','check-in','電梯']) assert.deepEqual(ids(q,'visible'),[],q);
assert.deepEqual(ids('lockers','visible'),[scene(6)]);
assert.deepEqual(ids('廁所','signs'),[3,4,6,26,27,31].map(scene));
assert.deepEqual(ids('stairs','visible'),[5,24,25,26,27,28,29].map(scene));
assert.deepEqual(ids('stairs','signs'),[3,10].map(scene));
assert.deepEqual(ids('interactive terminal'),[]);
for (const q of ['Taipei City Mall','台北地下街']) {
  assert.deepEqual(ids(q,'signs'),[6,7,10,11,12,13,19].map(scene).sort(),q);
  assert.deepEqual(ids(q,'visible'),[],q);
}
assert.ok(ids('西停車場','signs').includes(scene(13)));
assert.ok(ids('shopfront','visible').includes(scene(13)));
assert.deepEqual(ids('new balance','visible'),[scene(19)]);
assert.deepEqual(ids('new balance','signs'),[]);
assert.deepEqual(ids('臺鐵便當本舖','visible'),[scene(21)]);
assert.deepEqual(ids('K區地下街','visible'),[]);
for (const q of ['K區地下街','K Underground Mall']) assert.deepEqual(ids(q,'signs'),[scene(31)]);
for (const q of ['Zhongshan Metro Mall','中山地下街']) assert.deepEqual(ids(q,'signs'),[6,14,16].map(scene));
assert.deepEqual(ids('nonexistentdestination'),[]);
assert.deepEqual(ids('none'),[]);
assert.equal(search(data,'').results.length,Math.min(50,data.progress.scene_records));
assert.equal(search(data,'').total_count,data.progress.scene_records);
const pinned = data.records.filter(r => r.browse_priority !== undefined).sort((a,b) => a.browse_priority-b.browse_priority);
assert.deepEqual(search(data,'').results.slice(0,pinned.length).map(h=>h.record.image_id),pinned.map(r=>r.image_id));
const allScenes = search(data,'','all',data.progress.scene_records);
assert.equal(allScenes.results.length,data.progress.scene_records);
assert.equal(new Set(allScenes.results.map(h=>h.record.image_id)).size,data.progress.scene_records);
const batchOne = data.records.filter(r => {
  const n = Number(r.image_id.split('-').at(-1));
  return n >= 33 && n <= 52;
});
assert.equal(batchOne.length,20);
assert.deepEqual(search({...data,records:batchOne},'airport buses','signs').results.map(h=>h.record.image_id).sort(),batchOne.map(r=>r.image_id).sort());
assert.deepEqual(search({...data,records:batchOne},'Airport MRT').results,[]);
assert.equal(search(data,'airport').llm_called,false);
assert.throws(()=>search(data,'','invalid'));
// Relative assets must stay beneath the GitHub project prefix.
const base = new URL('https://example.github.io/TaipeiSignRAG/demo/app.js');
assert.equal(new URL('./search-data.json',base).pathname,'/TaipeiSignRAG/demo/search-data.json');
assert.equal(new URL('../release/huggingface/scene_images/scene_011.png',base).pathname,'/TaipeiSignRAG/release/huggingface/scene_images/scene_011.png');
const cases = JSON.parse(fs.readFileSync(0,'utf8'));
for (const test of cases) {
  const actual=search(data,test.query,test.mode);
  assert.equal(actual.total_count,test.total_count,`${test.query} total / ${test.mode}`);
  assert.deepEqual(actual.results.map(h=>[h.record.image_id,h.ranking_score,h.matched_categories,h.matched_transport]),test.hits,`${test.query} / ${test.mode}`);
}
console.log(`Browser checks passed, including ${cases.length} Python/JavaScript parity cases.`);
