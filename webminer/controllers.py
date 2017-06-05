# -*- coding: utf-8 -*-
import copy
import pickle
import logging
import time
import os
import datetime
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
                # print url
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


''' Controlador del Crawler'''
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

        logController = LogsController(self.directorio)
        logController.Info('Inicio Webminer')
        logController.Info(str(searchKey))

        while not self.progress.get_stop():
            clouds=minePackage['clouds']
            for cloud in clouds:

                true_nodes=self.trueNodesSelection(cloud)
                for n in true_nodes:
                    ''' Se setea en false para definir que dicha url fue explorada y no volver a utilizarlo'''
                    cloud.graph.node[n]['select']=False
                    if not self.progress.get_stop():
                        crawler7 = SimpleCrawler1(n,delay=0.1)
                        crawler7.newStructure(cloud.graph)
                        time=0
                        try:
                            sizeNube = len(cloud.graph.nodes())
                            while len(crawler7.visited)<cloudSize:
                                    if not self.progress.get_stop():
                                        # print "Explorando ..."
                                        ''' El crawler tiene method none. Es decir, no prioriza entre amplitud o profundidad '''
                                        crawler7.crawl(method=None)
                                        time+=1
                                        if time>cloudSize*10:
                                            break
                                    else:
                                        break
                        except Exception, e:
                            print "error"
                            print str(e)
                            logController.Warning(str(sys.exc_info()[0]) + " || " +  str(e))
                            self.progress.exception = str(sys.exc_info()[0]) + " || " +  str(e)
                            # self.progress.set_stop(True)
                            break

                        if sizeNube != len(cloud.graph.nodes()):
                            self.IRController.start(minePackage)
                            self.scraperController.start(minePackage,self.directorio,self.id_request)

                        if not self.progress.get_stop():
                                step+=1
                                tiempo = datetime.datetime.now()
                                logController.Info(str(tiempo) +' - Iteraccion numero: '+str(step) + ' - Cantidad Enlaces: ' + str(self.progress.totalIR))
                                self.progress.set_crawlerProgress(step)

                    else:
                        #print 'PROCESO DETENIDO!'
                        break
            if not self.progress.get_stop():
                print "No se encuentran mas Enlaces"
                # self.progress.set_stop(True)
            else:
                self.progress.set_crawlerState('Detenido')

        if not self.progress.get_stop():
            self.progress.set_crawlerState("Finalizado")

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

''' Controlador del Scraper '''
class ScraperController(Controller):

    #scraper=None
    def __init__(self,progress):
        super(ScraperController,self).__init__(progress)
        self.scraper=WebScraperClass()

    def start(self,minePackage,directorio,id_request):

        scraperLinks=[]
        clouds=minePackage['clouds']

        ''' Se recorre la nube para agregar los nodos en un conjunto nuevo'''
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
        ''' Inicio del proceso del scraper. '''
        if not self.progress.get_stop():
            self.scraper.start(scraperLinks,self.progress,directorio,id_request,minePackage['searchKey'])
        else:
            self.progress.set_scrapingState('Detenido')

''' Controlador para generar los logs del sistema '''
class LogsController(object):

    directorio = ""
    def __init__(self,directorio):
        super(LogsController,self).__init__()
        self.directorio = directorio
        import logging
        from models.config import config

        config = config()
        LOG_FILENAME = config.pathLog + self.directorio + '.log'

        if "/" in directorio:
            carpeta = self.directorio.split("/")[0]
            if not os.path.isdir(config.pathLog + carpeta):
                os.makedirs(config.pathLog + carpeta)

        LEVELS = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}

        if len(sys.argv) > 1:
            level_name = sys.argv[1]
            level = LEVELS.get(level_name, logging.NOTSET)
            logging.basicConfig(filename=LOG_FILENAME, level=level)

    def Debug(self,mensaje):
        logging.debug(mensaje)

    def Info(self,mensaje):
        logging.info(mensaje)

    def Warning(self,mensaje):
        logging.warning(mensaje)

    def Error(self,mensaje):
        logging.error(mensaje)

    def Critical(self,mensaje):
        logging.critical(mensaje)
###END###
