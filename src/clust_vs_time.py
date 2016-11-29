#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import igraph
from datetime import datetime, timedelta
import numpy as np
from pylab import plot, figure, close, show, grid

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

#--- 
nd  = 5 # debe ser impar!
nd2 = (nd-1)/2
clus = np.array(g.vs['clustering'])
# nmbr of days where I'll analyze
ndates = dates[nd2:-nd2].size 
_clus = np.zeros(ndates, dtype=np.float32)
for date, i in zip(dates[nd2:-nd2], range(ndates)):
    cc  = _dates>=(date-timedelta(days=nd2))
    cc &= _dates<=(date+timedelta(days=nd2))
    _clus[i] = np.array(g.vs['clustering'])[cc].mean()

t_days = np.arange(nd2+1, ndates+nd2+1, 1)

#---
fig = figure(1, figsize=(6,4))
ax  = fig.add_subplot(111)
ax.plot(t_days, _clus, '-o')

ax.set_xlabel('nro de dias desde %s'%dates[0].strftime('%d/%B/Y'))
ax.set_ylabel('<clustering>')
ax.grid()
fig.savefig('./clus_vs_time.png', dpi=135, bbox_inches='tight')
close(fig)

#EOF
