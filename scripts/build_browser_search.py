"""Export the curated records and shared lexical rules for static browser search."""
import json
from scene_rag_demo import ROOT, ALIASES, TRANSPORT_ALIASES, DESTINATION_ALIASES, STOP, INSTRUCTIONS, records

payload = {
    'schema_version':'0.1.0',
    'records':records(),
    'progress':json.loads((ROOT/'annotations/progress.json').read_text(encoding='utf-8')),
    'config':{'aliases':ALIASES,'transport_aliases':TRANSPORT_ALIASES,'destination_aliases':DESTINATION_ALIASES,'stop_words':sorted(STOP)},
    'llm_instructions':INSTRUCTIONS,
}
(ROOT/'demo/search-data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Exported {len(payload['records'])} scene records for browser-side bilingual search.")
