#!/usr/bin/env python
# -*- coding: utf-8 -*-


import graph_tool.all as gt
import sys
import os
import os.path

from numpy.random import shuffle
import numpy as np

# We need some Gtk and gobject functions
from gi.repository import Gtk, GObject

import argparse as arg
from datetime import date
import seaborn as sns


argparser = arg.ArgumentParser(description='')
argparser.add_argument('file', help='graph file')
argparser.add_argument('--offscreen', '-of', help='offscreen',
                       action='store_true')
args = argparser.parse_args()

# If True, the frames will be dumped to disk as images.
offscreen = "offscreen" if args.offscreen else False
dir = './frames_static-graph'
if offscreen and not os.path.exists(dir):
    os.mkdir(dir)

# load the graph
g = gt.load_graph(args.file)
g = gt.GraphView(g, vfilt=gt.label_largest_component(g), directed=False)
g = gt.Graph(g, prune=True)
pos = g.vp["pos_sfdp_infomap"]  # layout positions

# find the initial and final date
id, im, iy = map(int, (g.gp['initial-date'].split('-')))
fd, fm, fy = map(int, (g.gp['final-date'].split('-')))
initial_date = date(iy, im, id)
final_date = date(fy, fm, fd)

# set the posible state of each vertex
future = sns.xkcd_rgb['grey']
present = sns.xkcd_rgb['yellow']
past = sns.xkcd_rgb['brick red']

# Initialize all vertices to the _future_ state
state = g.new_vertex_property("string")
order = g.new_vertex_property("int")
for v in g.vertices():
    state[v] = future
    d, m, y = map(int, g.vp['date'][v].split('-'))
    vdate = date(y, m, d)
    order[v] = (vdate - initial_date).days

# Newly infected nodes will be highlighted in red
mark = g.new_vertex_property("bool")
visited = g.new_vertex_property("bool")
mark.a = False
visited.a = False


# This creates a GTK+ window with the initial graph layout
time = -1
max_time = np.max(list(order))
width = gt.prop_to_size(g.ep['weight'], ma=.1)
if not offscreen:
    win = gt.GraphWindow(g, pos, geometry=(500, 400),
                         edge_color=[0.6, 0.6, 0.6, 1],
                         vorder=visited,
                         vertex_fill_color=state,
                         vertex_halo=mark,
                         vertex_halo_color=[0.8, 0, 0, 0.6])
    print('asdasd', g.num_vertices())
else:
    win = Gtk.OffscreenWindow()
    win.set_default_size(500, 400)
    win.graph = gt.GraphWidget(g, pos,
                               edge_color=[0.6, 0.6, 0.6, 1],
                               vorder=visited,
                               vertex_fill_color=state,
                               vertex_halo=mark,
                               vertex_halo_color=[0.8, 0, 0, 0.6])
    win.add(win.graph)


# This function will be called repeatedly by the GTK+ main loop, and we use it
# to update the state according to the dynamics.
def update_state():
    global time
    mark.a = False
    visited.a = False
    g.set_vertex_filter(None)

    # visit the nodes in random order
    vs = list(g.vertices())
    shuffle(vs)
    for v in vs:
        if time > order[v]:
            visited[v] = True
            state[v] = past

        elif time == order[v]:
            visited[v] = True
            mark[v] = True
            state[v] = present
        else:
            visited[v] = False
    # Filter out the recovered vertices
    g.set_vertex_filter(visited)
    print(g.num_vertices())

    # The following will force the re-drawing of the graph, and issue a
    # re-drawing of the GTK window.
    win.graph.regenerate_surface(reset=True)
    win.graph.queue_draw()

    # if doing an offscreen animation, dump frame to disk
    time += 1
    if time > max_time:
        sys.exit(0)
    print(time)
    if offscreen:
        pixbuf = win.get_pixbuf()
        pixbuf.savev(dir + '/news-date_%06d.png' % time, 'png', [], [])

    # We need to return True so that the main loop will call this function more
    # than once.
    print('-'*80)
    return True


# Bind the function above as an 'idle' callback.
cid = GObject.idle_add(update_state)

# We will give the user the ability to stop the program by closing the window.
win.connect("delete_event", Gtk.main_quit)

# Actually show the window, and start the main loop.
win.show_all()
Gtk.main()
