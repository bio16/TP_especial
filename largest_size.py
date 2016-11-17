import igraph
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import random

# Matriz con las correlaciones entre noticias
corr_matrix = np.load('data/corr_matrix100.npy')

# Cargo el grafo, pesado y no dirigido
graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)

# Devuelvo valores del grafo
print('Numero de nodos: ', len(graph.vs))
print('Numero de enlaces: ', len(graph.es))
print('Grafo dirigido? ', graph.is_directed())
print('Grafo Pesado? ', graph.is_weighted())


size_max_component = []
for threshold in np.linspace(0.50, 1.00, 41):

    adjacency_matrix = deepcopy(corr_matrix)

    for i in range(adjacency_matrix.shape[0]):
        for j in range(adjacency_matrix.shape[1]):
            if adjacency_matrix[i][j] > threshold:
                adjacency_matrix[i][j] = 1
            else:
                adjacency_matrix[i][j] = 0

    # Cargo el grafo, pesado y no dirigido
    graph = igraph.Graph.Adjacency(list(adjacency_matrix), mode = igraph.ADJ_MAX)

    graph_aux = graph.clusters()
    size_max_component.append(max(graph_aux.sizes()))
    

plt.figure(1)
plt.plot(np.linspace(0.50, 1.00, 41), size_max_component, '.-')
plt.xlabel('Umbral')
plt.ylabel('Componente mas grande')
plt.grid('on')
plt.savefig('Componente_mas_grande.png')



adjacency_matrix = deepcopy(corr_matrix)
threshold = 0.80

for i in range(adjacency_matrix.shape[0]):
    for j in range(adjacency_matrix.shape[1]):
        if adjacency_matrix[i][j] < threshold:
            adjacency_matrix[i][j] = 0

# Cargo el grafo, pesado y no dirigido
graph = igraph.Graph.Weighted_Adjacency(list(adjacency_matrix), mode = igraph.ADJ_MAX, loops = False)

weights = [es['weight'] for es in graph.es]

random.seed(123457)
com = graph.community_fastgreedy(weights)
clust = com.as_clustering()

modularity = []
nrange = []

for n in range(1, 1191):

    try:
        clustering = com.as_clustering(n = n)
        membership = clustering.membership
        modularity.append(graph.modularity(membership))
        nrange.append(n)
    except: 
        pass

plt.figure(2)
plt.plot(nrange, modularity,'.-')
plt.ylabel('Modularidad')
plt.xlabel('Numero de comunas')
plt.title('Optimo: 147 comunas')
plt.grid('on')
plt.show()

"""
plt.savefig('Modularidad_umbral08.png')
"""
# Analizo comunas
clustering = com.as_clustering()
membership = clustering.membership

print graph.modularity(membership)

for i in range(len(membership)):
    if membership[i] == 1:
        print i,

