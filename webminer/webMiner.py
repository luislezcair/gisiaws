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

    # cloudSize = Parametro que define cuantas urls buscar por cada nodo a analizar 
    # searchKey = Clave de busqueda generada en el mail.
    # id_request = id obtenido mediante el parametro.
    # urls obtenidos de los buscadores
    # Nombre del directorio donde se almacenan los mejores 50 documentos. Generado por el nombre del proyecto creado en la interfaz.
    def __init__(self,cloudSize = 10,searchKey = "" ,id_request = 0, urls = [] , directorio = ""):
        super(WebMinerController, self).__init__()
        self.minePackage=dict()
        self.searchKey=searchKey
        self.n=0
        self.directorio = directorio
        self.cloudSize=cloudSize
        self.logController = LogsController(self.directorio)
        self.progress=Process(id_request,self.logController)
        self.engineSearchController=EngineSearchController(self.progress)
        self.crawlerController=CrawlerController(self.progress,directorio,id_request)
        self.MEGA_CrawlerController=MEGA_CrawlerController(self.progress)
        self.IRController=InformationRetrievalController(self.progress)
        self.storageController=StorageController(self.progress)
        self.scraperController=ScraperController(self.progress)
        self.urls = urls
        self.id_request = id_request
    
    # inicio del webminer.
    # Minepackage es un array que contiene todos los datos necesarios para el proceso del webminer.
    def run(self):
        self.minePackage['searchKey']=self.searchKey
        unProcessor = QueryProcessor()
        self.minePackage['searchKeyStemmer'] = unProcessor.processor(self.minePackage)#Se tokeniza la query

        self.minePackage['cloudSize']=self.cloudSize
        self.minePackage['clouds']=self.startClouds(self.urls)        

        self.crawler()

    def stopWebMiner(self):
        self.progress.set_stop(True)
        self.progress.set_crawlerState('Detenido')
        self.progress.set_IRState('Detenido')
        self.progress.set_scrapingState('Detenido')

    ''' Funcion para crear la nube dada la lista de urls inicial '''
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

    def search(self):
        if self.test:
            urls=TestLinksClass()
            links=urls.getTestLinks(self.numOfClouds)
            return links
        else:
            print "##### ",self.searchKey
            urls=self.engineSearchController.start(self.searchKey)
            return urls

    def crawler(self):
        self.crawlerController.start(self.minePackage)

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

# Inicio del proceso de Webminer #
# Parametro: request_id del proceso iniciado #
if __name__ == '__main__':
    
    # parser de las opciones ingresadas en el comando#
    parser = OptionParser()
    parser.add_option("-r", "--request", dest="request_id")

    (options, args) = parser.parse_args()
    request_id = options.request_id

    # import entities. Clase que mapeo en objetos los datos de la db.
    from models import entities

    with db_session:
        # get entities que coincidan con el --request del parametro.
        request = entities.get(r for r in entities.WSRequest if r.request_id == request_id)

        print "id_proyecto:", request.id_proyecto
        print "nombre_directorio:", request.nombre_directorio

        # Se obtienen las claves generados.
        searchkeys = Searchkeys_searchkey.select(lambda p: p.request_id == request_id)
        consulta = ""
        for searchKey in searchkeys:
            consulta = consulta + str(searchKey.clave) + " "
        
        # las consultas de busquedas se concatenan en un string.
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
    
    # Inicio del proceso del webminer.
    print "Inicio del proceso de webminer"
    wm = WebMinerController(id_request = request_id , searchKey = consulta,  urls = urls , directorio = nombre_directorio)
    wm.run()
