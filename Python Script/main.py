# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 04:01:58 2016

@author: antariksh
"""

import nltk
import pickle
from summarizer import *
import operator
from search_web import *

fileloc='/home/antariksh/Python/Project/2000/Summarize/05/0205000m.txt'

def idfscore(word):
    try:
        return idf[word]
    except KeyError:
        #return default value of idf score		
        return idf['#max']

def local_FD(text):
    dic={}    
    FD=nltk.FreqDist(nltk.word_tokenize(text))
    for key in FD:
        dic[key]=1+log(FD[key])
    return dic

f=open('inverted_dic_summary.pck','r')
invInd=pickle.load(f)
f.close()
f=open('IDF.pck','r')
idf=pickle.load(f)
f.close()
f=open('TF.pck','r')
tf=pickle.load(f)
f.close()

part_of_speech=['NNP']
text=open(fileloc).read()#raw_input('Enter Text: ')
print "INPUT FILE"
print text
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
local_tf=local_FD(text) # dictionary
sent=nltk.sent_tokenize(text)
sents=[nltk.word_tokenize(s) for s in sent]
postags=[nltk.pos_tag(s) for s in sents]
summ=[]
keywords=[]
for sent in postags:
    for w in sent:    
        wrd,tag=w
        if tag in part_of_speech and idfscore(wrd):
            if wrd not in keywords:            
                keywords.append(wrd)

priority={}
missingword=[]
for word in keywords:
    try:
        for File in invInd[word]:
            try:            
                priority[File]+=local_tf[word]*idfscore(word)*tf[File][word]
            except KeyError:
                priority[File]=local_tf[word]*idfscore(word)*tf[File][word]
    except KeyError:
        missingword.append(word)

sorted_priority = sorted(priority.items(), key=operator.itemgetter(1),reverse=True)
print sorted_priority[0:3]
print priority[fileloc]
print keywords
for File in sorted_priority[:min(3,len(sorted_priority))]:    
    f=open(File[0])
    print f.read()
    f.close()
    print "-----------------***F***-------------------------------"

query=""
for wrd in missingword:
    query+=wrd+" "
print "----Crawling Web NOW----",query
if len(missingword)>0:
    web_search(query)