# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 21:33:19 2016

@author: antariksh
"""

import re
import os
import sys
import urlparse as UP
import urllib as UL
import bs4
import threading
from goose import Goose

BS = bs4.BeautifulSoup
directory='/home/antariksh/Python/Project/Dataset/'
visited=[]
g=Goose()
e=threading.Event()
threadcount=[] # for Controlling the Thread Limit


def gooseHTMLParser(url):
    article=g.extract(url=url)
    #article.title
    #article.meta_description
    #article.top_image.src
    text=str(article.cleaned_text.encode("UTF-8").decode("unicode_escape").encode('ascii','ignore'))
    return str(article.title),text

def processPage(url):
    try:
        htmltext = UL.urlopen(url).read()
    except:
        print "Error Page: ",urls[0]
    soup = BS(htmltext)
    links=[]
    for tag in soup.findAll('a',href=True): 
        # finding anchor tag in html and there is link in href
        tag['href'] = UP.urljoin(url,tag['href']) # print data inside the href
        #print tag['href']
        if url in tag['href']:
            # add to the stack            
            links.append(tag['href'])
    title,text=gooseHTMLParser(url)
    return title,text,links

class myThread (threading.Thread):
    def __init__(self, threadID,url):
        threading.Thread.__init__(self)
        self.threadID=threadID        
        self.url=url
    def run(self):
        print "Starting " + str(self.threadID),self.url
        title,text,links=processPage(self.url)
        while e.isSet():
            m=1            
        e.set()
        for link in links:        
            urls.append(link)
            
        threadcount.pop(0)
        if len(text)>200:
            myfile=open(directory+title+".txt",'wb')
            myfile.write(text)
            myfile.close()
        e.clear()        
        print "Exiting " + str(self.threadID),self.url,len(links)
        
durl='http://www.thehindu.com/archive/print/2016/01/01/'
urls=[durl]
ctr=0
breakct=0
while ctr<1000:
    print "CTR=",ctr
    breakct+=1    
    while len(urls)==0:
        m=1
    myurl=urls.pop(0)
    #if myurl.rfind("#")>0:
    #    continue
    if myurl not in visited:    
        thread = myThread(ctr,myurl)
        ctr+=1
        while len(threadcount)==min(20,len(urls)+1):
            m=1
        threadcount.append(1)    
        thread.start();
        visited.append(myurl)

print "-----------------------------DONE---------------------------------"
#print visited
