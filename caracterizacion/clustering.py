#!/bin/env python3

from graph_tool.all import * 
import argparse as arg
import numpy as np

argparser = arg.ArgumentParser(description='')
argparser.add_argument('file',help='graph file')
args = argparser.parse_args()



g = load_graph(args.file,fmt='gml')

clustering = extended_clustering(g, undirected=True)

#for i,deep in enumerate(clustering):
    
deep1 = list(clustering[0])
filename = 'clustering/clustering_' + '.'.join(args.file.split('/')[-1].split('.')[:-1]) +'.txt'
np.savetxt( filename, deep1)
