import cPickle as pk
from Newspaper import Newspaper
import numpy as np
import codecs

idNotes = np.load('data/idNotes.npy')

news = Newspaper('data/LaNacion.xml')

info_communities = pk.load(file('Communities_infomap.pk','r'))

fp = codecs.open('Comunities_titulos.txt','a','utf8')

for i in range(len(info_communities)):
    fp.write(str(i) + '\n')
    for j in info_communities[i]:
        title = news.getNotebyId(idNotes[int(j)]).title
        fp.write(title + '\n')
    fp.write('\n')

fp.close()
