#!/usr/bin/env python3

import graph_tool.all as gt
import numpy as np
import argparse as arg

argparser = arg.ArgumentParser(description='')
argparser.add_argument('file',help='graph file')
argparser.add_argument('--overlap',action='store_true')
argparser.add_argument('--plot',action='store_true')

args = argparser.parse_args()

g = gt.load_graph(args.file)

weight = g.ep['weight'] if 'weight' in g.ep.keys() else None

nested_state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True, overlap=args.overlap)

levels = nested_state.get_levels()
partitions = [np.array( list(level.get_blocks()) ) for level in levels]

filename = 'communities_mcmc_'+'.'.join(args.file.split('/')[-1].split('.')[:-1])+ '_hierarchy'
if args.overlap:
    filename += '-overlap'


np.save('./partitions/'+filename+'_partition-level-0.npy', partitions[0])
np.save('./partitions/'+filename+'_partition-level-1.npy', partitions[1])

if args.plot:
    nested_state.draw(output='./schemes/'+filename+".pdf")
    pos = gt.sfdp_layout(g,eweight=weight,groups=levels[0].get_blocks() )
    deg = graph.degree_property_map("total",weight=graph.ep['weight'])
    deg_size = prop_to_size(deg, mi=.1,ma=2)
    levels[0].draw(pos=pos, vertex_size=deg_size, output= './schemes/'+filename+"_partition-level-0.pdf")
    levels[1].draw(output= './schemes/'+filename+"_partition-level-1.pdf")
