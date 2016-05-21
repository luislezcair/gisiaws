import threading, time
import csv, operator
from optparse import OptionParser
from progress import *
from controllers import *
from search.testLinks import TestLinksClass #solo para hacer pruebas sin motor de busqueda
from draw.twoDimensionalDrawing import *
from algorithms.retrievalAlgorithms import *

class WebMinerController(threading.Thread):

    def __init__(self,cloudSize,algorithm,searchKey):
        super(WebMinerController, self).__init__()
        self.progress=Process()
        self.algorithm=algorithm
        self.searchKey=searchKey
        self.n=0
        self.cloudSize=cloudSize
        self.engineSearchController=EngineSearchController(self.progress)
        self.crawlerController=CrawlerController(self.progress)
        self.MEGA_CrawlerController=MEGA_CrawlerController(self.progress)
        self.IRController=InformationRetrievalController(self.progress)
        self.storageController=StorageController(self.progress)
        self.scraperController=ScraperController(self.progress)

    def run(self):
        print self.searchKey
        print self.cloudSize
        print self.algorithm.getName()
        self.minePackage=self.crawler()
        if not self.progress.get_stop():
            self.informationRetrieval(self.minePackage,self.algorithm)
        if not self.progress.get_stop():
            self.scraper(self.minePackage)

    def stopWebMiner(self):
        self.progress.set_stop(True)
        self.progress.set_crawlerState('Detenido')
        self.progress.set_IRState('Detenido')
        self.progress.set_scrapingState('Detenido')

    def search(self):
        if self.n==0:
            urls=TestLinksClass()
            return urls.getTestLinks(7)
        else:
            urls=self.engineSearchController.start(self.searchKey)
            j=0
            for l in urls:
                j+=1
                print j,'-',l
            return urls

    def crawler(self):
        return self.crawlerController.start(self.search(),self.cloudSize,self.searchKey)

    def MEGA_cloud(self,minePackage,enlaces):# enlaces: es la cantidad de enlaces aleatorios que se crearan
        self.MEGA_CrawlerController.start(minePackage,enlaces)

    def informationRetrieval(self,minePackage,algorithm):
        self.IRController.start(minePackage,algorithm)

    def scraper(self,minePackage):
        self.scraperController.start(minePackage)

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
        request = entities.get(r for r in entities.WSRequest if r.id == request_id)

        print "id_proyecto:", request.id_proyecto
        print "nombre_directorio:", request.nombre_directorio

        # url_list tiene una lista de (orden, URL)
        url_list = request.urls.order_by(Url.orden)

