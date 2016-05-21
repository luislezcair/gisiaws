import pickle

path="/home/matt/clusterProject/webMining/clouds/"
fileName=path+"index.p"
pickle.dump({}, open(fileName, "wb" ))