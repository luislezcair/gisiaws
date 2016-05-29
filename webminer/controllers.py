# -*- coding: utf-8 -*-
import copy
import pickle
import logging
from progress import *
from webCrawler.crawler_07 import *
from webCrawler.crawler_08 import *
from webScraper.scraper import *
from pattern.web import URL
from search.engines import *
from webCrawler.tools import *
from models.ORM_functions import *

class Controller(object):
    def __init__(self,progress):
        super(Controller,self).__init__()
        self.progress=progress
    def getProgress(self):
        return self.progress

class EngineSearchController(Controller):

    def __init__(self,progress):
        super(EngineSearchController,self).__init__(progress)

    def toList(self,urls):
        crawlerList=[]
        for link in urls:
            auxList=[]
            auxList.append(link)
            crawlerList.append(auxList)
        return crawlerList

    def remove(self,urls):
        for url in urls:
            badLink=Filter()
            if badLink.detect(url):
                print url
                urls.remove(url)
        return urls



    def start(self,searchKey):
        google=Google_Engine('Google')
        bing=Bing_Engine('Bing')
        #urlsGoogle=google.run(searchKey)
        urlsGoogle=[]
        urlsBing=bing.run(searchKey)
        urls=list(set(urlsGoogle) | set(urlsBing)) #este paso filtra enlaces repetidos
        urls=self.remove(urls) #este paso elimina las redes sociales, youtube y otros
        urls=self.toList(urls) #cambia el formato de la lista para enviar al crawler
        return urls



class CrawlerController(Controller):

    def __init__(self,progress):
        super(CrawlerController,self).__init__(progress)
        self.stop=False

    def start(self,links,cloudSize,searchKey):
        self.progress.set_totalCrawling(len(links))
        self.progress.set_crawlerState('Ejecutando')
        clouds=[]
        step=0
        for link in links:
            if not self.progress.get_stop():
                crawler7 = SimpleCrawler1(link,delay=0.1)
                crawler7.newStructure()
                print "WEB CRAWLER "+"-" * 50
                time=0
                try:
                    while len(crawler7.visited)<cloudSize:
                        if not self.progress.get_stop():
                            crawler7.crawl(method=DEPTH)
                            #crawler7.crawl(method=BREADTH)
                            time+=1
                            #if crawler7.getSocial()==1:
                            #    cloudSize+=1
                            #    crawler7.setSocial()
                            if time>cloudSize*10:
                                break
                        else:
                            #print "PROCESO DETENIDO!"
                            break
                    if not self.progress.get_stop():
                        url=URL(link.pop(0))
                        clouds.append(Structure((crawler7.getStructure()).copy(), url.domain))
                        step+=1
                        self.progress.set_crawlerProgress(step)
                        print
                except ValueError:
                    logging.warning('%s','ValueError: Invalid IPv6 URL')
                    logging.critical(u'Error crítico -- cerrando')
                    break
                except Exception, e:
                    print e
                    logging.critical(u'Error crítico -- cerrando')
                    break
            else:
                #print 'PROCESO DETENIDO!'
                break
        if not self.progress.get_stop():
            minePackage={'clouds':clouds,'searchKey':searchKey,}
            self.progress.set_crawlerState('Finalizado')
            return minePackage
        else:
            self.progress.set_crawlerState('Detenido')




class MEGA_CrawlerController(Controller):#Genera aleatoriamente conexiones interdominio mas complejas que crawler_7

    def __init__(self,progress):
        super(MEGA_CrawlerController,self).__init__(progress)

    def start(self,minePackage,enlaces):
        clouds=minePackage['clouds']
        G=list()
        for cloud in clouds:
            G.append(cloud.graph)
        m=MEGA(G)
        MEGA_nodos=m.get()
        MEGA_cloud=m.generate(MEGA_nodos,enlaces)
        minePackage['clouds']=[Structure(MEGA_cloud,'mega.com')]



class InformationRetrievalController(Controller):

    def __init__(self,progress):
        super(InformationRetrievalController,self).__init__(progress)

    def start(self,minePackage,algorithm):
        algorithm.run(minePackage,self.progress)



class StorageController(Controller):

    def __init__(self,progress):
        super(StorageController,self).__init__(progress)

    def save(self,minePackage):
        clouds=minePackage['clouds']
        searchKey=minePackage['searchKey']
        str_clouds= pickle.dumps(clouds)#serializa el objeto que contiene las nubes
        try:
            save(searchKey,str_clouds)
            print
            print '---------'
            print 'Guardado!   =)'
            print '---------'
            print
        except:
            print
            print '-------------------------------'
            print '#ATENCION: El registro ya existe! =/'
            print '-------------------------------'
            print

    def get(self,searchKey):
        minePackage={}
        try:
            search=get(searchKey)
            minePackage['searchKey']=search.searchKey
            minePackage['clouds']=pickle.loads(search.structures)
            print 'Clave de búsqueda encontrada!   =)'
            return minePackage
        except:
            print '#ATENCION: La clave de búsqueda no existe! =('

    def removeAll(self):
        try:
            drop()
            print 'Base de datos eliminada!'
        except:
            print '#ERROR'



class ScraperController(Controller):

    #scraper=None
    def __init__(self,progress):
        super(ScraperController,self).__init__(progress)
        self.scraper=WebScraperClass()

    def start(self,minePackage,directorio,id_request):
        scraperLinks=[]
        clouds=minePackage['clouds']
        for cloud in clouds:
            if not self.progress.get_stop():
                for n in cloud.graph.nodes():
                    if not self.progress.get_stop():
                        scraperLinks.append(cloud.graph.node[n]['link'])
                    else:
                        self.progress.set_scrapingState('Detenido')
                        break
            else:
                break
        if not self.progress.get_stop():
            self.scraper.start(scraperLinks,self.progress,directorio,id_request)
        else:
            self.progress.set_scrapingState('Detenido')
