from __future__ import division
import nltk
import math
from math import log
import pickle
from directory_crawler import *

#filelist contains all txt file names to find idf for
#doclist contains all tokenized files
filelist=directoryCrawl()
doclist=[]
ct=1
for File in filelist:
	f=open(File)
	print ct,
	text=f.read()
	text=text.encode('punycode')
	doclist.append(nltk.word_tokenize(text))
	f.close()
	ct+=1

vocabulary={}

for doc in doclist:
	v={}
	for word in doc:
		try:
			v[word]+=1
		except KeyError:
			v[word]=1
			try:
				vocabulary[word]+=1
			except KeyError:
				vocabulary[word]=1

print "Creating IDF File"
idf={}
N=len(doclist)
f=open('IDF.txt','w')
idf['#max']=log(N)
f.write('#max/!@#$'+("%.9f"%(idf['#max']))+' ')
for word in vocabulary:
	idf[word]=log(N/(vocabulary[word]))
	#add 1 if number of documents is less, remove otherwise
	f.write(word+'/!@#$'+("%.9f"%(idf[word]))+' ')
f.close()

f=open('IDF.pck','w')
pickle.dump(idf,f)
f.close()
#to retrieve IDF use the following
'''
idfret={}
f=open('IDF.txt')
text=f.read()
text=text.split(' ')
for w in text:
	if w!='':
		t=w.split('/')
		idfret[t[0]]=float(t[1])
def idfscore(word):
	try:
		return idfret[word]
	except KeyError:
		#return default value of idf score		
		return idf['#max']
		
'''




	 
