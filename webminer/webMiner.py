import threading, time, csv, operator
from optparse import OptionParser
import networkx as nx
from pattern.web import URL
from progress import *
from controllers import *
from search.testLinks import TestLinksClass #solo para hacer pruebas sin motor de busqueda
from draw.twoDimensionalDrawing import *
from algorithms.retrievalAlgorithms import *
from algorithms.tools.algorithmTools import QueryProcessor

class Structure:#es un clase auxiliar para encapsular una estructura.

    def  __init__(self,graph,domain):
        self.graph=graph
        self.domain=domain
    def getGraph(self):
        return self.graph
    def getDomain(self):
        return self.domain


class WebMinerController(object):

    def __init__(self,cloudSize = 100,searchKey = "" ,id_request = 0, urls = [] , directorio = ""):
        super(WebMinerController, self).__init__()
        self.progress=Process(id_request)
        self.minePackage=dict()
        self.searchKey=searchKey
        self.n=0
        self.directorio = directorio
        self.cloudSize=cloudSize
        self.engineSearchController=EngineSearchController(self.progress)
        self.crawlerController=CrawlerController(self.progress,directorio,id_request)
        self.MEGA_CrawlerController=MEGA_CrawlerController(self.progress)
        self.IRController=InformationRetrievalController(self.progress)
        self.storageController=StorageController(self.progress)
        self.scraperController=ScraperController(self.progress)
        self.urls = urls
        self.id_request = id_request


    def run(self):
        self.minePackage['searchKey']=self.searchKey
        unProcessor = QueryProcessor()
        self.minePackage['searchKeyStemmer'] = unProcessor.processor(self.minePackage)#Se tokeniza la query

        self.minePackage['cloudSize']=self.cloudSize
        self.minePackage['clouds']=self.startClouds(self.urls)

        # clouds = self.minePackage['clouds']
        # for cloud in clouds:
        #     print cloud.graph.nodes()
        #     for n in cloud.graph.nodes():
        #         print n

        self.crawler()

    def stopWebMiner(self):
        self.progress.set_stop(True)
        self.progress.set_crawlerState('Detenido')
        self.progress.set_IRState('Detenido')
        self.progress.set_scrapingState('Detenido')

    def startClouds(self,urls):
        clouds=list()
        for n in urls:
            url=URL(n[0])
            graph=nx.DiGraph()
            graph.add_node(n[0],
                           select=True,
                           ID=0,
                           weight_VSM=0.0,
                           weight_WA=0.0,
                           weight_OKAPI=0.0,
                           weight_SVM=0.0,
                           weight_CRANK=0.0,
                           totalScore=0.0,
                           link=n[0],
                           methodData=None,
                           )
            clouds.append(Structure(graph,url.domain))
        return clouds


    def stopWebMiner(self):
        #self.progress.set_running(False)
        self.progress.set_stop(True)
        self.progress.set_crawlerState('Detenido')
        self.progress.set_IRState('Detenido')
        self.progress.set_scrapingState('Detenido')

    #def setStop(self):
    #    self.progress.set_stop(False)
    #    #self.progress.set_running(True)

    def search(self):
        if self.test:
            urls=TestLinksClass()
            links=urls.getTestLinks(self.numOfClouds)
            return links
        else:
            print "##### ",self.searchKey
            urls=self.engineSearchController.start(self.searchKey)
            #j=0
            #for l in urls:
            #    j+=1
            #    print j,'-',l
            return urls

    def crawler(self):
        self.crawlerController.start(self.minePackage)

    def MEGA_cloud(self,minePackage,enlaces):# enlaces: es la cantidad de enlaces aleatorios que se crearan
        self.MEGA_CrawlerController.start(minePackage,enlaces)

    def informationRetrieval(self):
        self.IRController.start(self.minePackage)

        self.IRController.start(minePackage,pattern_methods,own_methods)

    def scraper(self,minePackage):
        self.scraperController.start(minePackage,self.directorio,self.id_request)

    def getProgress(self):
        return self.progress

    def getState(self):
        print self.progress.get_progress()

    ##### FUNCIONES ADICIONALES ######
    def printClouds(self,minePackage):#Imprime nubes en consola
        clouds=minePackage['clouds']
        print '-'*100
        print 'query:',minePackage['searchKey']
        for cloud in clouds:
            print cloud.domain
            print cloud
            print cloud.graph.nodes(True)

    def drawClouds(self,minePackage): #Visulalizacion grafica de las nubes de enlaces
        clouds=minePackage['clouds']
        draw=DrawCloud()
        draw.plotFunction(clouds)
        #for cloud in clouds:
            #nx.draw(cloud.structure,node_size=300,alpha=0.8,node_color="cyan")

    def saveClouds(self,minePackage):#Guarda en disco local las nubes contenidas en minaPackage despues del crawler
        self.storageController.save(minePackage)

    def retrieveClouds(self,searchKey):#Recupera una nube de la base de datos directamente relacionada con una clave de busqueda
        return self.storageController.get(searchKey)
        #self.minePackage=self.storageController.get(searchKey)

    def deleteSearch(self,searchKey):#Elimina una nube relacionada a una query de la base de datos
        pass

    def removeAllSearches(self):
        self.storageController.removeAll()

    def csv(self,minePackage):#convierte una nube de enlaces a formato csv para poder visualizarla con el programa Gephi
        clouds=minePackage['clouds']
        csvNodes=open('/home/matt/clusterProject/webMining/csv/nodes.csv','w')
        csvEdges=open('/home/matt/clusterProject/webMining/csv/edges.csv','w')
        csvNodes=csv.writer(csvNodes,delimiter=';')
        csvEdges=csv.writer(csvEdges,delimiter=';')
        print('Escribiendo archivo "salida.csv"...')
        csvNodes.writerow(['Label','Id','Weight'])
        csvEdges.writerow(['Source','Target','Type'])

        for cloud in clouds:
            for n in cloud.graph.nodes():
                label=cloud.graph.node[n]['link']
                ID=cloud.graph.node[n]['ID']
                weight=cloud.graph.node[n]['weight']
                csvNodes.writerow([label,ID,weight])
                G=cloud.graph
                succ=G.successors(cloud.graph.node[n]['link'])
                for s in succ:
                    nod=cloud.graph.node[s]
                    source=ID
                    target=cloud.graph.node[s]['ID']
                    csvEdges.writerow([source,target,'Directed'])

    def report(self,minePackage):
        clouds=minePackage['clouds']
        visited=0
        for cloud in clouds:
           visited+=len(cloud.graph)
        totalLinks=len(self.search())*self.cloudSize
        print "  Total links.....", totalLinks
        print "Visited links.....", visited
        print "Missing links.....", totalLinks-visited

'''------------------------------------ADMIN------------------------------------------------------ '''
#Inicializar:
#wm=WebMinerController()

#RUN SEARCH ENGINES:
#wm.search()

#CRAWLER AND SCRAPER:
#minePackage=wm.crawler()
#wm.MEGA_cloud(minePackage,0)
#wm.scraper(minePackage)

#INFORMATION RETRIEVAL ALGORITHMS:
#wm.informationRetrieval(minePackage,wm.algorithm)

#PRINT AND DRAW:
#wm.printClouds(minePackage)
#wm.drawClouds(minePackage)
#wm.report(minePackage)

#GUARDAR Y RECUPERAR CLOUDS:
#wm.saveClouds(minePackage)
#wm.retrieveClouds(searchKey)
#wm.csv(minePackage)
'''----------------------------------------------------------------------------------------------- '''

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-r", "--request", dest="request_id")

    (options, args) = parser.parse_args()
    request_id = options.request_id

    from models import entities

    with db_session:
        request = entities.get(r for r in entities.WSRequest if r.request_id == request_id)

        print "id_proyecto:", request.id_proyecto
        print "nombre_directorio:", request.nombre_directorio

        # claves = entities.get(a for a in entities.Searchkeys_searchkey if a.request_id == request_id)
        searchkeys = Searchkeys_searchkey.select(lambda p: p.request_id == request_id)
        consulta = ""
        for searchKey in searchkeys:
            consulta = consulta + str(searchKey.clave) + " "

        consulta =  " ".join(filter(lambda x:x[0]!='-', consulta.split()))
        nombre_directorio = request.nombre_directorio
        # url_list tiene una lista de (orden, URL)
        url_list = request.urls.order_by(Url.orden)

    # urls contiene la lista de urls con el formato valido del crawler
        urls = []
        for url in url_list:
            urlAux = []
            urlAux.append(url.url)
            urls.append(urlAux)
        flush()

    wm = WebMinerController(id_request = request_id , searchKey = consulta,  urls = urls , directorio = nombre_directorio)
    wm.run()
