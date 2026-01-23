import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import os

listOfVectors = 'd7NoLat_benchmark-pdb1.txt'

complejos = {}
with open(listOfVectors) as entrada:
    #next(entrada)
    for line in entrada:
        aux = line[:-1].split('\t')
        complex_name = aux[0][:4]
        chain_name = aux[0][4:]
        #print(complex_name,chain_name)
        #print(aux[1][1:-1])
        cRCC = aux[1][1:-1]
        cRCC = cRCC.split(',')
        cRCC = list(map(int,cRCC))
        #print(len(cRCC))
        
        if complex_name in complejos:
            complejos[complex_name][chain_name] = np.array(cRCC)
        else:
            complejos[complex_name] = {chain_name : np.array(cRCC)}

print(len(complejos))

# Revisar si existe el directorio de salida
dir_name = "PerComplex"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

for cx in complejos:
    if len(complejos[cx]) > 1:
        salida = open('PerComplex/'+cx+'.csv','w')
        for ch in complejos[cx]:
            #print(cx,ch,complejos[cx][ch])
            to_print = cx+'_'+ch
            for i in complejos[cx][ch]:
                to_print += ','+str(i)
            print(to_print,file=salida)
        salida.close()

to_print = ''
for cx in complejos:
    if len(complejos[cx]) > 1:
        to_print += "'"+cx+"',"
#print('['+to_print[:-1]+']')

# Función para calcular ángulo entre dos vectores
def calcular_angulo(v1, v2):
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_theta = np.clip(cos_theta, -1.0, 1.0)  # evitar errores numéricos
    return np.degrees(np.arccos(cos_theta))

# Calcular ángulos entre pares únicos
eje_x = []
eje_y = []
eje_z = []
casos = 0
nulos = 0
con_paralelo = []
for cx in complejos:
    num_pares = 0
    num_paralelos = 0
    num_chain = len(complejos[cx])
    if num_chain == 1:
        continue
    casos += 1
    for (nombre1, v1), (nombre2, v2) in combinations(complejos[cx].items(), 2):
        
        num_pares += 1
        angulo = calcular_angulo(v1, v2)
        if angulo < 5:
            num_paralelos += 1
        #print(f'Ángulo entre {nombre1} y {nombre2}: {angulo:.2f}°')

    print(f'In complex {cx} there are {num_paralelos} semiparallel pairs of {num_pares} possible pairs (with {num_chain} chains).')
    if num_paralelos == 0:
        nulos += 1
    else:
        con_paralelo.append(cx)
    eje_x.append(num_pares)
    eje_y.append(num_paralelos)
    eje_z.append(num_chain)
    #print()

print('Complexes:',casos)
print('Without parallels:',nulos)
#print(con_paralelo)

plt.scatter(eje_x,eje_y)
plt.xlabel('Number of possible pairs per complex')
plt.ylabel('Number of parallel pairs per complex')
plt.xscale('log')
plt.yscale('log')
plt.show()

promedio = 0
promedio_ponderado = 0
for i in range(len(eje_x)):
    if eje_x[i] == 0 or eje_z[i] == 0:
        print(i,eje_x[i])
        print(i,eje_z[i])
        break
    promedio += eje_y[i] / eje_x[i]
    promedio_ponderado += (eje_y[i] / eje_x[i])*eje_z[i]
print(f'Arithmetic mean {promedio/len(complejos)}')
print(f'Weighted arithmetic mean {promedio_ponderado/np.array(eje_z).sum()}')

paralelismo = {}
for i in range(1,50):
    paralelismo[i] = []

promedios_precision = []
varianzas_precision = []
for i in paralelismo:
    for j in range(len(eje_x)):
        if eje_z[j] == i:
            paralelismo[i].append(eje_y[j]/eje_x[j])
    if len(paralelismo[i]) == 0:
        continue
    #print(i)
    promedios_precision.append(np.average(paralelismo[i]))
    varianzas_precision.append(np.var(paralelismo[i]))

promedios_precision = np.array(promedios_precision)
varianzas_precision = np.array(varianzas_precision)

#print(promedios_precision)
#print(varianzas_precision)
pesos = 1/(varianzas_precision+1e-8)
promedio_precision = (pesos*promedios_precision).sum() / pesos.sum()
error = np.sqrt(1/pesos.sum())

#print(f'promedio de precision {promedio_precision}')

plt.scatter(eje_z,eje_x)
plt.show()

from collections import Counter
conteo_x = Counter(eje_y)

# Preparar datos para graficar
valores_x = sorted(conteo_x.keys())
frecuencias = [conteo_x[v] for v in valores_x]

# Graficar
plt.figure(figsize=(10, 6))
plt.bar(valores_x, frecuencias, color='skyblue')
plt.xlabel('Number of parallel pairs in complex')
plt.ylabel('Number of complexes')
#plt.title('Histograma')
plt.grid(True)
plt.yscale('log')
plt.tight_layout()
plt.show()
