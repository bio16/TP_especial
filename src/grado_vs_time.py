#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import igraph, argparse
from datetime import datetime, timedelta
import numpy as np
from pylab import plot, figure, close, show, grid
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from numpy import power as pow
from numpy import log10

#--- retrieve args
parser = argparse.ArgumentParser(
formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
'-dist', '--dist',
action='store_true',
default=False,
help='whether to build degree-distributions or not.',
)
parser.add_argument(
'-nd', '--ndays',
type=int,
default=5, # has to be odd!!
help='number of days, around which we\'ll take data to analyze.',
)
pa = parser.parse_args()


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
nd  = pa.ndays #5 # debe ser impar!
nd2 = (nd-1)/2
clus = np.array(g.vs['clustering'])
# nmbr of days where I'll analyze
ndates = dates[nd2:-nd2].size 
t_days = np.arange(nd2+1, ndates+nd2+1, 1) #----------------
_grad = np.zeros(ndates, dtype=np.float32)
_grad_err = np.zeros(ndates, dtype=np.float32)

for date, i in zip(dates[nd2:-nd2], range(ndates)):
    cc  = _dates>=(date-timedelta(days=nd2))
    cc &= _dates<=(date+timedelta(days=nd2))
    # nodes in this time window
    nodes = cc.nonzero()[0]
    # solo los grados en esta ventana temporal
    _grad_ = np.array(g.degree(vertices=nodes))
    _grad[i]     = _grad_.mean()
    _grad_err[i] = _grad_.std()
    if pa.dist:
        #--- histogram
        hc, hx_ = np.histogram(_grad_, bins=20, normed=True)
        hx = 0.5*(hx_[:-1] + hx_[1:])
        fig = figure(1, figsize=(6,4))
        ax  = fig.add_subplot(111)
        ax.plot(hx, hc, 'ok', label='N:%d'%nodes.size)
        # linear fit
        _cc = hc>0.
        m, b = np.polyfit(np.log10(hx[_cc]), np.log10(hc[_cc]), deg=1)
        plot(hx, pow(10.,m*log10(hx)+b), '--r', alpha=0.6, lw=3, label='$\\alpha:$ %.1f'%m)

        ax.grid(True)
        ax.set_xlabel('grado'); ax.set_ylabel('PDF')
        ax.set_title(
        'nro de dias: %d'%nd+'\n'+\
        't: '+date.strftime('%d/%B/%Y')
        )
        ax.set_xscale('log'); ax.set_yscale('log')
        ax.set_xlim(1.,1e3); ax.set_ylim(1e-4, 1.)
        ax.legend(loc='best')
        fig.savefig('./degree_distrib/hist_%02d.png'%i, dpi=135, bbox_inches='tight')
        close(fig)
        #-------------
    print(i,ndates)

#--- normalized betweeness
fig = figure(1, figsize=(6,4))
ax  = fig.add_subplot(111)
ax.plot(t_days, _grad, '-ok')

# banda de error
inf     = _grad + _grad_err/np.sqrt(nd)
sup     = _grad - _grad_err/np.sqrt(nd)
ax.fill_between(t_days, inf, sup, facecolor='gray', alpha=0.5)

ax.set_xlabel('nro de dias desde %s'%dates[0].strftime('%d/%B/%Y'))
ax.set_ylabel('<grado>')
ax.set_ylim(0.,)
ax.grid(True)
fig.savefig('./grado_vs_time_ndays.%02d.png'%pa.ndays, dpi=135, bbox_inches='tight')
close(fig)


#EOF
