import numpy as np
import pandas as pd
from itertools import combinations
import time

input_file = 'd7NoLatN0/semiparalalelos_d7NoLatN0.csv'
output_file  = 'edges_d7NoLat.txt'

# Cargar el archivo CSV (ignorando la primera y última columna como etiquetas)
df = pd.read_csv(input_file,header=None)
vectors = df.iloc[:, 1:-1].values  # Excluir primera y última columna
labels = df.iloc[:, [0, -1]].values  # Guardar etiquetas

# Normalizar los vectores (para eficiencia)
norms = np.linalg.norm(vectors, axis=1, keepdims=True)
normalized_vectors = vectors / np.where(norms == 0, 1, norms)  # Evitar división por cero

# Comparar vectores sin repeticiones
try:
    with open(output_file) as f:
        lineas = f.readlines()
    print(len(lineas))
    final_pair = lineas[-1].split(',')
    if final_pair[1][-1] == '\n':
        final_pair[1] = final_pair[1][:-1]
    final_pair = [final_pair[0],final_pair[1]]
    print(final_pair)
    seguir = False
    calculate = False
except:
    final_pair = ['x','y']
    seguir = True
    calculate = True


# Umbral de paralelismo (cos(5°))
threshold = np.cos(np.radians(5))  # ~0.9962
count_found = 0
start_time = time.time()
report_interval = 250000  # Mostrar progreso cada 250000 hallazgos
for i in range(len(normalized_vectors)):
    if labels[i][0] in final_pair:
        seguir = True
    if seguir:
        for j in range(len(normalized_vectors)):
            if labels[i][0] in final_pair and labels[j][0] in final_pair:
                calculate = True
            if calculate:
                dot_product = np.abs(np.dot(normalized_vectors[i], normalized_vectors[j]))
                if dot_product >= threshold:
                    salida = open(output_file,'a')
                    if dot_product > 1:
                        dot_product = 1
                    print(labels[i][0]+','+labels[j][0],file=salida)
                    salida.close()

                    count_found += 1
                    if count_found % report_interval == 0:
                        elapsed = time.time() - start_time
                        print(f"{count_found},{elapsed:.2f}")
                        start_time = time.time()
