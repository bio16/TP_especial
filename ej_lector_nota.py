from Newspaper import Newspaper
import numpy as np

# Cargo identificador de notas
idNotes = np.load('data/idNotes.npy')

# Cargo cuerpo de notas
news = Newspaper('data/LaNacion.xml')

# Quiero ver las notas que en la red aparecen como los nodos 0, 1, 2
number_of_nodes = [5, 8, 73, 96, 112, 135, 186, 430, 487, 523, 539, 603, 649, 695, 726, 727, 799, 808, 825, 928, 1028, 1078]

# Paso el numero de nodo, al id de la nota para identificarlas
id_notes = [idNotes[i] for i in number_of_nodes]

for id_note in id_notes:

    # Obtengo nota por identificador
    note = news.getNotebyId(id_note)

    # Titulo de la nota
    print note.title

    # Subtitulo de la nota
#    print note.subtitle

    # Fecha de la nota
#    print note.date

    # Cuerpo de la nota
    # print note.body

