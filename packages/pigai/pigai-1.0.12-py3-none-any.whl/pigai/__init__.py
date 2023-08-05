# pigai, 20-9-18
from ipywidgets import widgets,interact, interactive, fixed, interact_manual,Button, Layout,Dropdown,RadioButtons
from IPython.display import display, clear_output
from IPython.core.display import HTML,display
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy,json,re,os, platform,builtins,requests
import pygtrie, random, json,redis
from functools import reduce,partial
from urllib.parse import quote
from collections import Counter,defaultdict

nlp			= spacy.load('en_core_web_sm')
merge_nps	= nlp.create_pipe("merge_noun_chunks")
postag		= lambda snt: pd.DataFrame([ (t.text, t.tag_) for t in nlp(snt)], columns=['word','pos'])
tokenize	= lambda snt: " ".join([t.text for t in nlp(snt) if len(t.text.strip())]).strip()

from elasticsearch import Elasticsearch
es	= Elasticsearch(['es.werror.com']) 
#rtest	= redis.Redis(host='dev.werror.com', port=9221,  db=0, decode_responses=True) # docker, for user testing , volatile
r	= redis.Redis(host='dev.werror.com', port=8008,  db=0, decode_responses=True) 
zsum	= lambda k='sino:verbs_noun:knowledge': sum( [ v for k,v in r.zrevrange(k,0,-1, True)] )
def norm(items):
	s = sum([v for k,v in items])
	return [ (k,round(100 * v/s,2)) for k,v in items] if s > 0 else items

def collocate(rel='verbs_noun', w='knowledge',corpus='sino', perc=False, vs=None, topk=10): 
	arr = [ (k, int(v)) for k,v in r.zrevrange(f'{corpus}:{rel}:{w}',0,-1,True)]
	if vs: 
		refer = dict(norm(r.zrevrange(f'{vs}:{rel}:{w}',0,-1,True)))
		return pd.DataFrame([ (k,v, refer.get(k, 0) )  for k,v in norm(arr)[0:topk] ], columns=['word',corpus, vs])
	return pd.DataFrame(norm(arr)[0:topk], columns=['word','prob(%)']) if perc else pd.DataFrame(arr[0:topk], columns=['word','freq'])

verbs_noun = partial(collocate,'verbs_noun')
verb_nouns = partial(collocate,'verb_nouns')
adjs_noun = partial(collocate,'adjs_noun')
adj_nouns = partial(collocate,'adj_nouns')
advs_verb = partial(collocate,'advs_verb')
adv_verbs = partial(collocate,'adv_verbs')
advs_adj = partial(collocate,'advs_adj')
adv_adjs = partial(collocate,'adv_adjs')
#print ( adj_nouns('pretty', vs='juk'))

toarr = lambda spair :  [ pair.split(":") for pair in spair.split(",")] #konwledge:30.09,knowlege:14.46,knoeledge:5.67,kownledge:5.43
tosf  = lambda spair :  [ (w, float(p)) for w,p in [ pair.split(":") for pair in spair.split(",")]]
tostr = lambda arr : ",".join([ f"{w}:{p}" for w,p in arr])

rdic = redis.Redis(host='dev.werror.com', port=8008, db=3, decode_responses=True)
def ecdic(pattern='con*ate', wlen=0,limit=10):
	words = [k for k in rdic.keys(pattern) if wlen <= 0 or len(k) == wlen][0:limit]
	return [(w,t) for w, t in zip(words, rdic.mget(words))]

def triples(corpus:str='dic', rel:str='dobj', w:str='open', start:int=0, end:int=10): # zrevrange gzjc:dobj_open_~ 0 10
	cnt = r.get(f"{corpus}:{rel}_{w}_~")
	return r.zrevrange(f"{corpus}:{rel}_{w}_~", start, end, withscores = True)

def get(corpus:str='gzjc', word:str='book'):
	return es.get('vocab','gzjc:book:lex')['_source'] # '_source': {'mf': 94, 'arr': 'book:55.32,books:43.62,booked:1.06'}}

def corpus_snt(word, corpus='dic'):
	d={
  "query": { 
    "bool": { 
      "must": [
        { "match": { "snt": word }}
      ],
      "filter": [ 
        { "term":  { "src": corpus }}
      ]
    }
  }
 }
	return es.search(body=d, index='sentbase')
#print(corpus_snt("love"))

api_url = "http://rest.wrask.com"	
rows		= lambda sql, corpus='dic', columns=[]: requests.get(f"{api_url}/kpfts/query/{corpus}", params={'sql':sql}).json() if not columns else pd.DataFrame(rows(sql, corpus, columns=[]), columns=columns)
mapk		= lambda sql, corpus='dic', columns=[]: {row[0]:row for row in requests.get(f"{api_url}/kpfts/query/{corpus}", params={'sql':sql}).json()}
select		= lambda sql, corpus='dic', columns=['kp','mf','arr']:  pd.DataFrame(rows(sql, corpus), columns=columns)
kwic		= lambda kw, corpus='dic', start=0, end=10:requests.get(f"{api_url}/kpfts/kwic/{corpus}", params={'kw':kw, 'start':start, 'end':end}).json() #http://dev.werror.com:7090/kwic/dic?kw=considering
getmf		= lambda kp, corpus='dic': requests.get(f"{api_url}/kpfts/mf", params={'kps':kp,'corpus':corpus}).json().get(corpus, {}).get(kp, 0.0)
getmfs		= lambda kps, corpus='dic': pd.read_json(f"{api_url}/kpfts/mf?kps={quote(kps)}&corpus={corpus}")
getsnt		= lambda kps, corpus='dic': requests.get(f"{api_url}/kpfts/snt/{corpus}", params={'kps':kps}).json() 
trpstar	= lambda kp, corpus='dic',start=0,end=10: pd.read_json(f"{api_url}/kpfts/trpstar/{corpus}?kp={quote(kp)}&start={start}&end={end}").set_axis(['word','prob','sent'], axis='columns', inplace=False) #dobj_open_%
getarr		= lambda kp, corpus='dic', start=0, end= 10, vs='', columns=['word','prob']: pd.read_json(f"{api_url}/kpfts/arr/{corpus}?kp={quote(kp)}&start={start}&end={end}&vs={vs}&columns={','.join(columns)}")
	
def subset(kp, cp1='gaokao', cp2='clec',columns=['#','word','num']):
	dct = { row['word']:row['prob'] for index, row in getarr(kp,cp2,end=0).iterrows()}
	df = pd.DataFrame([ (index,row['word'],row['prob']) for index, row in getarr(kp,cp1,end=0).iterrows() if not row['word'] in dct], columns=columns)
	return df.set_index(columns[0])
#print(subset('open */von'))

def parse(snt, merge_np= False):
	doc = nlp(snt)
	if merge_np : merge_nps(doc)
	return pd.DataFrame({'word': [t.text for t in doc], 'tag': [t.tag_ for t in doc],'pos': [t.pos_ for t in doc],'head': [t.head.orth_ for t in doc],'dep': [t.dep_ for t in doc], 'lemma': [t.text.lower() if t.lemma_ == '-PRON-' else t.lemma_ for t in doc],
	'lefts': [ list(t.lefts) for t in doc], 'n_lefts': [ t.n_lefts for t in doc], 'left_edge': [ t.left_edge for t in doc], 'rights': [ list(t.rights) for t in doc], 'n_rights': [ t.n_rights for t in doc], 'right_edge': [ t.right_edge for t in doc],
	'subtree': [ list(t.subtree) for t in doc],'children': [ list(t.children) for t in doc],})

def highlight(snt, merge_np= False,  colors={'ROOT':'red', 'VERB':'orange','ADJ':'green'}, font_size=0):
	doc = nlp(snt)
	if merge_np : merge_nps(doc)
	arr = [ f"<span pos='{t.tag_}'>{t.text.replace(' ','_')}</span>" for t in doc]
	for i, t in enumerate(doc): 
		if t.dep_ == 'ROOT': arr[i] = f"<b><font color='red'>{arr[i]}</font></b>"
		if t.pos_ in colors: arr[i] = f"<font color='{colors[t.pos_]}'>{arr[i]}</font>"
	html =  " ".join(arr) 
	return HTML(html if font_size <=0 else f"<div style='font-size:{font_size}px'>{html}</div>")

spellerr	= lambda w, topk=10: pd.DataFrame(tosf(r.hget('spellerr', w))[0:topk], columns=['word','prob'])
parasent	= lambda snt, topk=10,nprobe=10,corpus='dic': pd.DataFrame(requests.get(f'{api_url}/sntvec/search/{corpus}', params={'snt':snt, 'topk':topk,'nprobe':nprobe}).json(), columns=['sid','snt','semdis'])
cola		= lambda snt: pd.DataFrame(requests.get(f'{api_url}/cola/{snt}').json(), columns=['word','prob']) #http://cluesay.com:7095/cola/I%20love%20you%7CI%20live%20you |[["I love you",0.973],["I live you",0.2679]]
nextword	= lambda snt, topk=10: requests.get(f'{api_url}/auto/nextword', params={'snt': snt, 'topk':int(topk)}).json()
autowrite	= lambda snt, maxlen=30: requests.get(f'{api_url}/auto/autowrite', params={'snt': snt, 'maxlen':maxlen}).text
paraphrase	= lambda snt0, snt1: requests.get(f'{api_url}/auto/paraphrase', params={'snt0': snt0, 'snt1': snt1}).json()
nsp			= lambda snt0, snt1: requests.get(f'{api_url}/auto/nsp', params={'snt0': snt0, 'snt1': snt1}).json()
flue		= lambda snt, midx=0: requests.get(f'{api_url}/kenlm/flue/{snt}',params={'midx':midx}).json() #http://cluesay.com:7098/flue/I%20love%20you%7CI%20like%20you?midx=0
ppl		= lambda snt, midx=0: requests.get(f'{api_url}/kenlm/ppl/{snt}',params={'midx':midx}).json()
flueadd	= lambda snt, widx, word, midx=0: requests.get(f'{api_url}/kenlm/flueadd/{snt}/widx/word',params={'midx':midx}).json()
fluerep	= lambda snt, widx, word, midx=0: requests.get(f'{api_url}/kenlm/fluerep/{snt}/widx/word',params={'midx':midx}).json()
fluedel	= lambda snt, widx, midx=0: requests.get(f'{api_url}/kenlm/fluedel/{snt}/widx',params={'midx':midx}).json()
cloze		= lambda snt, topk=10: pd.DataFrame(requests.get(f'{api_url}/mask/cloze', params={'snt':snt, 'topk':topk}).json(), columns=['word','prob'])
addone		= lambda snt, index=0, topk=10: pd.DataFrame(requests.get(f'{api_url}/mask/addone', params={'snt':snt, 'index':index, 'topk':topk}).json(), columns=['word','prob'])
repone		= lambda snt, index=0, topk=10: pd.DataFrame(requests.get(f'{api_url}/mask/repone', params={'snt':snt, 'index':index, 'topk':topk}).json(), columns=['word','prob'])
nldp		= lambda snt : requests.get(f'{api_url}/nldpkp/', params={'q': snt, 'trpx': 0,'trp':0, 'ske':0}).json()
def restate(snt='John opened the window.', tense=0, option=[False, False, True, False, False, False]): # 0:unchanged 1:pres 2:past 3:futr | 0..5:  
	try:
		query = f"q={snt.replace(' ','+')}&tenseOpt={tense}" + "".join([ f"&Options%24{i}=on" for i,opt in enumerate(option) if opt])  #html.escape("hello world")
		res = requests.post(f'{api_url}/nldprestate/', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=f'__VIEWSTATE=%2FwEPDwUKLTcwMTczNTk3NmQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgcFCU9wdGlvbnMkMAUJT3B0aW9ucyQxBQlPcHRpb25zJDIFCU9wdGlvbnMkMwUJT3B0aW9ucyQ0BQlPcHRpb25zJDUFCU9wdGlvbnMkNVB%2F2Xl4E6Vc7Gl%2FWXYSYKbZ3OO4&{query}&Button1=%E5%8F%A5%E5%BC%8F%E6%94%B9%E5%86%99&__EVENTVALIDATION=%2FwEWDgLIgLeyBwLP76ruDAKM54rGBgLHr9K5CQLYr9K5CQLZr9K5CQLar9K5CQLXwPjXBQLx9MPdAQLw9MPdAQLv9MPdAQLu9MPdAQLt9MPdAQLs9MPdARuWtZztNkJEFeswt2Z1Y6i4m27E').text
		start = res.index('<span id="Label2"><font size="7">') + len('<span id="Label2"><font size="7">')
		end = res.index('</font></span>', start ) #<span id="Label2"><font size="7">The door was opened by Tom.</font></span>
		return res[start:end]
	except Exception as e:
		print("restate ex:", e, snt)
		return f"failed: {snt} tense={tense} option={option}" + e
#print(restate())

random_one	= lambda arr: arr[ int( len(arr) * random.random() )]
random_word	= lambda c: random_one([w for w, in requests.get(f"{api_url}/kpfts/query/wordlist", params={'sql':f"select kp from vocab where kp like '{c}%' limit 1000"}).json()])
nextword_if	= lambda snt_prefix, c , topk= 100: [ row for row in nextword(snt_prefix, topk= topk) if c in row[0] and row[0].isalpha() and len(row[0]) > 1]

def word_to_sent( word, topk = 300  ) :   #sentord, wordence
	snt = random_word(word[0])
	for i in range(1, len(word)):
		cands = nextword_if(snt, word[i], topk)
		if len(cands) > 0 : 
			snt = snt + " " + cands[0][0]
		else:
			return f"Failed: {snt} , i = {i} | {word}"
	return snt
#print(word_to_sent("family"))

def subwords(w = 'knowledge', minlen=1, editdis=0):
	if not hasattr(subwords, 'trie'):
		setattr(subwords, 'trie', pygtrie.CharTrie()) #subwords.trie = pygtrie.CharTrie()
		for w in r.hkeys('wordlist'): subwords.trie[w] = len(w)
	res =[]
	for i in range(len(w)): res.extend(subwords.trie.prefixes(w[i:]))
	res.sort(key =lambda ar: ar[1], reverse=True)
	return list(filter(lambda pair: pair[1] > minlen, res))
#print(subwords())

def sent_to_word(snt):
	cands = list({w for w in reduce(lambda x,y:[ i+j for i in x for j in y], [ [a for a in word] for word in snt.lower().split(" ")])})
	return [cand for cand, hit in zip(cands, r.hmget('wordlist', cands )) if not hit is None]
#print(sent_to_word("father and mother i love you"))

def learn(essay = "The quick fox jumped over the lazy dog. I have learned a lot of knowledges."): 
	doc = nlp(essay)
	wc = Counter([t.text.lower() for t in doc if not t.pos_ in ('PUNCT') and not t.is_stop])  #doc.count_by(LOWER) #nlp.vocab[8566208034543834098].text
	return [(w, r.zscore('wordidf', w), c) for w, c in wc.items()]

from math import log as ln
def likelihood(a,b,c,d):  #from: http://ucrel.lancs.ac.uk/llwizard.html
	try:
		E1 = c * (a + b) / (c + d)
		E2 = d * (a + b) / (c + d)
		G2 = 2 * ((a * ln(a / E1)) + (b * ln(b / E2)))
		return G2
	except Exception as e:
		print(e)
		return 0 
#likelihood(316 :inau-lexcnt, 4534:bnc-lexcnt, 149630.0 :inau-lexsum, 90350013 :bnc-lexsum) #nation
'''
The higher the G2 value, the more significant is the difference between two frequency scores. For these tables, a G2 of 3.8 or higher is significant at the level of p < 0.05 and a G2 of 6.6 or higher is significant at p < 0.01.

95th percentile; 5% level; p < 0.05; critical value = 3.84
99th percentile; 1% level; p < 0.01; critical value = 6.63
99.9th percentile; 0.1% level; p < 0.001; critical value = 10.83
99.99th percentile; 0.01% level; p < 0.0001; critical value = 15.13
'''

if __name__ == '__main__': 
	#print(trpstar("dobj_open_%").set_axis(['word','prob','sent'], axis='columns', inplace=False) )
	#print(getarr('book/pos'))
	#print(word_to_sent('family'))
	#print(nextword_if("we love", 'y'))
	print ( zsum())