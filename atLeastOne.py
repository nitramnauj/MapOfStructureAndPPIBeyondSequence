import numpy as np
import pandas as pd
import time

# Configuración
input_file = 'd7NoLatN0.csv'

dir_name = input_file.split('.')[0]
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

output_file = './'+dir_name+'/withatleastone_d7NoLatN0.csv'
threshold = np.cos(np.radians(5))  # Umbral para 5° (~0.9962)
report_interval = 1000  # Mostrar progreso cada 100 hallazgos

# Leer archivo CSV (omitir primera y última columna como etiquetas)
df = pd.read_csv(input_file)
vectors = df.iloc[:, 1:-1].values  # Ignorar primera y última columna
labels = df.iloc[:, [0, -1]].values  # Guardar etiquetas (primera y última columna)

# Normalizar vectores
norms = np.linalg.norm(vectors, axis=1, keepdims=True)
normalized_vectors = vectors / np.where(norms == 0, 1, norms)

# Inicializar estructuras
n = len(normalized_vectors)
print('vectores:',n)
used = np.zeros(n, dtype=bool)  # Marcar vectores ya emparejados
count_found = 0
start_time = time.time()
already_printed = np.zeros(n,dtype=bool)

# Abrir archivo de salida
with open(output_file, 'w') as out_f:
    # Escribir encabezados (opcional)
    #out_f.write("nur used[i] = True\n")

    for i in range(n):
        if used[i]:
            continue  # Saltar vectores ya emparejados

        for j in range(i + 1, n):  # Evitar comparaciones redundantes (i < j)

            # Calcular producto punto absoluto
            dot_product = np.abs(np.dot(normalized_vectors[i], normalized_vectors[j]))
            if dot_product >= threshold:
                # Escribir ambos vectores (formato: índice,etiquetas,vector)
                if not already_printed[i]:
                    out_f.write(f"{labels[i][0]},{','.join(map(str, vectors[i]))},{labels[i][1]}\n")
                    #p1 = labels[i][0].split('/')[-1].split('.')[0]+'_'+labels[i][0].split('/')[-1].split('.')[-1]
                    #p2 = labels[i][1].split('/')[-1].split('.')[0]+'_'+labels[i][1].split('/')[-1].split('.')[-1]
                    #out_f.write(f"{p1},{','.join(map(str, vectors[i]))},{p2}\n")
                    already_printed[i] = True
                    count_found += 1
                if not already_printed[j]:
                    out_f.write(f"{labels[j][0]},{','.join(map(str, vectors[j]))},{labels[j][1]}\n")
                    #p1 = labels[j][0].split('/')[-1].split('.')[0]+'_'+labels[j][0].split('/')[-1].split('.')[-1]
                    #p2 = labels[j][1].split('/')[-1].split('.')[0]+'_'+labels[j][1].split('/')[-1].split('.')[-1]
                    #out_f.write(f"{p1},{','.join(map(str, vectors[i]))},{p2}\n")

                    already_printed[j] = True
                    count_found += 1

                # Marcar como usados
                used[i] = True

                # Reportar progreso
                if count_found % report_interval == 0:
                    elapsed = time.time() - start_time
                    print(f"{count_found},{elapsed:.2f}")
                    start_time = time.time()
                break  # Pasamos al siguiente i

# Resultados finales
total_found = np.sum(used)
elapsed = time.time() - start_time
print(f"\nProceso completado.")
