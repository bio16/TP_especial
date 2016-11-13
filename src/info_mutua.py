#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import igraph, argparse
import numpy as np
import funcs as ff

#--- retrieve args
parser = argparse.ArgumentParser(
formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
'-wth', '--wth',
type=float,
default=0.6,
help='weight threshold',
)
pa = parser.parse_args()

# Matriz con las correlaciones entre noticias
corr_matrix = np.load('../data/corr_matrix100.npy')

# Cargo el grafo, pesado y no dirigido
graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)

# Devuelvo valores del grafo
nv = len(graph.vs)
ne = len(graph.es)
print('Numero de nodos: ', nv)
print('Numero de enlaces: ', ne)
print('Grafo dirigido? ', graph.is_directed())
print('Grafo Pesado? ', graph.is_weighted())

"""
- greedy gives ONE label to ALL!
"""
#--- list of algorithms to try
alist = (('greedy', 'infomap'),
         ('greedy', 'louvain'),
         ('infomap', 'louvain'))
#--- list of original weights
orig_w = [e['weight'] for e in graph.es]
#--- threshold weights
#thrs_w = (0.2, 0.3, 0.6, 0.8)
perc = np.arange(start=45., stop=100., step=3.) # last==stop-step
thrs_w = np.percentile(a=orig_w, q=perc)


mod = {}
nmemb = {}
for aname1, aname2 in alist:
    for e, i in zip(graph.es, range(len(graph.es))):
        # truncate with lower threshold
         e['weight'] = orig_w[i] if orig_w[i]>=pa.wth else 0.0

    #--- 1
    comm, memb1 = ff.comm_and_membership(graph, aname1)
    # Modularidad y Nro de comunas
    mod = graph.modularity(memb1)
    nmemb = len(set(memb1))
    for i in range(nv):
        graph.vs[i]['memb1'] = memb1[i]

    #--- 2
    comm, memb2 = ff.comm_and_membership(graph, aname2)
    # Modularidad y Nro de comunas
    mod = graph.modularity(memb2)
    nmemb = len(set(memb2))
    for i in range(nv):
        graph.vs[i]['memb2'] = memb2[i]

    fp = ff.calc_fprobs(
        graph, 
        np.array(list(set(memb1))), 'memb1', 
        np.array(list(set(memb2))), 'memb2'
    )
    #--- mutual info
    I, Inorm  = ff.information(fp['conj'], fp['memb1'], fp['memb2'])
    print(' Inorm (%s,%s): '%(aname1,aname2), Inorm)


#EOF
