import Data_manager.dbdatahandler as dh
from Preprocessing import textpreprocessing as tpp
import cluster_metric as cm

jobs = dh.getjobswithtext(1000)

testi=[]
titles=[]
for t in jobs:
    testi.append(t['testo'])
    titles.append(t['jobtitle'])

print len(jobs)

#testotoken = tpp.filter(testo)
#testoclean = tpp.stopwordremoval(testotoken)
#testostem = tpp.stemming(testoclean)

#print testostem
#testi= [testostem,testostem,testostem,testostem]

numcl=10
matrix = cm.tfidfmatrix(testi)
clusters = cm.tfidfkmeans(matrix,numcl)

#print clusters

for c in range(0,numcl):

    print "################\ncluster ",c,"\n ##############"
    for i in range(0,len(clusters)):
        if clusters[i]==c:
            print titles[i]

