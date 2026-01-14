from collections import defaultdict, Counter
import csv

input_file = 'edges_d7NoLat.txt'
organism_list = 'human_pdbs.txt'

# Leer lista de nodos de interés
nodos_interes = {}
with open(organism_list, 'r') as f:
    for line in f:
        if line[:-1].split(',')[0] not in nodos_interes:
            nodos_interes[line[:-1].split(',')[0]] = [line[:-1].split(',')[1]]
        else:
            nodos_interes[line[:-1].split(',')[0]].append([line[:-1].split(',')[1]])

print(f"Nodes in the organism list: {len(nodos_interes)}")

for n in nodos_interes:
    print(n,nodos_interes[n])
    break

# Procesar aristas y calcular grados en una sola pasada
grados = Counter()
aristas_filtradas_count = 0

case = input_file.split('.')[0]+'_classes.csv'
with open(case, 'r') as f:
    reader = csv.reader(f)

    for fila in reader:
        if len(fila) >= 2:  # Asegurar que hay al menos dos nodos
            nodo1, nodo2 = fila[0], fila[1]

            # Verificar si al menos un nodo está en la lista de interés
            if nodo1[:-3] in nodos_interes or nodo2[:-3] in nodos_interes:
                aristas_filtradas_count += 1
                grados[nodo1] += 1
                grados[nodo2] += 1

print(f"Edges after filtering: {aristas_filtradas_count}")

# Imprimir resultados
#print("\nDegrees for the nodes (with at least 1 edge):")

salida = open('degreeByNode_'+organism_list.split(.)[0]+'.csv','w')
print("Node,Degree,Uniprot",file=salida)
#print("-" * 15)
for nodo, grado in sorted(grados.items(), key=lambda x: x[1], reverse=True):
    try:
        to_print = ''
        for n in nodos_interes[nodo[:-3]]:
            to_print += n+';'
        print(f"{nodo},{grado},{to_print[:-1]}",file=salida)
    except:
        print(f"{nodo},{grado},notInOrganism",file=salida)
salida.close()

# Estadísticas
print(f"\n--- Estadísticas ---")
print(f"Total of nodes in the subnetwork: {len(grados)}")
if grados:
    print(f"Max degree: {max(grados.values())}")
    print(f"Min degree: {min(grados.values())}")
    print(f"Average degree: {sum(grados.values()) / len(grados):.2f}")
