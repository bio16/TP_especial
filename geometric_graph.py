import igraph
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import random

# Matriz con las correlaciones entre noticias
corr_matrix = np.load('data/dist_matrix100.npy')

corr_matrix = np.max(corr_matrix) - corr_matrix

# Cargo el grafo, pesado y no dirigido
graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)


# Devuelvo valores del grafo
print('Numero de nodos: ', len(graph.vs))
print('Numero de enlaces: ', len(graph.es))
print('Grafo dirigido? ', graph.is_directed())
print('Grafo Pesado? ', graph.is_weighted())

weights = [es['weight'] for es in graph.es]

com = graph.community_fastgreedy(weights)
clust = com.as_clustering()
membership = clust.membership
print graph.modularity(membership)

exit()

size_max_component = []
for threshold in np.linspace(0.00, 10.00, 21):

    adjacency_matrix = deepcopy(corr_matrix)

    for i in range(adjacency_matrix.shape[0]):
        for j in range(adjacency_matrix.shape[1]):
            if adjacency_matrix[i][j] < threshold:
                adjacency_matrix[i][j] = 1
            else:
                adjacency_matrix[i][j] = 0

    # Cargo el grafo, pesado y no dirigido
    graph = igraph.Graph.Adjacency(list(adjacency_matrix), mode = igraph.ADJ_MAX)

    graph_aux = graph.clusters()
    size_max_component.append(max(graph_aux.sizes()))
    


plt.plot(np.linspace(0.00, 10.00, 21), size_max_component, '.-')
plt.xlabel('Umbral')
plt.ylabel('Componente mas grande')
plt.grid('on')
plt.show()
