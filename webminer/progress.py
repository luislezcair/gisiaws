from models.entities import *
from models import ORM_functions
from models import entities

# -*- coding: utf-8 -*-
class Process:

    def __init__(self,id_request):
        self.crawlerState='Esperando'
        self.crawlerProgress=0
        self.totalCrawling=0

        self.scraperState='Esperando'
        self.scraperProgress=0
        self.totalScraping=0

        self.IRState='Esperando'
        self.IRProgress=0
        self.totalIR=0

        self.stop=False

        self.state=dict()
        self.id_request = id_request


        with db_session:
            estado = WsRequestState(estado = unicode(self.state), stop = False , search_keys = id_request)
            commit()


        # para inicializar el estado en la bd
        self.get_progress()

    #web crawling process, getters() and setters()
    def set_totalCrawling(self,quantity):

        self.totalCrawling=quantity
        #print self.totalCrawling
    def set_crawlerProgress(self,progress):
        self.crawlerProgress=progress

        with db_session:
           estadoActual = WsRequestState.get(search_keys = self.id_request)
           estadoActual.estado = unicode(self.get_progress())
           commit()

        self.comprobar_estado()
        #print self.crawlerProgress
    def set_crawlerState(self,state):
        self.crawlerState=state
        #print self.crawlerState
    def get_crawlerProgress(self):
        return self.crawlerProgress
    def get_crawlerState(self):
        return self.crawlerState
    def get_totalCrawling(self):
        return self.totalCrawling

    #web scraping process, getters() and setters()
    def set_totalScraping(self,quantity):
        self.totalScraping=quantity
        #print self.totalScraping
    def set_scrapingProgress(self,progress):
        self.scraperProgress=progress

        with db_session():
              estadoActual = WsRequestState.get(search_keys = self.id_request)
              estadoActual.estado = unicode(self.get_progress())
              commit()

        #print self.scraperProgress
    def set_scrapingState(self,state):
        self.scraperState=state
        #print self.scraperState
    def get_totalScraping(self):
        return self.totalScraping
    def get_scrapingProgress(self):
        return self.scraperProgress
    def get_scrapingState(self):
        return self.scraperState

    #information retrival process, getters() and setters()
    def set_totalIR(self,quantity):
        self.totalIR=quantity
    def set_IRProgress(self,progress):
        self.IRProgress=progress
        with db_session():
             estadoActual = WsRequestState.get(search_keys = self.id_request)
             estadoActual.estado = unicode(self.get_progress())
             commit()

    def set_IRState(self,state):
        self.IRState=state
    def get_totalIR(self):
        return self.totalIR
    def get_IRProgress(self):
        return self.IRProgress
    def get_IRState(self):
        return self.IRState

    #stop process, getters() and setters()
    def set_stop(self,stop):
        self.stop=stop
    def get_stop(self):
        return self.stop

    #get progress
    def get_progress(self):
        self.state['exploracion']=self.crawlerState+'||'+str(self.crawlerProgress)+'/'+str(self.totalCrawling)
        self.state['ranking']=self.IRState+'||'+str(self.IRProgress)+'/'+str(self.totalIR)
        self.state['extraccion']=self.scraperState+'||'+str(self.scraperProgress)+'/'+str(self.totalScraping)

        return self.state

    @db_session(serializable=True)
    def comprobar_estado(self):
         estadoActual = WsRequestState.get(search_keys = self.id_request)
         if estadoActual.stop:
             self.set_stop(True)
