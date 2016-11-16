#!/bin/env python3
import igraph
import numpy as np
import argparse as arg

argparser = arg.ArgumentParser(description='')
argparser.add_argument('adj_matrix',help='adj matrix in npy format')
argparser.add_argument('name',help='graph name')
argparser.add_argument('--threshold','-t', default=0, type=float)
argparser.add_argument('--binner','-b', action='store_true',help='simple graph or weighted (default:weighted)')
argparser.add_argument('--format','-f', default='gml',help='format (default:gml)')
args = argparser.parse_args()

# Matriz con las correlaciones entre noticias
corr_matrix = np.load(args.adj_matrix)
def f(matrix):
    IMAX,JMAX = matrix.shape
    for i in range(IMAX):
        for j in range(JMAX):
            if matrix[i,j] < args.threshold:
                matrix[i,j] = 0
            else:
                if args.binner:
                    matrix[i,j] = 1
    return matrix
corr_matrix = f(corr_matrix)

if args.binner:
    graph = igraph.Graph.Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX)
    graph = graph.simplify(loops=True,multiple=True)
else:
# Cargo el grafo, pesado y no dirigido
    graph = igraph.Graph.Weighted_Adjacency(list(corr_matrix), mode = igraph.ADJ_MAX, loops = False)


# Devuelvo valores del grafo
print( 'Numero de nodos: ', len(graph.vs))
print( 'Numero de enlaces: ', len(graph.es))
print( 'Grafo dirigido? ', graph.is_directed())
print( 'Grafo Pesado? ', graph.is_weighted())

type = 'simple' if args.binner else 'weighted'
graph.write_gml('./gml/%s-%s_threshold-%.3f.%s'%(args.name,type,args.threshold,args.format))
