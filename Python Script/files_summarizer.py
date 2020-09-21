# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 23:44:07 2016

@author: antariksh
"""

from directory_crawler import *
from summarizer import *

filelist=directoryCrawl()
for File in filelist:
    print File
    f=open(File,'rU')
    title=f.readline()
    title=f.readline() # to get the title
    if title=='\n':
        title='<NO TITLE>'
    author=f.readline()
    author=f.readline()
    author=f.readline() #to get author
    if len(author.split(" "))>7:
        text=author+f.read()
    else:
        text=f.read()
    f.close()
    summ=summarize(text)
    FileSave=File.replace('2000/01','2000/Summarize')
    f=open(FileSave,'wb')
    f.write(title+'\n')
    for line in summ:
        f.write(line+'\n')
    f.close()    