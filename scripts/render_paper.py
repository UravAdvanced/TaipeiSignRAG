"""Render stable numbered citations by first appearance; abstract has no citations."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'paper'
source = (PAPER / 'manuscript.source.md').read_text(encoding='utf-8')
references = json.loads((PAPER / 'references.json').read_text(encoding='utf-8'))
by_key = {r['key']: r for r in references}
assert len(by_key) == len(references), 'Duplicate reference keys'
abstract = source.split('## Abstract', 1)[1].split('## 1.', 1)[0]
assert '{cite:' not in abstract and not re.search(r'\[\d+\]', abstract), 'Abstract must be citation-free'
order = []

def cite(match):
    key = match.group(1)
    if key not in by_key:
        raise ValueError(f'Unknown citation: {key}')
    if key not in order:
        order.append(key)
    return f'[{order.index(key) + 1}]'

body = re.sub(r'\{cite:([a-zA-Z0-9_]+)\}', cite, source)
lines = []
bib = []
for number, key in enumerate(order, 1):
    ref = by_key[key]
    authors = ref['author'].replace(' and ', ', ').replace('{', '').replace('}', '')
    venue = ref.get('journal', ref.get('howpublished', ''))
    if ref.get('volume'):
        venue += f", {ref['volume']}({ref.get('number', '')}): {ref.get('pages', '').replace('--', '–')}"
    extra = f" arXiv:{ref['eprint']}." if ref.get('eprint') else ''
    doi = f" DOI: {ref['doi']}." if ref.get('doi') else ''
    lines.append(f"[{number}] {authors}. **{ref['title']}**. {venue + '. ' if venue else ''}{ref.get('year', 'n.d.')}.{extra}{doi} {ref.get('note', '')} {ref['url']}")
    fields = ',\n'.join(f'  {k} = {{{v}}}' for k, v in ref.items() if k not in ('key', 'type'))
    bib.append(f"@{ref['type']}{{{key},\n{fields}\n}}")

(PAPER / 'draft.md').write_text(body + '\n\n## References\n\n' + '\n\n'.join(lines) + '\n', encoding='utf-8')
(PAPER / 'references.bib').write_text('\n\n'.join(bib) + '\n', encoding='utf-8')
(PAPER / 'citation_order.json').write_text(json.dumps({key: i+1 for i, key in enumerate(order)}, indent=2), encoding='utf-8')
seen = []
for number in map(int, re.findall(r'\[(\d+)\]', body)):
    if number not in seen:
        seen.append(number)
assert seen == list(range(1, len(order)+1)), 'Nonsequential first citations'
assert set(order) == set(by_key), 'Uncited reference(s)'
print(f'Rendered {len(order)} references in first-appearance order; repeat numbers preserved; abstract citation-free.')
