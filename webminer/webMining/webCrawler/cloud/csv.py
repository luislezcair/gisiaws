import csv, operator

class Prueba:
    def __init__(self):
        pass
    def gen(self):
        csvNodes=open('nodes.csv','w')
        csvEdges=open('edges.csv','w')
        csvNodes=csv.writer(csvNodes,delimiter=';')
        csvEdges=csv.writer(csvEdges,delimiter=';')
        print('Escribiendo archivo "salida.csv"...')
        csvNodes.writerow(['Label','Id','Weight'])
        csvEdges.writerow(['Source','Target','Type'])
#obj=Prueba()
#obj.gen()

class Ccsv:
    def __init__(self):
        pass
    
    def gen(self,minePackage):
        clouds=minePackage['clouds']
        csvNodes=open('nodes.csv','w')
        csvEdges=open('edges.csv','w')
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
                nod=cloud.graph.node[n]
                succ=nod.successors(cloud.graph.node[n]['link'])
                for s in succ:
                    source=nod['ID']
                    target=cloud.graph.node[s]['ID']
                    csvEdges.writerow([source,target,'Directed'])




'''
with open('datos.csv') as csvarchivo:
    entrada = csv.DictReader(csvarchivo)
    csvsalida = open('salida.csv', 'w')
    salida = csv.writer(csvsalida, delimiter=';')
    print('Escribiendo archivo "salida.csv"...')
    print('Dialecto:', entrada.dialect, '...')
    salida.writerow(['NOMBRE','CONSUMO'])
    for reg in entrada:
        salida.writerow([reg['nombre'], reg['consumo']])  # Escribir registro en archivo

    print('El proceso de escritura ha terminado.')

del entrada, salida, reg
csvsalida.close()
del csvsalida
'''
