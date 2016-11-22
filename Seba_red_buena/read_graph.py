import igraph
import random

# Cargo en el objeto graph la red de dolphins.gml.
graph = igraph.read('red_060.gml')

random.seed(123457)

com = graph.community_infomap()
membership = com.membership

print graph.modularity(membership)

for i in range(len(graph.vs)):
    graph.vs['infomap_membership'] = membership[i]

fp = file('red_con_infomap.gml','a')
graph.write_gml(fp)
fp.close()
