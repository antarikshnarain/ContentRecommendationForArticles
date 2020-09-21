from __future__ import division
import nltk
import math
from math import log
import pickle
"""
idf={}
f=open('IDF.txt')
text=f.read()
f.close()
text=text.split(' ')
for w in text:
	if w!='':
		t=w.split('/!@#$')
		idf[t[0]]=float(t[1])
"""
f=open('IDF.pck','r')
idf=pickle.load(f)
f.close()

def idfscore(word):
    try:
        return idf[word]
    except KeyError:
        #return default value of idf score		
        return idf['#max']

def summarize(t):
    tf={}
    indexedscore=[]
    t=t.encode('punycode')
    t=nltk.sent_tokenize(t)
    t=[nltk.word_tokenize(sent) for sent in t]
    for sent in t:
        for word in sent:
            try:
                tf[word]+=1
            except KeyError:
                tf[word]=1
    for word in tf:
        tf[word]=1+log(tf[word])
    for si in range(len(t)):
        tsum=0		
        for word in t[si]:
            tsum+=tf[word]*idfscore(word)
        indexedscore.append((si,tsum))
    indexedscore.sort(key=lambda l:l[1],reverse=True)
	#important - below line determines number of lines of summary
    si=indexedscore[:int(min(6,len(t)/3))]
    si.sort(key=lambda l:l[0])
    summ=[]
    for (i,s) in si:
        summ.append(' '.join(t[i]))
    return summ
	
