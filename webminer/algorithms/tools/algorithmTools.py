# -*- coding: utf-8 -*-
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import math
import commands
import networkx as nx
from pattern.en import parse, Sentence
from pattern.web import URL, plaintext, MIMETYPE_PDF
from pattern.vector import stem, PORTER, LEMMA, count, words, Vector, distance, Document, Model, TFIDF



class QueryProcessor:
    def __init__(self):
        pass
    def processor(self,minePackage):
        # print '####SEARCH_KEY:',minePackage['searchKey']
        s = Sentence(parse(minePackage['searchKey']))
        minePackage['searchKey']=count(words(s), stemmer=PORTER)
        return minePackage['searchKey']


class UrlToPlainText:
    def __init__(self):
        pass

    ''' funcion que dado un link, descarga el contenido y lo transforma en texto plano
        En el caso de que sea un archivo pdf, lo descarga y luego utiliza la libreria pdf2txt para transformar
        un pdf a texto. Luego que obtiene el texto, elimina el pdf.
    '''
    def plainTextConverter(self,link,metodo = "SinEtiquetas"):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        url=URL(link)
        txtContent =""
        try:
            if url.mimetype in MIMETYPE_PDF:
                document = open (os.path.dirname(os.path.abspath(__file__))+'/temp.pdf','w')
                document.close()
                download = url.download()
                document = open(os.path.dirname(os.path.abspath(__file__))+'/temp.pdf','a')
                document.write(download)
                document.close()
                txtContent=commands.getoutput('pdf2txt.py '+os.path.dirname(os.path.abspath(__file__))+'/temp.pdf')
                os.remove(os.path.dirname(os.path.abspath(__file__))+'/temp.pdf')
            else:
                page = URL(url).download(user_agent='Mozilla/5')
                if metodo == "mantenerEtiquetas":
                    txtContent = page
                else:
                    txtContent= plaintext(page, keep={})
        except:
            pass
        return txtContent



class MethodData:
    data=None
    contenido=None
    contenidoConEtiquetas=None
    def __init__(self , data, url=""):
        if url != "":
            urlContent = UrlToPlainText()
            self.contenidoConEtiquetas = urlContent.plainTextConverter(url,"mantenerEtiquetas")
            self.contenido = plaintext(self.contenidoConEtiquetas,keep={})
        else:
            self.contenido = ""
        self.data = count(words(Sentence(parse(self.contenido))), stemmer=PORTER)
    def getData(self):
        return self.data
    def getContent(self):
        return self.contenido



class Tokenizer:
    '''tokenizer, remove stop words, stemmer'''
    def __init__(self):
        pass
    def run(self,minePackage):
        clouds=minePackage['clouds']
        urlContent=UrlToPlainText()
        for cloud in clouds:
            for n in cloud.graph.nodes():#Itera una lista de enlaces de la nube
                # print cloud.graph.node[n]['link']
                pageContent=urlContent.plainTextConverter(cloud.graph.node[n]['link'])
                cloud.graph.node[n]['methodData']=MethodData(count(words(Sentence(parse(pageContent))), stemmer=PORTER))
        #return minePackage



class VectorSimilarity:# Similitud vectorial con distancia del coseno, metodo VSM
    def __init__(self):
        pass
    def calculate(self,minePackage,progress):
        webDocuments=[]
        query=Document((minePackage['searchKey']))
        clouds=minePackage['clouds']
        count=UnPack()
        totalLinks=count.total(clouds)
        progress.set_totalIR(totalLinks)#Total de documentos a recuperar
        progress.set_IRState('Ejecutando')#Actualiza el estado del proceso
        urlContent=UrlToPlainText()
        step=0
        for cloud in clouds:
            if not progress.get_stop():
                for n in cloud.graph.nodes():
                    if not progress.get_stop():
                        doc=cloud.graph.node[n]['methodData']
                        webDocuments.append(Document(doc.getData()))
                        step+=1
                        progress.set_IRProgress(step)#Progreso del proceso paso a paso
                    else:
                        break
            else:
                break
        if not progress.get_stop():
            m=Model(documents=webDocuments, weight=TFIDF)
            for cloud in clouds:
                for n in cloud.graph.nodes():
                    methodData=cloud.graph.node[n]['methodData']
                    vector=Document(methodData.getData())
                    cloud.graph.node[n]['weight_VSM']=m.similarity(vector,query)



class UnPack:
    def __init__(self):
        pass
    def total(self,clouds):
        total=0
        for cloud in clouds:
            total+= len(cloud.graph.nodes())

        return total



class DistanceVector:# Por ahora no se usa este metodo.
    def __init__(self):
        pass
    def run(self,minePackage):
        q=Vector(minePackage['searchKey'])
        clouds=minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                methodData=cloud.graph.node[n]['methodData']
                v=Vector(methodData.getData())
                cloud.graph.node[n]['weight']=1-distance(v,q)
        #for cloud in clouds:
            #print '---cloud---'
            #for n in cloud.graph.nodes():
                #print 'Distance: ',cloud.graph.node[n]['weight']



class DomainDictionary:
    domainDictionary=str()
    def __init__(self,f):
        self.f=f
        self.domainDictionary=self.f.read()
    def validate(self,word=''):
        return word in self.domainDictionary
#obj=DomainDictionary()
#print obj.validate('tea')

''' Calculo del enfoque ponderado utilizando el minePackage y el diccionario de datos'''
class WeightingProccess:# Calculo de relevancia del metodo de enfoque ponderado

    def __init__(self):
       pass

    def run(self,minePackage):
        ac=0.0 #acierto clave
        ap=0.0 #acierto positivo
        an=0.0 #acierto negativo
        alpha=1.00
        beta=0.75
        gamma=0.25
        dictionary= open(os.path.dirname(__file__) + "/dictionary.txt",'r').read()
        dictionary = Document(dictionary, stemmer = PORTER)
        clouds=minePackage['clouds']
        query=minePackage['searchKeyStemmer']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                methodData=cloud.graph.node[n]['methodData']
                content = Document(methodData.getContent(),stemmer = PORTER)
                for doc in content.keywords(top=500,normalized=True):
                    if doc[1] in query and doc[1] in dictionary.words:
                        ac += doc[0]
                    elif doc[1] in dictionary.words:
                        ap += doc[0]
                    elif doc[1] in query:
                        an += doc[0]
                if ac+ap+an > 0:
                    cloud.graph.node[n]['weight_WA']=((ac*alpha)+(ap*beta)+(an*gamma))/(ac+ap+an)
                else:
                    cloud.graph.node[n]['weight_WA']=0

                #print cloud.graph.node[n]['weight']

#urlContent=UrlToPlainText()
#pageContent=urlContent.plainTextConverter('http://www.clips.ua.ac.be/sites/default/files/ctrs-002_0.pdf')
#pageContent=urlContent.plainTextConverter('http://www.clips.ua.ac.be/pages/pattern-vector')
#print len(count(words(Sentence(parse(pageContent))), stemmer=PORTER))
