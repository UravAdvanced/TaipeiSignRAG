// Pure retrieval shared by the browser UI and Node functional checks.
export function normalize(text) {
  return text.normalize('NFKC').toLowerCase().replaceAll('臺', '台').replace(/[\s-]+/g, ' ').trim();
}
function concepts(query, aliases) {
  const low = normalize(query);
  return Object.entries(aliases).filter(([, terms]) => terms.some(term => {
    const alias = normalize(term);
    if (/[^\x00-\x7F]/.test(alias)) return low.includes(alias);
    const escaped = alias.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return new RegExp('(?<![a-z])' + escaped + '(?![a-z])').test(low);
  })).map(([category]) => category);
}
function tokens(text, stop) {
  const low = normalize(text);
  const result = new Set((low.match(/[a-z0-9]+/g) || []).filter(word => !stop.has(word)));
  for (const run of low.match(/[\u3400-\u9fff]+/g) || []) {
    if (run.length === 1) result.add(run);
    for (let i = 0; i < run.length - 1; i++) result.add(run.slice(i, i + 2));
  }
  return result;
}
export function search(data, query, mode = 'all', limit = 50) {
  if (!['all', 'visible', 'signs'].includes(mode)) throw new Error('Unknown evidence mode');
  const wanted = concepts(query, data.config.aliases);
  const transport = concepts(query, data.config.transport_aliases);
  const stop = new Set(data.config.stop_words), qt = tokens(query, stop);
  const allowed = mode === 'visible' ? ['visible'] : mode === 'signs' ? ['sign_reference_only'] : ['visible', 'sign_reference_only'];
  const fields = new Set(['label_en','label_zh','visible_zh','visible_en','visible_text_zh','visible_text_en','region']);
  const results = [];
  for (const row of data.records) {
    const matchedTransport = mode === 'visible' ? [] : [...new Set(row.signs.map(s => s.transport_id).filter(id => transport.includes(id)))].sort();
    if (transport.length && !matchedTransport.length) continue;
    const matched = Object.fromEntries(wanted.filter(c => allowed.includes(row.amenity_coverage[c])).map(c => [c, row.amenity_coverage[c]]));
    if (wanted.length && !Object.keys(matched).length) continue;
    const objects = mode === 'signs' ? [] : row.objects;
    const signs = mode === 'visible' ? [] : row.signs;
    const corpus = [...objects, ...signs].flatMap(obj => Object.entries(obj).filter(([k]) => fields.has(k)).map(([,v]) => v ?? '')).join(' ');
    const ct = tokens(corpus, stop), hits = [...qt].filter(t => ct.has(t)).length;
    if (query.trim() && !wanted.length && !transport.length && !hits) continue;
    const score = Object.values(matched).reduce((sum, s) => sum + (s === 'visible' ? 4 : 2), 0) + hits + 6 * matchedTransport.length;
    results.push({record:row, ranking_score:score, matched_categories:matched, matched_transport:matchedTransport});
  }
  results.sort((a,b) => b.ranking_score - a.ranking_score || a.record.image_id.localeCompare(b.record.image_id));
  const selected = results.slice(0, limit);
  return {
    query, mode, count:selected.length, requested_categories:wanted, requested_transport:transport,
    retrieval_method:'browser-side lexical matching with bilingual aliases; ranking scores are not probabilities',
    results:selected,
    context_for_llm:selected.map(({record:r}) => ({source_id:r.image_id, source_image:r.source_image,
      scene_description:r.summary_en, physical_objects:r.objects, sign_references:r.signs,
      uncertainties:r.unknowns, map_coordinate:null, anchor_id:null, human_review:r.human_review_status})),
    llm_instructions:data.llm_instructions, llm_called:false,
    notice:'POC evidence retrieval only. No live generative model or spatial positioning is connected.'
  };
}
