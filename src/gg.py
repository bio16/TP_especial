#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import igraph
import numpy as np
import funcs as ff

# Matriz con las correlaciones entre noticias
corr_matrix = np.load('../data/corr_matrix100.npy')

# Cargo el grafo, pesado y no dirigido
graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)

# Devuelvo valores del grafo
print('Numero de nodos: ', len(graph.vs))
print('Numero de enlaces: ', len(graph.es))
print('Grafo dirigido? ', graph.is_directed())
print('Grafo Pesado? ', graph.is_weighted())

"""
- greedy gives ONE label to ALL!
"""
comm, memb = ff.comm_and_membership(graph, 'betweenness')
import pdb; pdb.set_trace()

# Modularidad y Silhouette
print('Fast greedy modularity:', graph.modularity(memb))
print('Silhouette:', ff.silhouette(graph, memb))



#opt = {
#    'vertex_size' : 5,
#    'edge_width'  : 0.5,
#    'opacity' : 0.3,
#}
## Grafo DrL
#layout = graph.layout_drl()
#igraph.plot(graph, layout = layout, target = 'Drl.png', **opt)

#EOF
