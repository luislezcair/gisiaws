#import time
# -*- coding: utf-8 -*-
from tools.algorithmTools import *

#Inicio
class Algorithm(object):

    name=str()
    tokens=None

    def __init__(self,name):
        super(Algorithm,self).__init__()
        self.name = name

    def tokenizer(self,minePackage):
        tokens=Tokenizer()
        tokens.run(minePackage)

    def queryProcessor(self):
        processor=QueryProcessor()
        return processor
        #processor.processor(minePackage)

    def distanceVector(self):
        distance=DistanceVector()
        return distance

    def getName(self):
        return self.name
        
    def vectorSim(self):
        return VectorSimilarity()
    
    def weighting(self):
        return WeightingProccess()
    
    def __str__(self):
        return self.name



'''#### Booleano ################################################################
FUNCIONAMIENTO: El algoritmo booleano no hace ranking, solo convierte los documentos a una tabla binaria, luego se extraen documentos que satisfacen la expresion booleana.
                1.tokenizar todos los enlaces=Tokenizer+stemming+stop_words+TF
                2.filtrar documentos usando expresiones booleanas tipo: (t1 AND t2)OR t4 ...
'''
class Boolean(Algorithm):
    
    def __init__(self,name):
        super(Boolean,self).__init__(name)

    def run(self,minePackage):
        self.tokenizer(minePackage)
        self.booleanFilter(minePackage)

    def booleanFilter(self,minePackage):
        relevant=[]
        notRelevant=[]
        clouds=minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                methodData=cloud.graph.node[n]['methodData']
                document=methodData.getData()
                if ( (('analysi' in document)and('pattern' in document)and('googl' in document)) and ('coock' in document)):
                    relevant.append(cloud.graph.node[n]['link'])
                else:
                    notRelevant.append(cloud.graph.node[n]['link'])
        print 'INFORMATION RETRIEVAL ALGORITHM: Boolean method'
        print
        print 'Relevant links:'
        for rel in relevant:
            print rel
        print 'Total:',len(relevant)
        print
        print 'Not relevant links:'
        for nrel in notRelevant:
            print nrel
        print 'Total:',len(notRelevant)



'''#### Booleano Extendido #####################################################
FUNCIONAMIENTO: El metodo booleano extendido se basa en la idea de que cuanto mayor es la frecuencia de
                un termino en el documento, mayor sera la relevancia que dicho termino le aporte al documento
'''
class ExtendedBoolean(Algorithm):

    def __init__(self,name):
        super(ExtendedBoolean,self).__init__(name)
    
    def run(self,minePackage):
        self.tokenizer(minePackage)
        self.booleanFilter(minePackage)
    
    def booleanFilter(self,minePackage):
        weightedList={}
        query='python','support','express','sign','zero','mathemat','ceil'
        clouds=minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                methodData=cloud.graph.node[n]['methodData']
                document=methodData.getData()
                #print len(document)
                weightedList[cloud.graph.node[n]['link']]=self.extendedOperator(document,query)
        self.ranking(weightedList)
    
    def extendedOperator(self,document,query):
        tf=[]
        for w in query:
            if w in document:
                tf.append(document[w])
            else:
                tf.append(0)
        return tf[0]*tf[1]*tf[2]+(tf[3]+tf[4]+tf[5]+tf[6])
    
    def ranking(self,weightedList):
        print 'INFORMATION RETRIEVAL ALGORITHM: Extended boolean method'
        print
        print 'Ranking:'
        print
        ranking=sorted(weightedList.items(),key = lambda x:x[1])
        #Orden Descendente:
        i=len(ranking)-1
        elem=-1
        f=1
        while i>=0:
            print f,'|||',ranking[elem][0],'||| W=',ranking[elem][1]
            elem-=1
            i-=1
            f+=1


'''#### Modelo de espacio vectorial #####################################################'''
'''FUNCIONAMIENTO: Cada documento se representa como un vector en el espacio n-dimensional. La clave de
                   búsqueda también se representa de la misma manera. Luego, el cálculo de relevancia
                   consiste en medir la distancia de cada vector-documento al vector consulta. Cuanto más
                   próximo esta un vector-documento del vector-consulta se lo considera de mayor relevancia.'''
class VectorSpaceModel(Algorithm):

    def __init__(self,name):
        super(VectorSpaceModel,self).__init__(name)

    def run(self,minePackage,progress):#recibe como parametro una referencia de la clase progress
        weightedList={}
        query=minePackage['searchKey']
        vectorSimilarity=self.vectorSim()
        vectorSimilarity.calculate(minePackage,progress)#como parametro le pasa el objeto que registra los progresos del algoritmo
        clouds=minePackage['clouds']
        if not progress.get_stop():
            for cloud in clouds:
                if not progress.get_stop():
                    for n in cloud.graph.nodes():
                        weightedList[cloud.graph.node[n]['link']]=cloud.graph.node[n]['weight']
                else:
                    progress.set_IRState('Detenido')
                    break
            if not progress.get_stop():
                self.ranking(weightedList,progress)
                progress.set_IRState('Finalizado')##Actualiza el estado del proceso
        else:
            progress.set_IRState('Detenido')
    
    ''' FUNCION RANKING '''
    def ranking(self,weightedList,progress):
        print 'INFORMATION RETRIEVAL ALGORITHM: Vector Space Model'
        print
        print 'Ranking:'
        print
        ranking=sorted(weightedList.items(),key = lambda x:x[1])
        #Orden Descendente:
        i=len(ranking)-1
        elem=-1
        f=1
        while i>=0:
            if not progress.get_stop():
                print f,'|||',ranking[elem][0],'||| W=',ranking[elem][1]
                elem-=1
                i-=1
                f+=1
            else:
                progress.set_IRState('Detenido')
                break



'''#### Documento Vector #####################################################'''
class DocumentVector(Algorithm):
    
    def __init__(self,name):
        super(DocumentVector,self).__init__(name)
    
    def run(self,minePackage):
        weightedList={}
        self.tokenizer(minePackage)
        processor=self.queryProcessor()
        processor.processor(minePackage)
        distance=self.distanceVector()
        distance.run(minePackage)
        clouds=minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                weightedList[cloud.graph.node[n]['link']]=cloud.graph.node[n]['weight']
        self.ranking(weightedList)
    
    def ranking(self,weightedList):
        print 'INFORMATION RETRIEVAL ALGORITHM: Document Vector'
        print
        print 'Ranking:'
        print
        ranking=sorted(weightedList.items(),key = lambda x:x[1])
        #Orden Descendente:
        i=len(ranking)-1
        elem=-1
        f=1
        while i>=0:
            print f,'|||',ranking[elem][0],'||| W=',ranking[elem][1]
            elem-=1
            i-=1
            f+=1



'''#### Enfoque Ponderado #####################################################'''
class WeightedApproach(Algorithm):
    def __init__(self,name):
        super(WeightedApproach,self).__init__(name)
    def run(self,minePackage):
        weightedList={}
        self.tokenizer(minePackage)#Descarga contenido y lo tokeniza
        processor=self.queryProcessor()#Se instancia un procesador de query
        processor.processor(minePackage)#Se tokeniza la query
        weightingProccess=self.weighting()#Se instancia la clase encargada de ponderar contenido de los nodos
        weightingProccess.run(minePackage)#Se inicia proceso de ponderacion de nodos
        clouds=minePackage['clouds']#se extraen las nubes del paquete
        for cloud in clouds:
            for n in cloud.graph.nodes():
                weightedList[cloud.graph.node[n]['link']]=cloud.graph.node[n]['weight']#Genera un diccionario con los enlaces ponderados
        self.ranking(weightedList)#Se presentan enlaces web en un Ranking

    def ranking(self,weightedList):
        print 'INFORMATION RETRIEVAL ALGORITHM: Weighted Approach'
        print
        print 'Ranking:'
        print
        ranking=sorted(weightedList.items(),key = lambda x:x[1])
        #Orden Descendente:
        i=len(ranking)-1
        elem=-1
        f=1
        while i>=0:
            print f,'|||',ranking[elem][0],'||| W=',ranking[elem][1]
            elem-=1
            i-=1
            f+=1



'''#### Ranking Colaborativo #####################################################'''
class CRank(Algorithm):
    def __init__(self,name):
        super(CRank,self).__init__(name)

'''#### Support Vector Machine #####################################################'''
class SupportVectorMachine(Algorithm):
    def __init__(self,name):
        super(SupportVectorMachine,self).__init__(name)

'''#### Latent Semantic Analysis #####################################################'''
class LatentSemanticAnalysis(Algorithm):
    def __init__(self,name):
        super(LatentSemanticAnalysis,self).__init__(name)
