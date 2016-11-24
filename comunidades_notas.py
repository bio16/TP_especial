import cPickle as pk
from Newspaper import Newspaper
import numpy as np
import codecs

idNotes = np.load('data/idNotes.npy')

news = Newspaper('data/LaNacion.xml')

info_communities = pk.load(file('Communities_infomap.pk','r'))

#fp = codecs.open('Comunities_titulos.txt','w','utf8')
#fp.write('#id (original network) - Community infomap \n')

for i in range(len(info_communities)):
#    fp.write(str(i) + '\n')
    for j in info_communities[i]:
        if int(j) == 176:
            title = news.getNotebyId(idNotes[int(j)]).title
            body = news.getNotebyId(idNotes[int(j)]).body
            print title
            print body
            exit()
#        fp.write(str(int(j)) + ' ' + title + '\n')
#    fp.write('\n')

fp.close()
