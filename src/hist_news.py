#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import igraph
from datetime import datetime, timedelta
import numpy as np

#fname = '../news-weighted_0.60-corr_with-dates_with-comms_filtered.graphml'
#fname = '../igraph_news-weighted_0.60-corr_with-dates_with-comms_filtered.graphml'
#fname = '../igraph_news-weighted_0.60-corr_with-dates_with-comms.graphml'
fname = '../jimmy.gml'
#g = igraph.Graph.Read_GraphML(fname)
g = igraph.read(fname)

d = {} # counter
for v in g.vs:
    dd, mm, yyyy = map(int, v['date'].split('-'))
    date = datetime(yyyy, mm, dd)
    if date not in d.keys():
        d[date] = 1
    else:
        d[date] += 1

#---
c = [d[_nm] for _nm in d.keys()]
dates = [nm for nm in d.keys()]

print(np.min(dates), np.max(dates))
print(np.min(c), np.max(c))
print(len(d.keys()))

#EOF
