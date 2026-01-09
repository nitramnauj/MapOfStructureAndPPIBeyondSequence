from collections import defaultdict
import pandas as pd
import numpy as np
import csv

'''
Este código calcula todos los ángulos posibles en una lista de vectores.
Va construyendo un histograma sin "recordar" todos los ángulos,
	pues los va colocando en el bin correspondiente conforme los calcula.
Si el ángulo es menor que 5 grados,
	los considera paralelos y los imprime en un archivo de salida.
'''

# To test, input "d7NoLat,Random" or "d7NoLat,Synthetic"

def calcular_angulo(v1, v2):
	#Calcula el ángulo en grados entre dos vectores usando producto punto.
	dot = np.dot(v1, v2)
	norm_v1 = np.linalg.norm(v1)
	norm_v2 = np.linalg.norm(v2)
	cos_theta = dot / (norm_v1 * norm_v2)
	cos_theta = np.clip(cos_theta, -1.0, 1.0)  # evitar errores numéricos
	return np.degrees(np.arccos(cos_theta))

# Cargar archivo CSV
file_name = input('Input samples ("d9NoLat,Synthetic"):')


name = file_name.split(',')[0]
#kind = 'Random'
kind = file_name.split(',')[1]
samples = [1,2500]

for s in range(samples[0],samples[1]+1):
	if kind == 'Random':
		df = pd.read_csv('Samples_'+kind+'/size'+name+'N0/sample_'+name+'N0_'+str(s)+'.csv')
	else:
		df = pd.read_csv('Samples_'+kind+'/size'+name+'N0/synthetic_'+name+'N0_'+str(s)+'.txt')

	# Detectar número de columnas
	num_cols = df.shape[1]

	# Extraer etiquetas de la primera columna
	etiquetas = df.iloc[:, 0].values

	# Seleccionar las 26 columnas intermedias
	data = df.iloc[:, 1:27].values

	# Crear bins dinámicamente
	bin_size = 2.5
	max_value = 90
	bins = [(i,i+bin_size) for i in range(0,int(max_value),int(bin_size))]
	bins[-1] = (bins[-1][0],max_value) # Aseguramos que el último bin incluya a 90°
	counts = defaultdict(int)

	# Archivo de salida
	with open("Samples_"+kind+"/size"+name+"N0/pars_"+name+"_"+str(s)+".csv", mode="w", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(["etiqueta_A", "etiqueta_B", "angulo_grados"])

		# Calcular todos los pares posibles sin repetición
		n = len(data)
		for i in range(n):
			for j in range(i+1, n):  # asegura que no se repita A con B y B con A
				angulo = calcular_angulo(data[i], data[j])
				# imprimir conforme se calcula
				#print(f"{etiquetas[i]} vs {etiquetas[j]}: {angulo:.2f}°")
				# guardar en archivo de paralelos
				if angulo < 5:
					writer.writerow([etiquetas[i], etiquetas[j], f"{angulo:.2f}"])
				else:
					pass
				if 0 <= angulo <= max_value:
					# Buscamos el índice de bin para colocarlo
					bin_index = int(angulo // bin_size)
					# max_value va en el último bin
					if angulo == max_value:
						bin_index = len(bins) - 1
					counts[bin_index] += 1/(samples[1]-samples[0]+1)
	print('Sample',s,'is ready')


histogram = open('Samples_'+kind+'/histogram_'+kind[0].lower()+kind[1:4]+'_'+name+'_'+str(samples[0])+'_'+str(samples[1])+'.csv','w')
for i, (low, high) in enumerate(bins):
	print(f"{high},{counts[i]}",file=histogram)
histogram.close()
