import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# Parámetros
# -----------------------------

porcentaje = 1   # usar el % de las líneas del archivo de aristas [0,1]

archivo_aristas = "GCC_d7NoLatN0.txt"
archivo_prefijo1 = "human_pdbs.txt"
archivo_prefijo2 = "musMusculus_pdbs.txt"
archivo_prefijo3 = "sCerevisiae_pdbs.txt"
# -----------------------------

# Función para cargar prefijos
def cargar_prefijos(archivo):
    prefijos = set()
    with open(archivo, "r") as f:
        for linea in f:
            if linea.strip():
                prefijo = linea.strip().split(",")[0]
                prefijos.add(prefijo)
    return prefijos

# Cargar prefijos de los tres archivos
prefijos1 = cargar_prefijos(archivo_prefijo1)
prefijos2 = cargar_prefijos(archivo_prefijo2)
prefijos3 = cargar_prefijos(archivo_prefijo3)

print('Prefijos cargados')

# Leer aristas
with open(archivo_aristas, "r") as f:
    aristas = [linea.strip().split(",") for linea in f if linea.strip()]

# Seleccionar porcentaje de aristas (primeras líneas)
n_total = len(aristas)
print('Aristas leídas:',n_total)
n_usar = int(n_total * porcentaje)
aristas = aristas[:n_usar]
print('Aristas escogidas:',n_usar)

# Crear grafo
G = nx.Graph()
G.add_edges_from(aristas)

print('Red creada')

# Asignar colores a nodos
colores = []
for nodo in G.nodes():
    prefijo = nodo[:4]  # primeros 4 caracteres
    if prefijo in prefijos1:
        colores.append("blue")
    elif prefijo in prefijos2:
        colores.append("red")
    elif prefijo in prefijos3:
        colores.append("green")
    else:
        colores.append("gray")
print('Red coloreada')

# Crear posiciones iniciales por grupo
pos_inicial = {}
for nodo in G.nodes():
    prefijo = nodo[:4]
    if prefijo in prefijos1:
        pos_inicial[nodo] = (0, 10)   # arriba
    elif prefijo in prefijos2:
        pos_inicial[nodo] = (-10, -10) # izquierda abajo
    elif prefijo in prefijos3:
        pos_inicial[nodo] = (10, -10)  # derecha abajo
    else:
        pos_inicial[nodo] = (0, 0)   # centro


# Dibujar grafo
plt.figure(figsize=(20, 20))  # figura grande
pos = nx.spring_layout(G, pos=pos_inicial, seed=42)  # layout de fuerza

nx.draw_networkx_nodes(G, pos,
                       node_color=colores,
                       node_size=1)  # nodos pequeños
nx.draw_networkx_edges(G, pos,
                       width=0.1,     # aristas delgadas
			edge_color='lightgray')	# aristas grises

print('Red dibujada')
# No mostrar etiquetas
plt.axis("off")
plt.savefig('GCC_byOrg_'+str(int(porcentaje*100))+'_v3.png')
print('Red guardada')
