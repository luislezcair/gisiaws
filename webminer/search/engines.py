# -*- coding: utf-8 -*-
'''
1-Búsqueda en Google
2-Búsqueda en Bing
3-Eliminación de dominios no deseados:facebook,twitter,amazon,ebooks.google,youtube,etc...
4-Eliminación de enlaces deseados pero duplicados
'''
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.web import Google, Bing, asynchronous, plaintext
from pattern.web import SEARCH, IMAGE, NEWS
import time

class SearchEngine(object):

    name=str()

    def __init__(self,name):
        super(SearchEngine,self).__init__()
        self.name = name

    def badLink(self,link):
        pass



class Google_Engine(SearchEngine):

    def __init__(self,name):
        super(Google_Engine,self).__init__(name)
    
    def run(self,q):# q is the query
        engine = Google(license=None, language="en")
        # Google is very fast but you can only get up to 100 (10x10) results per query.
        urlsGoogle=[]
        for i in range(1,11):
            for result in engine.search(q, start=i, count=10, type=SEARCH, cached=True):
                urlsGoogle.append(result.url)
        return urlsGoogle



class Bing_Engine(SearchEngine):

    def __init__(self,name):
        super(Bing_Engine,self).__init__(name)

    def run(self,q):# q is the query
        urlsBing=[]
        engine = Bing(license=None) # Enter your license key.
        for i in range(1,11):
            for result in engine.search(q, type=SEARCH, start=i):
                urlsBing.append(result.url)
        return urlsBing



class Patent_Engine(SearchEngine):
    pass




'''
engine = Bing(license=None, language="en")
q = "\"is more important than\""
#q = "\"tea market in india\""

request = asynchronous(engine.search, q, start=1, count=100, type=SEARCH, timeout=10)

while not request.done:
    time.sleep(0.01)
    #print ".",

#print
#print

# An error occured in engine.search(), raise it.
if request.error:
    raise request.error

# Retrieve the list of search results.
j=0
for result in request.value:
    j+=1
    print j,'-',result.url
    #print result.text
    #print
'''

