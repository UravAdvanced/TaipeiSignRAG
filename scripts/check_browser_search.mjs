import assert from 'node:assert/strict';
import fs from 'node:fs';
import {search} from '../demo/search.mjs';

const data = JSON.parse(fs.readFileSync(new URL('../demo/search-data.json', import.meta.url), 'utf8'));
const ids = (q, mode='all') => search(data,q,mode).results.map(h=>h.record.image_id).sort();
const scene = n => `tps-scene-${String(n).padStart(3,'0')}`;
for (const q of ['airport buses','機場巴士','Airport Express','机场巴士']) assert.deepEqual(ids(q),[1,2,11].map(scene).sort(),q);
for (const q of ['Taoyuan Airport MRT','AIRPORT-MRT','機場捷運','機捷','airport train']) assert.deepEqual(ids(q),[8,9,10].map(scene),q);
for (const q of ['Taipei Bus Station','臺北轉運站','台北轉運站','台北转运站']) assert.deepEqual(ids(q),[6,11].map(scene),q);
for (const q of ['airport buses','機場捷運','Taipei Bus Station','廁所','check-in','電梯']) assert.deepEqual(ids(q,'visible'),[],q);
assert.deepEqual(ids('lockers','visible'),[scene(6)]);
assert.deepEqual(ids('廁所','signs'),[3,4,6].map(scene));
assert.deepEqual(ids('stairs','visible'),[scene(5)]);
assert.deepEqual(ids('stairs','signs'),[3,10].map(scene));
assert.deepEqual(ids('interactive terminal'),[]);
assert.deepEqual(ids('nonexistentdestination'),[]);
assert.deepEqual(ids('none'),[]);
assert.equal(ids('').length,data.progress.scene_records);
assert.equal(search(data,'airport').llm_called,false);
assert.throws(()=>search(data,'','invalid'));
// Relative assets must stay beneath the GitHub project prefix.
const base = new URL('https://example.github.io/TaipeiSignRAG/demo/app.js');
assert.equal(new URL('./search-data.json',base).pathname,'/TaipeiSignRAG/demo/search-data.json');
assert.equal(new URL('../release/huggingface/scene_images/scene_011.png',base).pathname,'/TaipeiSignRAG/release/huggingface/scene_images/scene_011.png');
const cases = JSON.parse(fs.readFileSync(0,'utf8'));
for (const test of cases) {
  const actual=search(data,test.query,test.mode);
  assert.deepEqual(actual.results.map(h=>[h.record.image_id,h.ranking_score,h.matched_categories,h.matched_transport]),test.hits,`${test.query} / ${test.mode}`);
}
console.log(`Browser checks passed, including ${cases.length} Python/JavaScript parity cases.`);
