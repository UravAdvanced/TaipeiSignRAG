"""Cache public destination searches/pages; never convert web facts into photo labels."""
import concurrent.futures
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote
import xml.etree.ElementTree as ET
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/sign_catalog'
OUT.mkdir(parents=True,exist_ok=True)
def clean(value):
    value=re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',value,flags=re.S|re.I)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',value))).strip()
def fetch(query):
    url=query if query.startswith('https://') else 'https://www.bing.com/search?q='+quote(query)+'&format=rss'
    try:
        response=requests.get(url,timeout=25,headers={'User-Agent':'Mozilla/5.0'})
        try: response.content.decode('utf-8');response.encoding='utf-8'
        except UnicodeDecodeError: response.encoding=response.apparent_encoding
        if '<rss' in response.text[:500]:
            root=ET.fromstring(response.content)
            items=[{'title':i.findtext('title'),'url':i.findtext('link'),'description':i.findtext('description')} for i in root.findall('.//item')]
            return {'query':query,'url':response.url,'status':response.status_code,'retrieved_at':datetime.now(timezone.utc).isoformat(),'text':'\n'.join(str(i) for i in items),'links':[i['url'] for i in items],'search_results':items}
        items=re.findall(r'<li class="b_algo".*?</li>',response.text,flags=re.S)
        text='\n'.join(clean(item) for item in items) if items else clean(response.text)
        links=[html.unescape(x) for x in re.findall(r'(?:href|src)=[\"\']([^\"\']+)',response.text) if not x.startswith('data:') and len(x)<1000]
        links=[unquote(x.split('/url?q=',1)[1].split('&',1)[0]) if '/url?q=' in x else x for x in links]
        anchors=[{'url':html.unescape(m.group(1)),'label':clean(m.group(2))} for m in re.finditer(r'<a\b[^>]*href=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)</a>',response.text,flags=re.S|re.I)]
        return {'query':query,'url':response.url,'status':response.status_code,'retrieved_at':datetime.now(timezone.utc).isoformat(),'text':text,'links':links,'anchors':anchors}
    except Exception as exc:return {'query':query,'error':str(exc)}
if __name__=='__main__':
    name=sys.argv[1]
    if '--cached' in sys.argv:
        results=json.loads((OUT/(name+'_sources.json')).read_text(encoding='utf-8'))
    else:
        queries=json.loads((OUT/(name+'_queries.json')).read_text(encoding='utf-8'))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(fetch,queries))
        (OUT/(name+'_sources.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    for r in results:
        snippets=[r['text'][max(0,m.start()-100):m.end()+250] for m in re.finditer(r'Cosmos|天成|凱撒|地下街|Taipei Main|台北車站|台北站前|台北車站|市民大道|中山北路|承德路|忠孝西路',r.get('text',''),flags=re.I)]
        relevant_anchors=[a for a in r.get('anchors',[]) if re.search(r'mall|交通|地下街|台北站前|臺北車站|taipei main|cosmos',a['label'],flags=re.I)]
        print(json.dumps({**{k:v for k,v in r.items() if k not in ('text','links','search_results','anchors')},'text':r.get('text','')[:1200],'relevant_snippets':snippets[:3],'relevant_links':relevant_anchors[:20]},ensure_ascii=False))
