#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import igraph
from datetime import datetime, timedelta
import numpy as np
from pylab import plot, figure, close, show, grid
import matplotlib.patches as patches
import matplotlib.transforms as transforms

fname = '../jimmy.gml'
g = igraph.read(fname)

d = {} # counter
for v in g.vs:
    dd, mm, yyyy = map(int, v['date'].split('-'))
    date = datetime(yyyy, mm, dd)
    if date not in d.keys():
        d[date] = 1
    else:
        d[date] += 1

# 
#c     = [d[_nm] for _nm in d.keys()]
dates = np.sort([nm for nm in d.keys()])

#--- array of all dates in the graph
_dates = [] #np.array(g.vs['date'])
for v in g.vs:
    dd, mm, yyyy = map(int, v['date'].split('-'))
    _dates += [datetime(yyyy,mm,dd)]
_dates = np.array(_dates)

"""
we use the normalization for the betweenness:
https://graph-tool.skewed.de/static/doc/centrality.html#graph_tool.centrality.central_point_dominance
"""
nd  = 5 # debe ser impar!
nd2 = (nd-1)/2
clus = np.array(g.vs['clustering'])
# nmbr of days where I'll analyze
ndates = dates[nd2:-nd2].size 
t_days = np.arange(nd2+1, ndates+nd2+1, 1) #----------------
_bet = np.zeros(ndates, dtype=np.float32)
_bet_std = np.zeros(ndates, dtype=np.float32)
_cent = np.zeros(ndates, dtype=np.float32)
for date, i in zip(dates[nd2:-nd2], range(ndates)):
    cc  = _dates>=(date-timedelta(days=nd2))
    cc &= _dates<=(date+timedelta(days=nd2))
    # nodes in this time window
    nodes = cc.nonzero()[0]
    # list of all betweenness centralities
    _bet_ = np.array(g.betweenness())[nodes]
    # difference between the max and min
    _bet_ext = np.max(_bet_) - np.min(_bet_)
    # normalized betweenness
    _bet[i]     = (_bet_.mean() - np.min(_bet_))/_bet_ext
    # error
    _bet_std[i] = _bet_.std()/_bet_ext
    # central dominance
    _cent[i]    = (np.max(_bet_) - _bet_).sum()/(nodes.size-1)
    print(i,ndates)


#--- normalized betweeness
fig = figure(1, figsize=(6,4))
ax  = fig.add_subplot(111)
ax.plot(t_days, _bet, '-ok')

# banda de error
inf     = _bet + _bet_std/np.sqrt(nd)
sup     = _bet - _bet_std/np.sqrt(nd)
ax.fill_between(t_days, inf, sup, facecolor='gray', alpha=0.5)

ax.set_xlabel('nro de dias desde %s'%dates[0].strftime('%d/%B/%Y'))
ax.set_ylabel('<betweenness> (normalizado)')
ax.set_ylim(0.,)
ax.grid(True)
fig.savefig('./betweenness_vs_time.png', dpi=135, bbox_inches='tight')
close(fig)

"""
plot(_cent); show(); close()
"""

#EOF
