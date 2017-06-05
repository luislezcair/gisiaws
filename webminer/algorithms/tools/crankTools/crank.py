from __future__ import division
from pattern.vector import *


class CRanking:

    def __init__(self):
        self.levels=list()
        self.back=3


    def run(self,minePackage):
        clouds=minePackage['clouds']
        query = minePackage['searchKeyStemmer']
        unaListaDocumentos = []
        unaListaModel = []
        for cloud in clouds:
            for n in cloud.graph.nodes():
                content = cloud.graph.node[n]['methodData'].getContent()

                unDocumento = DocumentoCrank()
                unDocumento.url = cloud.graph.node[n]['link']
                unDocumento.contenido = content
                unDocumento.pattern = Document(content, stemmer = PORTER, name=unDocumento.url)
                unaListaDocumentos.append(unDocumento)
                unaListaModel.append(unDocumento.pattern)

        model = Model(documents=unaListaModel, weight=TFIDF)
        ''' Se calcula el score general de cada documento en base a su contenido '''
        for unDocumento in unaListaDocumentos:
            unDocumento.score = self.calcular_score_relevance_crank(unDocumento,query,model)

        ''' Se arma el grafo para llevar a cabo el calculo de relevancia de contribucion'''
        for cloud in clouds:
            self.levels=list()
            for n in cloud.graph.nodes():
                self.backLinks(cloud,n,0)

                auxiliarBackLinks = list()
                for level in self.levels:
                    for link in level:
                        auxiliarBackLinks.append(link)

                unDocumentBack = None
                unDocumento = next((x for x in unaListaDocumentos if x.url == n), None)
                documentosInlinks = []
                for link in list(set(auxiliarBackLinks)):
                    unDocumentoBack = next((x for x in unaListaDocumentos if x.url == link), None)
                    documentosInlinks.append(unDocumentoBack)
                unDocumento.inlinks = documentosInlinks

        ''' Una vez obtenido el grafo, se calcula el Crank final '''
        self.calcular_Crank(unaListaDocumentos)

        ''' Se guarda el valor Crank a la nube de nodos creado por el crawler '''
        for cloud in clouds:
            for n in cloud.graph.nodes():
                cloud.graph.node[n]['weight_CRANK'] = next((x for x in unaListaDocumentos if x.url == n), None).score

    def contains(self,list, filter):
        for x in list:
            if filter(x):
                return True
        return False

    ''' Backlinks hace referencia a, dada una pagina, buscar aquellas que hacen referencia a dicha pagina mediante un enlace'''
    def backLinks(self,cloud,node,repeat):
        if repeat<self.back:
            repeat+=1
            if len(cloud.graph.predecessors(node))!=0:
                self.levels.append(cloud.graph.predecessors(node))
                for n in cloud.graph.predecessors(node):
                    self.backLinks(cloud,node,repeat)

    ''' Funcion definida en el paper del crank para el calculo de la relevancia '''
    def coord(self,documento, consulta):
        contador = 0
        for word in consulta:
            ''' documento.pattern.words es una bolsa de palabras que se encuentran en el documento'''
            if word in documento.pattern.words:
                contador =+1
        return (contador / len(consulta))

    ''' Funcion definida en el paper del crank para el calculo de la relevancia '''
    def norm(self,documento, un_termino):
        valor = 0
        if un_termino in documento.pattern.vector:
            ''' Se obtiene el valor de frecuencia del termino '''
            valor = documento.pattern.vector[un_termino]
        return valor

    ''' Funcion definida para realizar el calculo de relevancia parcial
        Se recibe como parametro el documento, la consulta de busqueda y el modelo de la libreria pattern
    '''
    def calcular_score_relevance_crank(self,doc,consulta,model):
        score_relevance = 0
        var_coord = self.coord(doc,consulta)
        for termino in consulta:
            # score_relevance += doc.pattern.tfidf(termino) * self.norm(doc,termino)*var_coord
            score_relevance += self.norm(doc,termino)*var_coord * model.document(doc.url).vector.get(termino,0)
        doc.score_relevance = score_relevance

    ''' Funcion definida para obtener los puntajes de cada pagina teniendo en cuenta sus referencias '''
    def calcular_score_inlinks(doc):
       score = 0
       for inlink in doc.inlinks:
           if inlink != doc:
               if len(inlink.inlinks) > 0:
                   for aux_inlink in inlink.inlinks:
                       if aux_inlink != doc:
                           score += aux_inlink.score_relevance
                   return score
               else:
                   return 0

       return score

    ''' Funcion definida para obtener el puntaje de contribucion
        Como parametro utiliza el documento, el nivel del documento y todos los documentos ya analizados
        para evitar bucles infinitos.
    '''
    def calcular_score_contribution(self,doc,nivel,analizados):
        score = 0;

        if nivel < 4:
            if not doc in analizados:
                analizados.append(doc)
                if doc.inlinks:
                    for inlink in doc.inlinks:
                        score += self.calcular_score_contribution(inlink,nivel+1,analizados)
                        if inlink.inlinks:
                            score_inlink = 0
                            for aux_inlink in inlink.inlinks:
                                score_inlink += aux_inlink.score_relevance
                            if inlink.score_relevance+score_inlink > 0:
                                score += (doc.score_relevance/(inlink.score_relevance+score_inlink))*inlink.score_relevance
                            else:
                                score += doc.score_relevance
                        else:
                            score += doc.score_relevance
        return score

    ''' Funcion definida para realizar el calculo de relevancia final
        Se recorre la lista de documentos, se calcula el puntaje de contribuccion y se aplica
        la formula.
    '''
    def calcular_Crank(self,unaListaDocumentos):
        # print "SCORE RELEVANCE"
        for doc in unaListaDocumentos:
            analizados = []
            doc.score_contribution = self.calcular_score_contribution(doc,0,analizados)
            doc.score = 0.80 * doc.score_relevance + 0.20 * doc.score_contribution
            # print doc.score_relevance
##end##

''' Clase para representar el Documento o Pagina'''
class DocumentoCrank:
    url = ""
    contenido = ""
    pattern = ""
    score_crank = 0
    score_contribution = 0
    score_relevance = 0
    score_inlink = 0
    inlinks = []
