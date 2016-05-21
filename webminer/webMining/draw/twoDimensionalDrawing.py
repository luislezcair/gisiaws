import networkx as nx

class DrawCloud():
    def __init__(self):
        pass
    
    def assignColor(self,color):
        if color==0:
            return 'cyan'
        elif color==1:
            return 'lime'
        elif color==2:
            return 'yellow'
        elif color==3:
            return 'red'
        elif color==4:
            return 'blue'
        elif color==5:
            return 'orange'
        elif color==6:
            return 'pink'
        elif color==7:
            return 'black'
        elif color==8:
            return 'violet'
        elif color==9:
            return 'grey'
        elif color==10:
            return 'purple'
        elif color==11:
            return 'brown'
        elif color==12:
            return 'green'
        elif color==13:
            return 'silver'
        else:
            return 'white'
    
    def plotFunction(self,clouds):
        c=0
        for cloud in clouds:
            nx.draw(cloud.graph,node_size=300,alpha=0.8,node_color=self.assignColor(c))
            c+=1
    