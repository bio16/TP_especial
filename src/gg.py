#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
"""
script para explorar umbrales inferiores del peso
de los enlaces. La idea el calcular el nro de comunas
q se detectan (con los diferentes algoritmos) y llegar 
a detectar MAS de DOS comunas.
"""
import igraph, os
import numpy as np
import funcs as ff
if 'DISPLAY' in os.environ:
    from pylab import figure, close, hist

# Matriz con las correlaciones entre noticias
corr_matrix = np.load('../data/corr_matrix100.npy')
orig_matrix = corr_matrix.copy() # original

# Devuelvo valores del grafo
#print('Numero de nodos: ', len(graph.vs))
#print('Numero de enlaces: ', len(graph.es))
#print('Grafo dirigido? ', graph.is_directed())
#print('Grafo Pesado? ', graph.is_weighted())


"""
- greedy gives ONE label to ALL!
"""
#--- list of algorithms to try
alist = ('greedy', 'infomap', 'louvain')
#--- list of original weights
#orig_w = [e['weight'] for e in graph.es]
#--- threshold weights
#thrs_w = (0.2, 0.3, 0.6, 0.8)
perc = np.arange(start=45., stop=100., step=3.) # last==stop-step
thrs_w = np.percentile(a=corr_matrix, q=perc)
#import pdb; pdb.set_trace()
import pdb; pdb.set_trace()


mod = {}
nmemb = {}
for thres in thrs_w:
    print('------ thres: ',thres)
    mod[thres] = {}
    nmemb[thres]  = {}
    for aname in alist:
        #for e, i in zip(graph.es, range(len(graph.es))):
        #    # truncate with lower threshold
        #     e['weight'] = 1.0 if orig_w[i]>=thres else 0.0
        for i in range(corr_matrix.shape[0]):
            cc = corr_matrix[i]<thres
            corr_matrix[i][cc] = 0.0
            corr_matrix[i][~cc] = orig_matrix[i][~cc]

        # Cargo el grafo, pesado y no dirigido
        graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)

        comm, memb = ff.comm_and_membership(graph, aname)
        # Modularidad y Silhouette
        mod[thres][aname] = graph.modularity(memb)
        nmemb[thres][aname] = len(set(memb))
        print(' > modularity (%s): '%aname, mod[thres][aname])
        print(' > n_memb: ', len(set(memb)))


#--- figure of number of comms
for aname in alist:
    m = [ mod[thres][aname] for thres in thrs_w ] # list
    nm = [ nmemb[thres][aname] for thres in thrs_w ] # list
    #--- fig (modularity
    fig = figure(1, figsize=(6,4))
    ax  = fig.add_subplot(111)
    ax2 = ax.twinx()
    ax.plot(thrs_w, m, '-ob',label='modularity')
    ax2.plot(thrs_w, nm, '-or',label='N of membership')
    ax.set_xlabel('weight threshold')
    ax.set_ylabel('modularity')
    ax2.set_ylabel('N of membership')
    ax.legend(loc='best')
    ax2.legend(loc='center left')
    ax.grid()
    ax.set_title(aname)
    fig.savefig('fig_%s.png'%aname, dpi=135, bbox_inches='tight')
    close(fig)
    

#print('Silhouette:', ff.silhouette(graph, memb))



#opt = {
#    'vertex_size' : 5,
#    'edge_width'  : 0.5,
#    'opacity' : 0.3,
#}
## Grafo DrL
#layout = graph.layout_drl()
#igraph.plot(graph, layout = layout, target = 'Drl.png', **opt)

#EOF
