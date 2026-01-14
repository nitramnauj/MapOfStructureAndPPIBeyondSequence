input_file = 'edges_d7NoLat.txt'

# Cargar diccionario de clases
clases = {}
full_database = input_file.split('_')[1].split('.')[0]+'N0.csv'
with open(full_database) as f:
    reader = csv.reader(f)
    for row in reader:
        nodo = row[0]
        clase = row[-1]
        clases[nodo] = clase

# Procesar aristas y añadir clases
with open(input_file) as fin, open(input_file.split('.')[0]+'_classes.csv', 'w', newline='') as fout:
    reader = csv.reader(fin)
    writer = csv.writer(fout)
    for nodo1, nodo2 in reader:
        clase1 = clases.get(nodo1, 'NA')
        clase2 = clases.get(nodo2, 'NA')
        writer.writerow([nodo1, nodo2, clase1, clase2])


import networkx as nx
import matplotlib.pyplot as plt

# Parámetros ajustables
figsize = (12, 12)
node_size = 10
edge_width = 0.5

# Colores por clase
color_map = {'1': 'blue', '2': 'red', '3': 'purple', '4': 'yellow', '6': 'green'}

# Construir red
G = nx.Graph()
with open(input_file.split('.')[0]+'_classes.csv') as f:
    for line in f:
        nodo1, nodo2, clase1, clase2 = line.strip().split(',')
        G.add_node(nodo1, clase=clase1)
        G.add_node(nodo2, clase=clase2)
        G.add_edge(nodo1, nodo2)

# Asignar colores
colors = [color_map.get(G.nodes[n]['clase'], 'gray') for n in G.nodes]

# Dibujar
plt.figure(figsize=figsize)
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, node_color=colors, node_size=node_size, width=edge_width, with_labels=False)
#plt.show()
plt.savefig(input_file.split('_')[1].split('.')[0]+"_plot.png")
