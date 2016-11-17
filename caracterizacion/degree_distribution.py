#!/usr/bin/env python3

import igraph
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import argparse as arg

fig,subplot = plt.subplots(ncols=1,nrows=1)

argparser = arg.ArgumentParser(description='')
argparser.add_argument('file',help='graph file')
 
args = argparser.parse_args()

g = igraph.read(args.file,format='gml')

grados = g.indegree()

hist, bins = np.histogram(grados, density=True)
centers = .5*(bins[:-1]+bins[1:])

#inv_hist = 1/hist
res = igraph.power_law_fit(hist)

subplot.plot(centers,hist, 'o')
#subplot.plot(centers, res.alpha*centers )

sns.distplot(grados,kde=False, ax=subplot, norm_hist=True, bins=bins)

subplot.set_xlabel('grado')
subplot.set_ylabel('densidad')

subplot.set_xscale('log')
subplot.set_yscale('log')


filename = args.file.split('/')[-1]
plt.savefig('degree_distribution/'+filename+'.png')
plt.show()


