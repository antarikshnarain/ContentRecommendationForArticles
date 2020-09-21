# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 04:03:56 2016

@author: antariksh
"""
from directory_crawler import *
import pickle
import nltk

files=directoryCrawl('/home/antariksh/Python/Project/2000/Summarize/')
iDic={} # inverted index dictionary
f=open('IDF.pck','r')
idf=pickle.load(f)
f.close()

def idfscore(word):
    try:
        return idf[word]
    except KeyError:
        #return default value of idf score		
        return idf['#max']
        
def correctFileData():    
    for File in files:
        print File
        f1=open(File,'rU')
        text=f1.read()
        f1.close()    
        text=text.replace(' .','.')
        f1=open(File,'wb')
        f1.write(text)
        f1.close()

for File in files:
    f=open(File,'rU')
    print File
    text=f.readline()
    text=f.read()
    f.close()
    sent=nltk.sent_tokenize(text)
    sentences=[nltk.word_tokenize(s) for s in sent]
    for sentence in sentences:    
        for token in sentence:
            x,y=nltk.pos_tag([token])[0]
            if idfscore(token)>6 or y=='NNP':
                if iDic.has_key(token):
                    if File not in iDic[token]:
                        iDic[token].append(File)
                else:
                    iDic[token]=[]
                    iDic[token].append(File)

f=open('inverted_dic_summary.pck','w')
pickle.dump(iDic,f)
f.close()
                
    