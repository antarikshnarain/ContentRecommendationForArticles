# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 01:18:41 2016

@author: antariksh
@Description: It gets the top links from the web and runs the summarizers.
"""
import threading
from searchEngineResults import *
from htmlSummarizer import *

class myThread (threading.Thread):
    def __init__(self, threadID, url,query):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.query=query
    def run(self):
        #print "Starting ",self.threadID
        getPageData(self.url,self.query)
        #print "Exiting ",self.threadID

def getData(url,query):
    try:
        pageScore,title,summary,links=runner(url,query)
        # Pages with pageScore<5 are Omited
        #print "PageScore:%d NLinks: %d Title: %s"%(pageScore,len(links),title)
        return pageScore,title,summary,links
    except:
        print "URL Error: ",url
    
    return 0,"","",0
    
        
def getPageData(url,query):
    pageScore,title,summary,links=getData(url,query)
    print '--WEB-SUMMARY-->',url
    print "Summary:",summary
    """
    if len(links)>5:        
        print "________________________CRAWLING________________________"
        text=""        
        for link in links:
            pageScore,title,summary,sub_links=getData(link,query)
            text+=summary+"\n"
        print "______START_________CRAWLED SUMMARY_______________________"
        if len(text)>40:
            for s in fs.summarize(text, 4):
                print '*',s
        print "_______END__________CRAWLED SUMMARY_______________________"
    """
        
def web_search(query):
	#query=raw_input("Search:")
	urls=search_engine(query)
	print len(urls),urls
	l=1
	for url in urls:
		thread = myThread(l,url,query)
		thread.start()
		#thread.join() # No need to join threads makes it slow
		l+=1
