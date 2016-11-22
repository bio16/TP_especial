import igraph
import random
import numpy as np


# Cargo en el objeto graph la red de dolphins.gml.
graph = igraph.read('news-weighted_0.60-corr_with-dates_with-comms.gml')
random.seed(123457)

com = graph.community_infomap()
membership = com.membership

np.save('infomap_membership.npy', membership)

