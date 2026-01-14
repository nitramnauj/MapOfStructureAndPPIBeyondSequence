from collections import Counter, defaultdict

# Leer el archivo y contar los grados
input_file = 'edges_d7NoLat.txt'

grados = defaultdict(int)
try:
    with open(input_file, 'r') as archivo:
        for linea in archivo:
            nodos = linea[:-1].split(',')
            if len(nodos) >= 2:
                u, v = nodos[:2]
                grados[u] += 1
                grados[v] += 1
except:
    continue

# Contar la distribución de grados
distribucion = Counter(grados.values())

suma = 0
# Ordenar y mostrar los resultados
salida = open('nodesByDegree_'+input_file.split('.')[0]+'.csv','w')
for grado, cantidad in sorted(distribucion.items()):
    #print(f"Nodos con grado {grado}: {cantidad}")
    print(f"{grado},{cantidad}",file=salida)
    suma += cantidad
salida.close()
print(str(d)+c+'Lat',len(grados),suma)
