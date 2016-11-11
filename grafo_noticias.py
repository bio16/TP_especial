import igraph
import numpy as np

# Matriz con las correlaciones entre noticias
corr_matrix = np.load('corr_matrix100.npy')

# Cargo el grafo, pesado y no dirigido
graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)

# Devuelvo valores del grafo
print 'Numero de nodos: ', len(graph.vs)
print 'Numero de enlaces: ', len(graph.es)
print 'Grafo dirigido? ', graph.is_directed()
print 'Grafo Pesado? ', graph.is_weighted()
