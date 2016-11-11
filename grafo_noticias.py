import igraph
import numpy as np

corr_matrix = np.load('corr_matrix100.npy')

graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)

print 'Numero de nodos: ', len(graph.vs)
print 'Numero de enlaces: ', len(graph.es)

print 'Grafo dirigido? ', graph.is_directed()
print 'Grafo Pesado? ', graph.is_weighted()
