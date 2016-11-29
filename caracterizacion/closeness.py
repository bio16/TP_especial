#!/bin/env python3

import graph_tool.all as gt
import argparse as arg
import matplotlib
import pandas as pd

# seccion de argumentos del programa

argparser = arg.ArgumentParser(description='')
argparser.add_argument('file', help='graph file')

args = argparser.parse_args()

g = gt.load_graph(args.file)
g = gt.GraphView(g, vfilt=gt.label_largest_component(g), directed=False)
g = gt.Graph(g, prune=True)


# chequea que todo sea como "debe ser"
print('chequeando...', args.file)
print('vertices', g.num_vertices())   # numero de vertices
print('edges', g.num_edges())         # numero de links

weight = g.ep['weight']
width = gt.prop_to_size(weight, ma=.5)


# seteo de algunas argumentos de la creacion del grafo

pos = g.vp['pos_sfdp_infomap']

vcl = gt.closeness(g, weight=weight)
vsize = gt.prop_to_size(vcl)
vorder = -vsize.a

df = pd.DataFrame({'node': list(g.vertices()), 'closeness': list(vcl)})
df.sort_values(by='closeness', inplace=True, ascending=False)
print(df.head(15))

print('drawing...')
# dibuja el grafico en el archivo filename.png
gt.graph_draw(g, pos,
              output_size=(500, 400),
              vertex_size=vsize,
              vertex_fill_color=vsize,
#              vorder=vorder,
              vcmap=matplotlib.cm.gist_heat,
#              edge_color=ebet,
              edge_pen_width=width,
              output=r'./closeness.png')
