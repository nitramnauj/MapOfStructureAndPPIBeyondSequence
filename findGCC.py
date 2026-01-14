import pandas as pd
import networkx as nx

input_file = 'edges_d7NoLat.txt'
case = input_file.split('_')[1].split('.')[0]

df = pd.read_csv(input_file, header=None, names=['nodo1', 'nodo2'])

G = nx.from_pandas_edgelist(df, 'nodo1', 'nodo2')

# Encontrar todos los componentes conexos
componentes = list(nx.connected_components(G))
# Identificar el componente gigante
componente_gigante = max(componentes, key=len)
G_gigante = G.subgraph(componente_gigante).copy()

# Guardar las aristas del componente gigante en un nuevo CSV
aristas_gigante = list(G_gigante.edges())
pd.DataFrame(aristas_gigante, columns=['nodo1', 'nodo2']).to_csv('GCC_'+case+'.csv', index=False)

# Información resumida
print(f"Nodes in the network: {G.number_of_nodes()}")
print(f"Edges in the network: {G.number_of_edges()}")
print(f"Components: {len(componentes)}")
print(f"Nodes in the GCC: {len(componente_gigante)}")
print(f"Edges in the GCC: {G_gigante.number_of_edges()}")
