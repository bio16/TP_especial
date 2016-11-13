#!/usr/bin/env python
# -*- coding: utf-8 -*-
import igraph
import numpy as np
from pylab import figure, close, hist

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

def calc_fprobs(g, set1, name1, set2, name2):
    """
    - g:
    graph
    - seti {numpy.array, 1D}:
    set of labels
    - namei {string}:
    keyname to identify the label of each node, using
    the g.vs[namei]
    """
    # frequentist probability
    fprob = np.zeros(shape=(set1.size,set2.size), dtype=np.float)
    # let's sample both labels && accumulate into `fprob`
    for v in g.vs:
        # catch the set1-index 
        i1 = (v[name1]==set1).nonzero()[0][0]
        # catch the set2-index 
        i2 = (v[name2]==set2).nonzero()[0][0]
        fprob[i1,i2] += 1.0
    # normalize 
    fprob /= fprob.sum()

    # return conj && marginates
    fp = {
    'conj' : fprob,
    name1  : np.sum(fprob, axis=1),
    name2  : np.sum(fprob, axis=0),
    }
    return fp

def information(p12, p1, p2):
    """
    we are using:
    I({C1},{C2}) = \sum_{C1,C2} P(C1,C2) * log(P(C1,C2)/(P(C1)*P(C2)))
    Inorm = 2*I({C1},{C2}) / (H1+H2),
    where:
    H1 = -\sum_i p1[i]*log(p1[i])
    H2 = -\sum_i p2[i]*log(p2[i])
    -- Output: 
    returns `I` and `Inorm`
    """
    # log term
    log_pp = np.log(p12) - np.log(np.outer(p1,p2))
    # information values
    p1_, p2_ = p1[p1>0], p2[p2>0] # filter-out zeros
    # the norm factor is a sum of two entropies (H1 and H2)
    norm_factor = -dot(p1_, log(p1_)) + -dot(p2_, log(p2_))
    I = 0.0 # total mutual information
    for i_s in range(p12.shape[0]):
        for i_m in range(p12.shape[1]):
            #NOTE: contribute to sum only if (joint) probability is >0.0
            I += p12[i_s,i_m]*log_pp[i_s,i_m] if p12[i_s,i_m]>0.0 else 0.0

    return I, (2.*I/norm_factor)

#EOF
