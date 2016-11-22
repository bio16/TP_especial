import igraph
import random
import numpy as np

# Cargo en el objeto graph la red de dolphins.gml.
graph = igraph.read('news-weighted_0.60-corr_with-dates_with-comms.gml')

random.seed(123457)

com = graph.community_infomap()
membership = com.membership

print graph.modularity(membership)

# Matriz pesada
W = np.zeros([len(graph.vs), len(graph.vs)], dtype = np.float)
for es in graph.es:
    W[es.source][es.target] = es['weight']
W = W + np.transpose(W)

# Matriz diagonal con los grados de los nodos
D = np.diag([graph.degree(i) for i in range(len(graph.vs))])
D_1 = linalg.inv(D)

# Etiquetas de cada nodo, inicialmente todos con el mismo peso
# A definir que etiquetas quiero testear

# Y.shape = [n documentos, n etiquetas]
Y = np.ones([len(graph.vs),len(etiquetas)]) * (1.00 / len(etiquetas))

# Elijo que documentos quiero etiquetar
# Ej: Y[0] = [1, 0, 0, 0, ...]

print D_1.shape
print W.shape
print Y.shape

iterations = 20

for i in range(iterations):

    # Hago la multiplicacion de matrices
    # y normalizo
    Y = (D_1.dot(W)).dot(Y)
    for j in range(np.shape(Y)[0]):
        Y[j] = Y[j] / np.sum(Y[j])

    # Reseteo las fuentes
    #Y[0] = [1, 0, 0, 0, ..., 0]

# Lo que obtengo al final es un vector que contiene
# las probabilidad de pertener a una de las clases.    
# Puedo decir que la pertenencia es la clase mas probable
# si supera cierto umbral

print Y
 
