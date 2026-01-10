import pandas as pd
import numpy as np
import random
import csv
import os

input_name = "d7NoLatN0.csv"

# Revisar si existe el directorio de salida
dir_name = "Angles"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

def calcular_angulo(v1, v2):
    """Calcula el ángulo en grados entre dos vectores usando producto punto."""
    dot = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot / (norm_v1 * norm_v2)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)  # evitar errores numéricos
    return np.degrees(np.arccos(cos_theta))

# Cargar archivo CSV
df = pd.read_csv(input_name)

# Extraer etiquetas de la primera columna
etiquetas = df.iloc[:, 0].values

# Tomar solo las columnas intermedias (ignorando primera y última que son etiquetas)
data = df.iloc[:, 1:-1].values # Estos son los vectores de todo el archivo
n = len(data)

def seleccionar_pares_y_angulos(num_pares, archivo_salida="Angles/pares_angulos.csv"):
    vistos = set()  # para registrar pares ya usados
    
    with open(archivo_salida, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["vector_A", "vector_B", "angulo_grados"])
        
        count = 0
        while count < num_pares:
            i, j = random.sample(range(n), 2)  # dos índices distintos
            par = tuple(sorted((i, j)))       # ordenado para evitar duplicados inversos
            
            if par in vistos:
                continue  # ya calculado, saltar
            
            vistos.add(par)
            angulo = calcular_angulo(data[i], data[j]) # Aquí calculamos el ángulo entre los vectores
            
            # imprimir conforme se calcula
            #print(f"Par ({i}, {j}) -> {etiquetas[i]} vs {etiquetas[j]}: {angulo:.2f}°")
            
            # guardar en archivo
            writer.writerow([etiquetas[i], etiquetas[j], f"{angulo:.2f}"])
            count += 1

import time
muestra_size = [1,9,10,11] # Esto calcula 10, 10^9, 10^10 y 10^11 angulos
muestra_size = [11] # Esto calcula 10, 10^9, 10^10 y 10^11 angulos
for i in muestra_size:
    begin = time.time()
    seleccionar_pares_y_angulos(10**i,archivo_salida="Angles/"+input_name.split('.')[0]+"_angulos_"+str(i)+".csv")
    end = time.time()
    print(f"{end-begin:.6f} seconds")
