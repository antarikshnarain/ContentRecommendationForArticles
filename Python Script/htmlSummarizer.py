# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 05:04:44 2016

@author: antariksh
"""

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import urllib2
import BeautifulSoup
from goose import Goose
import re


class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
         Initilize the text summarizer.
         Words that have a frequency term lower than min_cut 
         or higer than max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut 
        self._stopwords = set(stopwords.words('english') + list(punctuation))
    
    def _compute_frequencies(self, word_sent):
        """ 
          Compute the frequency of each of word.
          Input: 
           word_sent, a list of sentences already tokenized.
          Output: 
           freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        # frequencies normalization and fitering
        m = float(max(freq.values()))
        for w in freq.keys():
            freq[w] = freq[w]/m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]
        return freq
    
    def summarize(self, text, n):
        """
          Return a list of n sentences 
          which represent the summary of text.
        """
        sents = sent_tokenize(text)
        assert n <= len(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i,sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
                sents_idx = self._rank(ranking, n)    
        return [sents[j] for j in sents_idx]
    
    def _rank(self, ranking, n):
        """ return the first n sentences with highest ranking """
        return nlargest(n, ranking, key=ranking.get)

class gooseHtmlParser:
    def __init__(self,url,query):
        self.page_url=url
        self.query=query
    def get_page_data(self):
        url=self.page_url        
        g=Goose()
        article=g.extract(url=url)
        #article.title
        #article.meta_description
        #article.top_image.src
        links=[]        
        for link in article.links:
            if(re.match("http.*",link)!=None):
                links+=[link]
        text=str(article.cleaned_text.encode("UTF-8").decode("unicode_escape").encode('ascii','ignore'))
        pageScore=len(re.findall(self.query,text,re.IGNORECASE))
        return pageScore,str(article.title),text,links
    
    def numlines(self,title):
        if title.rfind('Wikipedia, the free encyclopedia')>=0:
            return 4
        else:
            return 2
            
    def getResult(self):
        url=self.page_url
        fs = FrequencySummarizer()
        pageScore,title, text, links = self.get_page_data()
        #print title
        ct=self.numlines(title)
        #print "CT:",ct
        summary=""
        if(len(text)>40 and pageScore>=2):
            for s in fs.summarize(text, ct):
                #print '*',s
                summary+='*'+s+"\n"
        return pageScore,title,summary,links
        
        
def runner(url,query):
	gooseParser=gooseHtmlParser(url,query)
	pageScore,title,summary,links=gooseParser.getResult()
	return pageScore,title,summary,links
