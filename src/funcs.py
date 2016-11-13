#!/usr/bin/env python
# -*- coding: utf-8 -*-
import igraph
import numpy as np
from pylab import figure, close

# Definicion de silhouette
def silhouette(g, membership):
    silhouette_per_vertex = []
    membership_set = set(membership)

    #--- assign membership labels
    for i in range(len(g.vs)):
        g.vs[i]["membership"] = membership[i]

    for i in range(len(g.vs)):
       average_distance = {}
       for j in range(len(g.vs)):
           try:
               average_distance[g.vs[j]['membership']].append(g.shortest_paths_dijkstra(i,j)[0][0])
           except:
               average_distance[g.vs[j]['membership']] = []
               average_distance[g.vs[j]['membership']].append(g.shortest_paths_dijkstra(i,j)[0][0])

       a = np.mean(average_distance[g.vs[i]['membership']])
       b_list = [np.mean(average_distance[key]) for key in membership_set if key != g.vs[i]['membership']]
       b = min(b_list)

       if (b-a)!=0.0:
           silhouette_per_vertex.append(float(b - a)/max(a,b))
       else:
           silhouette_per_vertex.append(0.00)
        
    return np.mean(silhouette_per_vertex)


def comm_and_membership(g, aname, weighted=True):
    """
    community detection
    """
    #--- build list of weights
    if weighted:
        lw = []
        for e in g.es:
            lw += [ e['weight'] ]
    else:
        lw = [1 for i in range(len(g.es))] # set all links to weight=1
    #---
    if aname=='greedy':
        comm    = g.community_fastgreedy(weights=lw)
        cluster = comm.as_clustering()
        member  = cluster.membership # da 2 comunas!
    elif aname=='betweenness':
        # clusters: the number of clusters we would like to see (i.e. the
        # level where we cut the dendogram)
        comm    = g.community_edge_betweenness(clusters=None, directed=False, weights=lw) # takes very long...
        cluster = comm.as_clustering()
        member  = cluster.membership
    elif aname=='infomap':
        # trials: number of attempts to partition the network
        comm    = g.community_infomap(edge_weights=lw, vertex_weights=None, trials=10)
        member  = comm.membership # gives full zeros
    elif aname=='louvain':
        # return_levels:  if C{True}, the communities at each level are
        # returned in a list.
        comm    = g.community_multilevel(weights=lw, return_levels=False)
        member  = comm.membership # da 2 comunas!
    else:
        raise SystemExit(' algorithm not recognized!')

    return comm, member
#EOF
