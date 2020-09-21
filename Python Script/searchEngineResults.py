# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 03:47:42 2016

@author: antariksh
"""

from googlesearch import GoogleSearch
from py_bing_search import PyBingSearch
import urllib as UL
import urlparse as UP
import bs4

BS=bs4.BeautifulSoup

class SearchEngine:
    def __init__(self,query):
        self.query=query
        self.bing_api_key='HK3O/eleIl4kjb5vFKeFMWgMY+FwqZilO/8TZbzjOhA'
    def crawl(pageurl,soup):
        urls=[]
        url=pageurl
        urls=[url]
        visited = [urls[0]] # historic record of urls
        for tag in soup.findAll('a',href=True): 
            # finding anchor tag in html and there is link in href
            tag['href'] = UP.urljoin(url,tag['href']) # print data inside the href
            #print tag['href']
            if url in tag['href'] and tag['href'] not in visited:
                # add to the stack            
                urls.append(tag['href'])
                visited.append(tag['href'])
        print pageurl
        print "----------------------------------"
        print visited
        print"###################################"
    
    def googleSearch(self):
        #Query can be site specific-> site:link word
        google=GoogleSearch(self.query)
        ct=GoogleSearch(self.query).count()
        print "No. Of Google Results: %d"%(ct)
        results=google.top_urls()
        return results
    
    def bingSearch(self,numresult=10):
        bing=PyBingSearch(self.bing_api_key)
        results,next_uri=bing.search(self.query,limit=numresult,format='json')
        res=[]
        for i in range(numresult):
            res+=[results[i].url]
        return res
    
    def bingWikiSearch(self):
        query=self.query.split(" ")[0]+" :wiki"
        bing=PyBingSearch(self.bing_api_key)
        results,next_uri=bing.search(query,limit=1,format='json')
        return results[0].url
        

def search_engine(query): 
    query+=" :article"
    SE = SearchEngine(query)   
    googleResult = SE.googleSearch()
    bingResult = SE.bingSearch(5)
    #print "Gooogle:",googleResult
    #print "Bing:",bingResult
    urllist=[SE.bingWikiSearch()]   
    print googleResult
    for url in googleResult:
        urllist+=[url]
    for url in bingResult:
        if url not in urllist:
            urllist+=[url]
    return urllist
    
#query=raw_input("Search:")
#print search_engine(query)


"""
for url in googleResult:
	bs=getPageData(url,str(ct))
	ct+=1
	crawl(url,bs)
for url in bingResult:
	bs=getPageData(url,str(ct))
	ct+=1
	crawl(url,bs)
"""
