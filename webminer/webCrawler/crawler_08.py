import random
import networkx as nx
from pattern.web import URL
   
class MEGA:
    def __init__(self,G):
        self.GRAPHS=G
        self.MEGA=nx.DiGraph()

    def get(self):
        clouds=dict()
        unaNube=list()
        c=0
        for cloud in self.GRAPHS:
            c+=1
            clouds[c]=[cloud.nodes(),cloud.edges()]
        c=0
        ide=0
        for x in clouds:
            c+=1
            unaNube=clouds[c]
            nodos=unaNube[0]
            aristas=unaNube[1]
            for n in nodos:
                ide+=1
                self.MEGA.add_node(n,weight=0.0,ID=ide,link=n,methodData=None)
            for e in aristas:
                self.MEGA.add_edge(e[0],e[1])
        return self.MEGA.nodes()
        #nx.draw(MEGA,node_size=300,alpha=0.8,node_color='yellow')
    
    def ruleta(self,rango):
        a=0
        b=0
        valores=list()
        while a==b:#Evita bucle hacia el mismo nodo
            a=random.randint(0,rango)
            b=random.randint(0,rango)
        valores.append(a)
        valores.append(b)
        return valores
    
    def generate(self,mega_nodos,enlaces):
        rango=len(mega_nodos)-1
        print 'RANGO:',rango
        url_a=URL('http://www.mega.com/page.html')
        url_b=URL('http://www.mega.com/page.html')
        e=1
        while e<=enlaces:
            while url_a.domain==url_b.domain:# Evita que se generen enlaces hacia nodos de la misma nube
                sorteo=self.ruleta(rango)
                linkFrom=mega_nodos[sorteo[0]]
                link=mega_nodos[sorteo[1]]  
                url_a=URL(linkFrom)
                url_b=URL(link)
            url_a=URL('http://www.mega.com/page.html')#url de inicializacion, es ficticia
            url_b=URL('http://www.mega.com/page.html')#url de inicializacion, es ficticia
            self.MEGA.add_edge(linkFrom,link)
            print linkFrom,' ',link
            e+=1
        #nx.draw(self.MEGA,node_size=300,alpha=0.8,node_color='yellow')
        return self.MEGA
    
    def PrintInfo(self,nodo=None):
        print
        print 'Cantidad de nodos:',len(self.MEGA.nodes())
        print 'Cantidad de enlaces:',len(self.MEGA.edges())
        if nodo!=None:
            print "Predecesores de",nodo,":",self.MEGA.predecessors(nodo)
            print "Sucesores de",":",self.MEGA.successors(nodo)
