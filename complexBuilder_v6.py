import csv
import numpy as np
import itertools
import time
import random
import os
import pandas as pd

def leer_vectores(archivo):
    # Read vectors from a csv file
    vectores = {}
    with open(archivo, 'r') as f:
        lector = csv.reader(f)
        for fila in lector:
            etiqueta = fila[0]
            vector = np.array([float(x) for x in fila[1:]])
            vectores[etiqueta] = vector
    return vectores

def calcular_angulo(v1, v2):
    # Calculates the angle between two vectors, in degrees
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0
    
    coseno = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    coseno = np.clip(coseno, -1.0, 1.0)
    return np.degrees(np.arccos(coseno))

def encontrar_trayectoria_completa(vectores, archivo_salida, angulo_umbral=5, max_combinacion=5, tiempo_limite_minutos=30):
    # Find trajectories of sums considering sums of multiple vectors with a time limit
    etiquetas = list(vectores.keys())
    mejor_trayectoria = []
    mejor_longitud = 0
    solucion_completa = False
    tiempo_inicio = time.time()
    tiempo_limite_segundos = tiempo_limite_minutos * 60
    semillas_probadadas = set()
    
    archivo_salida.write(f"Time limit per seed: {tiempo_limite_minutos} minutes\n")
    archivo_salida.write(f"Total of vectors/seeds: {len(etiquetas)}\n\n")
    archivo_salida.flush()
    
    def backtrack(trayectoria_actual, suma_actual, disponibles, profundidad=0):
        nonlocal mejor_trayectoria, mejor_longitud, solucion_completa
        
        # If there is already a complet solution, stop all threads
        if solucion_completa:
            return
        
        # Check if the running time exceeds the time limit.
        if time.time() - tiempo_inicio_semilla > tiempo_limite_segundos:
            archivo_salida.write(f"  [TIME EXCEEDED] Stoping current seed after {tiempo_limite_minutos} minutes\n")
            archivo_salida.flush()
            return True
        
        indentacion = "  " * profundidad
        archivo_salida.write(f"{indentacion}Level {profundidad}: Current trajectory: {trayectoria_actual}\n")
        archivo_salida.write(f"{indentacion}Available vectors: {disponibles}\n")
        archivo_salida.flush()
        

        # Update the best trajectory currently found
        num_vectores = len(trayectoria_actual)
        if num_vectores > mejor_longitud:
            mejor_trayectoria = trayectoria_actual.copy()
            mejor_longitud = num_vectores
            archivo_salida.write(f"{indentacion}*** New best trajectory: {mejor_trayectoria} (length: {mejor_longitud})\n")
            archivo_salida.flush()
        
        # If there are no more available vectors, we finish and mark the solution as completed
        if not disponibles or (len(vectores)-len(disponibles))/len(vectores) >= 0.95:
            archivo_salida.write(f"{indentacion}FULL SOLUTION! There are no more available vectors\n")
            archivo_salida.flush()
            solucion_completa = True
            return
        
        # Try first with individual vectors (k=1)
        encontrado = False
        angulos_calculados = []
        
        for i, etiqueta in enumerate(disponibles):
            # Check if there is already a complete solution
            if solucion_completa:
                return
            
            # Check time
            if time.time() - tiempo_inicio_semilla > tiempo_limite_segundos:
                archivo_salida.write(f"{indentacion}  [TIME EXCEEDED] Stoping search...\n")
                archivo_salida.flush()
                return True
                
            vector = vectores[etiqueta]
            angulo = calcular_angulo(suma_actual, vector)
            angulos_calculados.append((etiqueta, angulo))
            
            archivo_salida.write(f"{indentacion}  Angle between current sum and {etiqueta}: {angulo:.2f}°\n")
            archivo_salida.flush()
            
            if angulo < angulo_umbral:
                encontrado = True
                archivo_salida.write(f"{indentacion}  *** {etiqueta} satisfies condition (angle < {angulo_umbral}°)\n")
                archivo_salida.flush()
                
                # Sum that vector and continue
                nueva_suma = suma_actual + vector
                nueva_trayectoria = trayectoria_actual + [f"{etiqueta} (angle: {angulo:.2f}°)"]
                nuevos_disponibles = disponibles[:i] + disponibles[i+1:]
                
                interrumpido = backtrack(nueva_trayectoria, nueva_suma, nuevos_disponibles, profundidad + 1)
                if interrumpido:
                    return True
                
                # If we find a complete solution, stop search
                if solucion_completa:
                    return
        
        # Show calculated angles for k=1
        if angulos_calculados and not solucion_completa:
            min_angulo = min(angulos_calculados, key=lambda x: x[1])
            archivo_salida.write(f"{indentacion}For k=1: Minimum found angle = {min_angulo[1]:.2f}° with {min_angulo[0]}\n")
            archivo_salida.flush()
        
        # If there have been no individual vector, try with combination of more vectors
        k = 2
        while not encontrado and k <= min(max_combinacion, len(disponibles)) and not solucion_completa:
            # Check time
            if time.time() - tiempo_inicio_semilla > tiempo_limite_segundos:
                archivo_salida.write(f"{indentacion}  [TIME EXCEEDED] Stoping search\n")
                archivo_salida.flush()
                return True
                
            archivo_salida.write(f"{indentacion}  -> There are no individual vectors. Trying with combinations of {k} vectors...\n")
            archivo_salida.flush()
            
            # Try all combinations of k available vectors
            combinaciones_probadadas = 0
            combinaciones_validas = 0
            
            for combinacion in itertools.combinations(disponibles, k):
                # Check if there is already a complete solution
                if solucion_completa:
                    return
                    
                # Check time
                if time.time() - tiempo_inicio_semilla > tiempo_limite_segundos:
                    archivo_salida.write(f"{indentacion}    [TIME EXCEEDED] Stoping search...\n")
                    archivo_salida.flush()
                    return True
                
                # Calculate the sum of k vectors
                vector_suma = sum(vectores[etiq] for etiq in combinacion)
                angulo = calcular_angulo(suma_actual, vector_suma)
                combinaciones_probadadas += 1
                
                etiquetas_combinacion = "+".join(combinacion)
                archivo_salida.write(f"{indentacion}    Angle between current sum and {etiquetas_combinacion}: {angulo:.2f}°\n")
                archivo_salida.flush()
                
                if angulo < angulo_umbral:
                    combinaciones_validas += 1
                    archivo_salida.write(f"{indentacion}    *** COMBINATION {etiquetas_combinacion} satisfies condition (angle < {angulo_umbral}°)\n")
                    archivo_salida.flush()
                    
                    # Sum those k vectors and continue
                    nueva_suma = suma_actual + vector_suma
                    nueva_trayectoria = trayectoria_actual + [
                        f"COMBINATION: {etiquetas_combinacion} (angle: {angulo:.2f}°)"
                    ]
                    nuevos_disponibles = [et for et in disponibles if et not in combinacion]
                    
                    interrumpido = backtrack(nueva_trayectoria, nueva_suma, nuevos_disponibles, profundidad + 1)
                    if interrumpido:
                        return True
            
            archivo_salida.write(f"{indentacion}  For k={k}: {combinaciones_validas}/{combinaciones_probadadas} combinations satisfied condition\n")
            archivo_salida.flush()
            
            if combinaciones_validas > 0:
                encontrado = True
            else:
                k += 1
        
        # If there is not already a valid combination after trying all possible k vectors
        if not encontrado and not solucion_completa:
            archivo_salida.write(f"{indentacion}  -> Backtrack: no combination of maximum {min(max_combinacion, len(disponibles))} vectors satisfied condition\n")
            archivo_salida.flush()
        
        return False
    
    # Test seeds in random order until find a complete solution or exhaust all options
    tiempo_total_inicio = time.time()
    
    while len(semillas_probadadas) < len(etiquetas) and not solucion_completa:
        # Select a random seed (not tested yet)
        semillas_no_probadadas = [et for et in etiquetas if et not in semillas_probadadas]
        if not semillas_no_probadadas:
            break
            
        etiqueta_inicial = random.choice(semillas_no_probadadas)
        semillas_probadadas.add(etiqueta_inicial)
        
        archivo_salida.write(f"\n{'='*60}\n")
        archivo_salida.write(f"Starting with seed: {etiqueta_inicial} (Seed {len(semillas_probadadas)}/{len(etiquetas)})\n")
        archivo_salida.write(f"Tested seeds: {sorted(semillas_probadadas)}\n")
        archivo_salida.write(f"{'='*60}\n")
        archivo_salida.flush()
        
        # Restart time for this seed
        tiempo_inicio_semilla = time.time()
        disponibles = [et for et in etiquetas if et != etiqueta_inicial]
        
        # Run backtracking for this seed
        interrumpido = backtrack([etiqueta_inicial], vectores[etiqueta_inicial], disponibles, 0)
        
        # If there is stop due time, continue with next seed
        if interrumpido:
            archivo_salida.write(f"\n[STOPED] Time exceeded for seed {etiqueta_inicial}. Continuing with next seed...\n")
            archivo_salida.flush()
            continue
        
        # If there is a complete solution, stop script
        if solucion_completa:
            archivo_salida.write(f"\n[COMPLETE SOLUTION] Found with seed {etiqueta_inicial}\n")
            archivo_salida.flush()
            break
    
    tiempo_total = time.time() - tiempo_total_inicio
    archivo_salida.write(f"\nTotal running time: {tiempo_total/60:.2f} minutes\n")
    archivo_salida.write(f"Tested seeds: {len(semillas_probadadas)}/{len(etiquetas)}\n")
    
    return mejor_trayectoria

def reconstruir_suma_final(vectores, trayectoria):
    # Rebuild the final sum from the trajectory
    if not trayectoria:
        return np.zeros_like(next(iter(vectores.values()))), []
    
    # Extract the original labels from the path
    etiquetas_usadas = []
    for paso in trayectoria:
        # Search single labels
        if "COMBINATION:" not in paso and "SUM:" not in paso:
            etiqueta = paso.split(" ")[0]  # Extract the label before the first space character
            etiquetas_usadas.append(etiqueta)
        else:
            # For combinations, extract the labels with the format "COMBINATION: A+B+C"
            if "COMBINATION:" in paso:
                partes = paso.split(": ")[1].split(" ")[0]  # Get "A+B+C"
            else: 
                partes = paso.split(": ")[1].split(" ")[0]  # Get "A+B"
            etiquetas_combinacion = partes.split("+")
            etiquetas_usadas.extend(etiquetas_combinacion)
    
    # Calculate the final sum
    suma = np.zeros_like(next(iter(vectores.values())))
    for etiqueta in etiquetas_usadas:
        suma += vectores[etiqueta]
    
    return suma, etiquetas_usadas

def main(archivo_csv):
    archivo_salida = directorio+'/pathway_'+archivo_csv.split('.')[0]+'.txt'

    # Open output file
    with open(archivo_salida, 'w', encoding='utf-8') as f:

        f.write("=== ANALYSIS OF VECTOR TRAJECTORIES ===\n\n")
        
        # Reed vectors
        vectores = leer_vectores(directorio+'/'+archivo_csv)
        
        f.write(f"Original vectors: {list(vectores.keys())}\n")
        f.write(f"Number of vectors: {len(vectores)}\n")
        
        # Set parameters
        angulo_umbral = 5    # Threshold angle
        max_combinacion = 6  # Maximum number of vectors to combine
        tiempo_limite_minutos = 15  # 15 minutes per seed
        
        f.write(f"Threshold angle: {angulo_umbral}°\n")
        f.write(f"Test maximum combination: {max_combinacion} vectors\n")
        f.write(f"Time limit per seed: {tiempo_limite_minutos} minutes\n")
        f.write(f"Estimated total maximum time: {len(vectores) * tiempo_limite_minutos / 60:.1f} hours\n\n")
        
        # Find the longest trajectory of sums
        f.write("Searching trajectories...\n")
        f.flush()
        
        trayectoria = encontrar_trayectoria_completa(
            vectores, f, angulo_umbral, max_combinacion, tiempo_limite_minutos
        )
        
        f.write(f"\n{'='*60}\n")
        f.write(f"=== FINAL RESULT ===\n")
        f.write(f"{'='*60}\n")
        
        if trayectoria:
            suma_final, etiquetas_usadas = reconstruir_suma_final(vectores, trayectoria)
            
            f.write(f"Found trajectory:\n")
            for i, paso in enumerate(trayectoria):
                f.write(f"  Step {i+1}: {paso}\n")
            
            f.write(f"\nLength of the trajectory: {len(trayectoria)} steps\n")
            f.write(f"Used vectors: {etiquetas_usadas}\n")
            f.write(f"Number of used vectors: {len(etiquetas_usadas)}\n")
            f.write(f"Value of the final sum: {np.linalg.norm(suma_final):.4f}\n")
            
            if len(etiquetas_usadas) == len(vectores):
                #f.write("\n¡SE ENCONTRÓ UNA TRAYECTORIA COMPLETA!\n")
                f.write("THERE IS A FULL TRAJECTORY! "+archivo_csv.split('.')[0]+' with '+str(len(vectores))+' chains.\n')
                print("THERE IS A FULL TRAJECTORY!",archivo_csv.split('.')[0],'with',len(vectores),'chains.')

            else:
                f.write(f"\nNote: Only {len(etiquetas_usadas)} of {len(vectores)} vectors could be included\n")
        else:
            f.write("No valid path was found\n")
    
    #print(f"Proceso completado. Resultados guardados en {archivo_salida}")


# Path to the directory where the CSV files are located
directorio = './PorComplejo'  # Adjust if your files are in another location
todos_los_archivos = os.listdir(directorio)

# Filter those that end in ".csv"
archivos = [f for f in todos_los_archivos if f.endswith('.csv')]

#print(archivos[0])

archivos = ['2qhl.csv']

for a in archivos:
    df = pd.read_csv(directorio+'/'+a,header=None)
    if len(df)==1:
        #print('solo 1 vector',a)
        continue
    else:
        main(a)
