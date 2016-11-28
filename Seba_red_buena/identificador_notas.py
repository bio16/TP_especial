import igraph
from Newspaper import Newspaper
import numpy as np
import codecs

graph = igraph.read('news-weighted_0.60-corr_with-dates_with-comms_filtered.gml')

idNotes = np.load('data/idNotes.npy')
news = Newspaper('data/LaNacion.xml')

fp = codecs.open('Notas.txt','w','utf-8')
fp.write('# id network \t title \n')
for comm in range(100):
    fp.write('# Community' + str(comm) + '\n')
    for i in range(len(graph.vs)):
        if int(graph.vs[i]['comm_infomap']) == comm:
            note = news.getNotebyId(int(idNotes[int(graph.vs[i]['id'])]))
            fp.write(str(i) + '\t' + note.title + '\n')
fp.close()            
    

    




