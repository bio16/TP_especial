import cPickle as pk
from Newspaper import Newspaper
import numpy as np
import codecs

idNotes = np.load('data/idNotes.npy')

news = Newspaper('data/LaNacion.xml')

info_communities = pk.load(file('Communities_infomap.pk','r'))


def extract_notes(list_nodes):

    for i in range(len(info_communities)):
        for j in info_communities[i]:
            if int(j) in list_nodes:
                title = news.getNotebyId(idNotes[int(j)]).title
                body = news.getNotebyId(idNotes[int(j)]).body
                print title
                print body[:200]
            

