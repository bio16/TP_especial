#!/usr/bin/env python
# -*- coding: utf-8 -*-


import graph_tool.all as gt
import sys
import os
import os.path

from numpy.random import shuffle
import numpy as np

# We need some Gtk and gobject functions
from gi.repository import Gtk, GObject, Gdk

import argparse as arg
from datetime import date, timedelta
import seaborn as sns
import cairo


argparser = arg.ArgumentParser(description='')
argparser.add_argument('file', help='graph file')
argparser.add_argument('--offscreen', '-of', help='offscreen',
                       action='store_true')
args = argparser.parse_args()

# If True, the frames will be dumped to disk as images.
offscreen = "offscreen" if args.offscreen else False
dir = './frames_dynamic-graph_windowed-10d-comm'
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
state = g.new_vertex_property("int")
order = g.new_vertex_property("int")
for v in g.vertices():
    state[v] = 2
    d, m, y = map(int, g.vp['date'][v].split('-'))
    vdate = date(y, m, d)
    order[v] = (vdate - initial_date).days

# Newly infected nodes will be highlighted in red
mark = g.new_vertex_property("bool")
visited = g.new_vertex_property("bool")
mark.a = False
visited.a = False


# This creates a GTK+ window with the initial graph layout
time = 0
vs = list(g.vertices())
shuffle(vs)
for v in vs:
    if time > order[v]:
        visited[v] = True
        state[v] = 0

    elif time == order[v]:
        visited[v] = True
        mark[v] = True
        state[v] = 1
    else:
        visited[v] = False
# Filter out the recovered vertices
max_time = np.max(list(order))
g.set_vertex_filter(visited)
print('asdasd', g.num_vertices())
#width = gt.prop_to_size(g.ep['weight'], ma=.1)

vsize = g.new_vertex_property("double")
deg = g.degree_property_map("total")
vsize = gt.prop_to_size(g.degree_property_map("total"))
pos = gt.sfdp_layout(g, eweight=g.ep['weight'],
                     groups=g.vp['comm_infomap'],
                     init_step=0.005, max_iter=1)
if not offscreen:
    win = gt.GraphWindow(g, pos, geometry=(500, 400),
                         edge_color=[0.6, 0.6, 0.6, 1],
                         vorder=visited,
                         vertex_size=vsize,
                         vertex_fill_color=state,
                         vertex_halo=mark,
                         vertex_halo_color=[0.8, 0, 0, 0.6])
else:
    win = Gtk.OffscreenWindow()
    win.set_default_size(500, 400)
    win.graph = gt.GraphWidget(g, pos,
                               edge_color=[0.6, 0.6, 0.6, 1],
                               vorder=visited,
                               vertex_size=vsize,
                               vertex_fill_color=state,
                               vertex_halo=mark,
                               vertex_halo_color=[0.8, 0, 0, 0.6])
    win.add(win.graph)

def put_text(pixbuf, text, x, y):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                 pixbuf.get_width(),
                                 pixbuf.get_height())
    context = cairo.Context(surface)

    Gdk.cairo_set_source_pixbuf(context, pixbuf, 0, 0)
    context.paint()         # paint the pixbuf

    # add the text
    fontsize = 20
    context.move_to(x, y+fontsize)
    context.set_font_size(fontsize)
    context.set_source_rgba(0, 0, 0, 1)
    context.show_text(text)

    # get the resulting pixbuf
    surface = context.get_target()
    pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0,
                                         surface.get_width(),
                                         surface.get_height())

    return pixbuf

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
        if time - 5 < order[v] < time + 5:
            visited[v] = True

        elif time == order[v]:
            visited[v] = True
            mark[v] = True
        else:
            visited[v] = False
    # Filter out the recovered vertices
    g.set_vertex_filter(visited)
    size = gt.prop_to_size(g.degree_property_map("total"),ma=10)
    #vsize = gt.prop_to_size(deg)
    nested_state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True)

    level = nested_state.get_levels()[0].get_blocks()
    print(list(level))
    gt.sfdp_layout(g, pos=pos, eweight=g.ep['weight'],
                   groups=level, max_iter=0)
    for v in vs:
        vsize[v] = size[v]
        state[v] = level[v]
    print(g.num_vertices())

    # The following will force the re-drawing of the graph, and issue a
    # re-drawing of the GTK window.
    win.graph.fit_to_window(g=g)
    win.graph.regenerate_surface()
    win.graph.queue_draw()

    # if doing an offscreen animation, dump frame to disk
    time += 1
    if time > max_time:
        sys.exit(0)
    print(time)
    if offscreen:
        pixbuf = win.get_pixbuf()
        strdate = (initial_date+timedelta(days=time)).strftime('%d-%m-%Y')
        pixbuf = put_text(pixbuf, strdate, 0, 10)
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
