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


def comm_and_membership(g, aname):
    """
    community detection
    """
    if aname=='greedy':
        comm    = g.community_fastgreedy()
        cluster = comm.as_clustering()
        member  = cluster.membership
    elif aname=='betweenness':
        comm    = g.community_edge_betweenness(directed = False)
        cluster = comm.as_clustering()
        member  = cluster.membership
    elif aname=='infomap':
        comm    = g.community_infomap()
        member  = comm.membership
    elif aname=='louvain':
        comm    = g.community_multilevel()
        member  = comm.membership
    else:
        raise SystemExit(' algorithm not recognized!')

    return comm, member
#EOF
