import igraph
import numpy as np

# Matriz con las correlaciones entre noticias
corr_matrix = np.load('corr_matrix100.npy')

# Cargo el grafo, pesado y no dirigido
graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)

# Devuelvo valores del grafo
print('Numero de nodos: ', len(graph.vs))
print('Numero de enlaces: ', len(graph.es))
print('Grafo dirigido? ', graph.is_directed())
print('Grafo Pesado? ', graph.is_weighted())

opt = {
    'vertex_size' : 5,
    'edge_width'  : 0.5,
    'opacity' : 0.3,
}

"""
# Grafo Fruchterman - Reingold
layout = graph.layout_fruchterman_reingold()
igraph.plot(graph, layout = layout, target = 'FrutRein.png')

# Grafo Kamada Kawai
layout = graph.layout_kamada_kawai()
igraph.plot(graph, layout = layout, target = 'KamKaw.png')
"""
# Grafo DrL
layout = graph.layout_drl()
igraph.plot(graph, layout = layout, target = 'Drl.png', **opt)

# Layouts que NO nos da una buena visualización

## Grafo Random
#layout = graph.layout_random()
#igraph.plot(graph, layout = layout, target = 'Random.png')
#
## Grafo Multidimensional Scaling
#layout = graph.layout_mds()
#igraph.plot(graph, layout = layout, target = 'Multi.png')
#EOF
