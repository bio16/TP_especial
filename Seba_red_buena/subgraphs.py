import igraph
import cPickle as pk
from copy import deepcopy

subgraphs = pk.load(file('Subgraphs_new.pk','r'))

i = 2
for subgraph in subgraphs[2:]:
    layout = subgraph.layout('auto')
    igraph.plot(subgraph, layout = layout, vertex_size = 25, vertex_label_size = 12, target = 'Community' + str(i) + '.png')
    i += 1
"""
graph = deepcopy(subgraphs[1])

degrees = [{'id':vs['id'], 'degree':graph.degree(vs)} for vs in graph.vs]
degrees = sorted(degrees, reverse = True, key = lambda x: x['degree'])
for degree in degrees:
    print degree

weights = [es['weight'] for es in graph.es]
comm = graph.community_infomap(edge_weights = weights)
membership = comm.membership

print set(membership)
"""
