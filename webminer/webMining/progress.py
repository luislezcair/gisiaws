# -*- coding: utf-8 -*-
class Process:
    
    def __init__(self):
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

    #web crawling process, getters() and setters()
    def set_totalCrawling(self,quantity):
        self.totalCrawling=quantity
        #print self.totalCrawling
    def set_crawlerProgress(self,progress):
        self.crawlerProgress=progress
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
