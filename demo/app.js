import {search} from './search.mjs';

const $ = selector => document.querySelector(selector);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const arrows = {up:'↑',left:'←',right:'→',up_right:'↗',up_left:'↖',down_right:'↘',down_left:'↙',u_turn:'↶ (return arrow)'};
const transportLabels = {
  airport_bus:'Airport buses / 機場巴士',
  taoyuan_airport_mrt:'Taoyuan Airport MRT / 桃園機場捷運',
  taipei_bus_station:'Taipei Bus Station / 臺北轉運站'
};
let dataset;
let resultLimit = 50;
$('#q').value = new URLSearchParams(location.search).get('q') || '';
function run(reset = true) {
  if (!dataset) return;
  if (reset) resultLimit = 50;
  const data = search(dataset, $('#q').value, $('#mode').value, resultLimit);
  $('#status').textContent = data.count ? `Showing ${data.count} of ${data.total_count} matching scene records / 顯示 ${data.count} 筆，共 ${data.total_count} 筆符合的照片紀錄` : 'No supported match in this POC. This does not establish absence from the station. / 本概念驗證未找到支持證據，不代表車站沒有該設施。';
  $('#more').hidden = data.count >= data.total_count;
  $('#results').innerHTML = data.results.map(({record:r,matched_categories:m,matched_transport:t}) => {
    const imageUrl = r.demo_image ? new URL('./' + r.demo_image, import.meta.url).href : r.evidence_image ? new URL('../release/huggingface/' + r.evidence_image, import.meta.url).href : null;
    const picture = imageUrl ? `<img src="${esc(imageUrl)}" loading="lazy" alt="${r.demo_image ? 'Supplemental demo photograph' : 'Masked source evidence'} for ${esc(r.image_id)}">` : '';
    return `<article data-publication="${r.supplemental_demo ? 'supplemental_demo' : imageUrl ? 'image' : 'annotations_only'}">${picture}<div class="body"><small>${esc(r.image_id)} · ${esc(r.filename_family)}</small><h2>${esc(r.display_name || (r.filename_family + ' scene'))}</h2>
    ${imageUrl ? '' : `<p><strong>Annotations only / 僅標註</strong></p><pre>${esc(r.source_archive)}\n${esc(r.source_image)}</pre>`}
    ${Object.entries(m).map(([c,s]) => `<span class="badge ${s==='sign_reference_only'?'sign':''}">${esc(c.replaceAll('_',' '))}: ${s==='visible'?'visible':'sign only'}</span>`).join('')}
    ${t.map(id => `<span class="badge sign">${esc(transportLabels[id])}: sign only</span>`).join('')}
    <p>${esc(r.summary_en)}</p><p lang="zh-Hant">${esc(r.summary_zh)}</p>
    <h3>Physically visible / 實際可見</h3><ul>${r.objects.map(o => `<li>${esc(o.label_en)} / ${esc(o.label_zh)} — ${esc(o.region)}</li>`).join('')}</ul>
    <h3>Sign references / 指標提及</h3><ul>${r.signs.map(s => `<li>${esc(s.visible_zh||s.label_en)} · ${esc(s.label_en)} ${esc(arrows[s.direction]||'— arrow association unverified')}${s.visible_en ? `<br>Printed English: ${esc(s.visible_en)}` : ''}${s.note ? `<br><small>${esc(s.note)}</small>` : ''}</li>`).join('')}</ul>
    <details><summary>Uncertainties and source / 不確定資訊與來源</summary><ul>${r.unknowns.map(u => `<li>${esc(u)}</li>`).join('')}${r.uncertain.map(u => `<li>${esc(u.description)}</li>`).join('')}</ul><p>${r.supplemental_demo ? esc(r.privacy_review) : imageUrl ? 'Masked regions are not assessable.' : 'Source photograph is referenced by dataset and filename; no image is included with this record.'} Coordinates and anchors: unknown. Expert review: pending. Arrows describe the photograph only.</p><pre>${esc(r.source_archive)}\n${esc(r.source_image)}\nSHA-256: ${esc(r.source_sha256)}</pre>${r.source_url ? '<a href=' + String.fromCharCode(34) + esc(r.source_url) + String.fromCharCode(34) + ' target=' + String.fromCharCode(34) + '_blank' + String.fromCharCode(34) + ' rel=' + String.fromCharCode(34) + 'noopener noreferrer' + String.fromCharCode(34) + '>Original dataset · CC BY 4.0</a>' : (r.supplemental_demo ? '<span>Supplemental demo image; outside the core TibaMe release.</span>' : '')}</details></div></article>`;
  }).join('');
  $('#context').textContent = JSON.stringify({instructions:data.llm_instructions,evidence:data.context_for_llm,llm_called:false},null,2);
}
$('#search').addEventListener('submit', event => {event.preventDefault();run();});
$('#more').addEventListener('click', () => {resultLimit += 50;run(false);});
$('#mode').addEventListener('change', run);
document.querySelectorAll('[data-q]').forEach(button => button.addEventListener('click', () => {$('#q').value=button.dataset.q;run();}));
try {
  const response = await fetch(new URL('./search-data.json', import.meta.url));
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  dataset = await response.json();
  if (!Array.isArray(dataset.records) || !dataset.config || !dataset.progress) throw new Error('Invalid evidence package');
  const p = dataset.progress;
  $('#coverage').textContent = `${p.scene_records} whole-photo records · ${p.unique_source_images_with_any_new_annotation} unique annotated source photos including the locker pilot · ${p.remaining_source_entries_without_new_annotation.toLocaleString()} source entries remaining · ${p.human_reviewed_records} human-reviewed records.`;
  run();
} catch (error) {
  $('#status').textContent = 'Evidence could not load. Serve this site over HTTP or GitHub Pages, then reload. / 無法載入資料，請透過 HTTP 或 GitHub Pages 開啟後重新整理。';
}
