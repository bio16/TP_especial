import igraph
import random
import numpy as np
from scipy import linalg
import cPickle as pk
from copy import deepcopy

subgraphs = pk.load(file('Subgraphs.pk','r'))

graph = deepcopy(subgraphs[1])

# Matriz pesada
W = np.zeros([len(graph.vs), len(graph.vs)], dtype = np.float)
for es in graph.es:
    W[es.source][es.target] = es['weight']
W = W + np.transpose(W)

# Matriz diagonal con los grados de los nodos
D = np.diag([graph.degree(i) for i in range(len(graph.vs))])
for i in range(len(graph.vs)):
    if graph.degree(i) == 0:
        print i,

D_1 = linalg.inv(D)

print W.shape
print D_1.shape


# Etiquetas de cada nodo, inicialmente todos con el mismo peso
# A definir que etiquetas quiero testear
"""
Etiquetas puestas: 0: Bonafini, 1: Cristina, 2: Macri, 3: Stolbizer
4: Maximo, 5: de Vido, 6: Massa, 7: Carrio.
"""
etiquetas = range(8)

# Y.shape = [n documentos, n etiquetas]
Y = np.ones([len(graph.vs),len(etiquetas)]) * (1.00 / len(etiquetas))

id_notas = [[110, 2, 43],[656],[138],[93],\
           [72,23,24,26],[41,58],[172,10],[60]]

id_nodos = []
for i in id_notas:
    aux = []
    for j in i:
        for k in range(len(graph.vs)):
            if graph.vs[k]['id'] == j:
                aux.append(k)
    id_nodos.append(aux)

def etiquetador_de_fuentes(f_Y, f_id_nodos, f_etiquetas):
    for i in range(len(id_nodos)):
        for j in f_id_nodos[i]:
            f_Y[j] = np.zeros([1, len(f_etiquetas)])
            f_Y[j][i] = 1.00

iterations = 200

# Inicializo las fuentes
etiquetador_de_fuentes(Y, id_nodos, etiquetas)

for i in range(iterations):

    # Hago la multiplicacion de matrices
    # y normalizo
    Y = (D_1.dot(W)).dot(Y)
    for j in range(np.shape(Y)[0]):
        Y[j] = Y[j] / np.sum(Y[j])

    # Reseteo las fuentes
    etiquetador_de_fuentes(Y, id_nodos, etiquetas)

# Lo que obtengo al final es un vector que contiene
# las probabilidad de pertener a una de las clases.    
# Puedo decir que la pertenencia es la clase mas probable
# o si supera cierto umbral

colors = ['blue', 'red', 'yellow', 'green', 'gray', 'white', 'orange', 'violet']
for i in range(len(graph.vs)):
    graph.vs[i]['color'] = colors[int(np.argmax(Y[i]))]
    graph.vs[i]['label'] = str(int(graph.vs[i]['id']))

layout = graph.layout('fruchterman_reingold')
igraph.plot(graph, layout = layout, \
            vertex_label = [vs['label'] for vs in graph.vs])
