from optparse import OptionParser
import networkx as nx
from pattern.web import URL
from progress import *
from controllers import *
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
        self.directorio = directorio
        self.cloudSize=cloudSize
        self.logController = LogsController(self.directorio)
        self.progress=Process(id_request,self.logController)
        self.crawlerController=CrawlerController(self.progress,directorio,id_request)
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

    def crawler(self):
        self.crawlerController.start(self.minePackage)

    def getProgress(self):
        return self.progress


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
