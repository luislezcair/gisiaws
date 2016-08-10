# -*- coding: utf-8 -*-
import copy
import pickle
import logging
import time
from progress import *
from webCrawler.crawler_07 import *
from webCrawler.crawler_08 import *
from webScraper.scraper import *
from pattern.web import URL
from search.engines import *
from webCrawler.tools import *
from models.ORM_functions import *
from algorithms.retrievalAlgorithms import *
from algorithms.tools.algorithmTools import MethodData

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

    def __init__(self,progress,directorio,id_request):
        super(CrawlerController,self).__init__(progress)
        self.IRController=InformationRetrievalController(self.progress)
        self.scraperController=ScraperController(self.progress)
        self.stop=False
        self.directorio = directorio
        self.id_request = id_request

    def trueNodesSelection(self,cloud):
        in_true=list()
        for n in cloud.graph.nodes():
            nod=cloud.graph.node[n]
            if nod['select']==True:
                in_true.append(n)
        return in_true

    def start(self,minePackage):
        self.progress.set_crawlerState('Ejecutandose')
        cloudSize=minePackage['cloudSize']
        searchKey=minePackage['searchKey']
        step=0
        while not self.progress.get_stop():
            clouds=minePackage['clouds']
            for cloud in clouds:

                true_nodes=self.trueNodesSelection(cloud)
                for n in true_nodes:
                    cloud.graph.node[n]['select']=False
                    if not self.progress.get_stop():
                        crawler7 = SimpleCrawler1(n,delay=0.1)
                        crawler7.newStructure(cloud.graph)
                        time=0
                        try:
                            sizeNube = len(cloud.graph.nodes())
                            while len(crawler7.visited)<cloudSize:
                                    if not self.progress.get_stop():
                                        print "Explorando ..."
                                        crawler7.crawl(method=None)
                                        time+=1
                                        if time>cloudSize*10:
                                            break
                                    else:
                                        break
                        except Exception, e:
                            print "error"
                            self.progress.exception = str(e)
                            self.progress.set_stop(True)
                            break

                        if sizeNube != len(cloud.graph.nodes()):
                            self.IRController.start(minePackage)
                            self.scraperController.start(minePackage,self.directorio,self.id_request)

                        if not self.progress.get_stop():
                                step+=1
                                self.progress.set_crawlerProgress(step)
                        #except ValueError:
                            #logging.warning('%s','ValueError: Invalid IPv6 URL')
                            #logging.critical(u'Error crítico -- cerrando')
                            #break
                        #except:
                            #logging.critical(u'Error crítico -- cerrando')
                            #break
                    else:
                        #print 'PROCESO DETENIDO!'
                        break
            if not self.progress.get_stop():
                print "No se encuentran mas Enlaces"
                # self.progress.set_stop(True)
            else:
                self.progress.set_crawlerState('Detenido')

        if not self.progress.get_stop():
            self.progress.set_crawlerState('Finalizado')




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

    def start(self,minePackage):
        self.descargarContenido(minePackage)
        pattern_methods=[VectorSpaceModel('Vector Space Model')]
        own_methods=[WeightedApproach('Weighted Approach'),Okapi('Okapi-BM25'),CRank('CRank')]
        for algorithm in pattern_methods:
            algorithm.run(minePackage,self.progress)

        for algorithm in own_methods:
            algorithm.run(minePackage,self.progress)

    def descargarContenido(self,minePackage):
        clouds = minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                if(cloud.graph.node[n]['methodData']==None):
                    unMethodData = MethodData("",cloud.graph.node[n]['link'])
                    cloud.graph.node[n]['methodData'] = unMethodData


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
                        scraperLinks.append(cloud.graph.node[n])
                    else:
                        self.progress.set_scrapingState('Detenido')
                        break
            else:
                break
        if not self.progress.get_stop():
            self.scraper.start(scraperLinks,self.progress,directorio,id_request,minePackage['searchKey'])
        else:
            self.progress.set_scrapingState('Detenido')
###END###
