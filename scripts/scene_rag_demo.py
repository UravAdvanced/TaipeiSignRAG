"""Local evidence retrieval and LLM-context API. No remote inference or embeddings.

Run: python scripts/scene_rag_demo.py serve --port 8766
     python scripts/scene_rag_demo.py search '置物櫃' --mode visible
"""
import argparse
import json
import mimetypes
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'release/huggingface'
ALIASES={
 'lockers':['locker','lockers','luggage storage','置物櫃','寄物櫃','行李寄放'],
 'toilets':['toilet','toilets','restroom','restrooms','bathroom','廁所','洗手間'],
 'shopfront':['shop','shops','storefront','shopfront','商店','店名','商舖'],
 'fare_gates_or_turnstiles':['turnstile','turnstiles','fare gate','gates','驗票閘門','閘門','剪票口'],
 'elevator':['elevator','elevators','lift','lifts','電梯','升降機'],
 'stairs':['stairs','staircase','stairway','樓梯'],
 'escalator':['escalator','escalators','電扶梯','扶梯'],
 'train_platform_or_entrance':['platform','platforms','train entrance','月台'],
 'kiosk':['kiosk','kiosks','interactive terminal','互動式資訊機','資訊機'],
 'check_in_counter':['check-in','check in','checkin','報到','登機櫃檯','預辦登機'],
 'ticket_counter':['ticket counter','ticket office','售票處','售票櫃檯'],
 'service_counter':['service centre','service center','information counter','服務中心','服務櫃檯'],
 'map_information_board':['map','maps','map board','地圖','資訊看板'],
 'emergency_exit_sign':['emergency exit','逃生出口','緊急出口'],
}
STOP={'where','is','are','the','a','an','i','can','find','me','show','there','this','that','to','for','of','in','do','you','what','with','it','please'}

def records():
    return [json.loads(s) for s in (PACK/'scene_annotations.jsonl').read_text(encoding='utf-8').splitlines() if s]

def tokens(text):
    text=text.lower()
    result=set(w for w in re.findall(r'[a-z0-9]+',text) if w not in STOP)
    for run in re.findall(r'[\u3400-\u9fff]+',text):
        result.update(run[i:i+2] for i in range(len(run)-1))
        if len(run)==1:result.add(run)
    return result

def concepts(query):
    low=query.lower()
    def present(alias):
        return bool(re.search(r'(?<![a-z])'+re.escape(alias)+r'(?![a-z])',low)) if alias.isascii() else alias in low
    return [cat for cat,terms in ALIASES.items() if any(present(alias) for alias in terms)]

def search(query,mode='all',limit=8):
    if mode not in ('all','visible','signs'):raise ValueError('Unknown evidence mode')
    wanted=concepts(query);qt=tokens(query);results=[]
    for row in records():
        # Preserve the bus/MRT distinction even though both share "airport".
        if any(t in query.lower() for t in ('airport mrt','機場捷運','機捷')) and not any(s['label_en']=='Taoyuan Airport MRT' for s in row['signs']):
            continue
        coverage=row['amenity_coverage'];matched={c:coverage[c] for c in wanted if coverage.get(c) in ('visible','sign_reference_only')}
        allowed=('visible',) if mode=='visible' else ('sign_reference_only',) if mode=='signs' else ('visible','sign_reference_only')
        matched={c:s for c,s in matched.items() if s in allowed}
        if wanted and not matched:continue
        objects=row['objects'] if mode!='signs' else []
        signs=row['signs'] if mode!='visible' else []
        corpus=' '.join(str(v) for obj in objects+signs for k,v in obj.items() if k in ('label_en','label_zh','visible_zh','visible_en','visible_text_zh','visible_text_en','region'))
        hits=len(qt & tokens(corpus))
        if query.strip() and not wanted and not hits:continue
        score=sum(4 if s=='visible' else 2 for s in matched.values())+hits
        results.append({'record':row,'ranking_score':score,'matched_categories':matched})
    results.sort(key=lambda r:(-r['ranking_score'],r['record']['image_id']))
    results=results[:limit]
    context=[]
    for hit in results:
        r=hit['record'];context.append({'source_id':r['image_id'],'source_image':r['source_image'],
          'scene_description':r['summary_en'],'physical_objects':r['objects'],'sign_references':r['signs'],
          'uncertainties':r['unknowns'],'map_coordinate':None,'anchor_id':None,'human_review':r['human_review_status']})
    instructions=('Answer only from the supplied evidence and cite source_id. Distinguish physical objects visible in the photo from destinations mentioned on signs. '
      'Directions are arrows in a historical image, not live route commands. Do not infer current location, floor, availability, accessibility, opening hours, or map coordinates. '
      'If a facility is not observed, say it is not established by these pilot images; do not say it is absent from the station. '
      'Records are assistant-checked and human review is pending. No people may be described. If evidence is insufficient, say so.')
    return {'query':query,'mode':mode,'count':len(results),'requested_categories':wanted,
      'retrieval_method':'local lexical matching with bilingual amenity aliases; ranking scores are not probabilities',
      'results':results,'context_for_llm':context,'llm_instructions':instructions,
      'llm_called':False,'notice':'Pilot evidence retrieval only. No live generative model or spatial positioning is connected.'}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        u=urlsplit(self.path)
        if u.path=='/api/search':
            q=parse_qs(u.query)
            try:data=json.dumps(search(q.get('q',[''])[0],q.get('mode',['all'])[0]),ensure_ascii=False).encode('utf-8')
            except ValueError as exc:self.send_error(400,str(exc));return
            self.send_response(200);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
        if u.path=='/':p=ROOT/'demo/index.html'
        elif u.path.startswith('/scene_images/'):
            p=(PACK/unquote(u.path[1:])).resolve()
            if not p.is_relative_to((PACK/'scene_images').resolve()):self.send_error(403);return
        else:self.send_error(404);return
        if not p.is_file():self.send_error(404);return
        data=p.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(str(p))[0] or 'application/octet-stream');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def log_message(self,format,*args):pass

if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    serve=sub.add_parser('serve');serve.add_argument('--port',type=int,default=8766)
    find=sub.add_parser('search');find.add_argument('query');find.add_argument('--mode',choices=['all','visible','signs'],default='all')
    args=p.parse_args()
    if args.command=='search':print(json.dumps(search(args.query,args.mode),ensure_ascii=False,indent=2))
    else:
        httpd=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
        print(f'TaipeiSignRAG evidence demo: http://127.0.0.1:{args.port}',flush=True)
        httpd.serve_forever()
