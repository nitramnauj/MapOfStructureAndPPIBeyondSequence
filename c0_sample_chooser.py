import pandas as pd
import numpy as np

# Configuración

nombres = ['d5LatN0','d5NoLatN0',
           'd6LatN0','d6NoLatN0',
           'd7LatN0','d7NoLatN0',
           'd8LatN0','d8NoLatN0',
           'd9LatN0','d9NoLatN0']

for name in nombres:
    archivo = name+'.csv'  # Nombre de tu archivo CSV

    # Leer el archivo CSV (ignorando la primera y última columna como etiquetas)
    df = pd.read_csv(archivo)
    datos_numericos = df.iloc[:, 1:-1]  # Excluye primera y última columna
    etiquetas = df.iloc[:, [0, -1]]     # Guarda las etiquetas

    # Calcular y mostrar promedios de todas las columnas
    promedios_totales = datos_numericos.mean()
    #print("\nPromedios de todas las columnas (dataset completo):")
    #print(promedios_totales.to_string())

    # Descomentar las siguientes dos líneas para generar varios tipos de subconjuntos
    #sample_size = np.arange(1000,10500,500)              # Cantidad de vectores (debe ser < N)
    #subsets = np.arange(2000,11000,2000)                 # Número de subconjuntos a generar

    # Si se descomentan las 2 línes anteriores, se deben comentar las 2 siguientes
    # Esto genera 2500 muestras con 2000 vectores cada una
    sample_size = [2000]              # Cantidad de vectores (debe ser < N)
    subsets = [2500]                 # Número de subconjuntos a generar

    salida = open('salida_final_'+name+'.csv','a')
    print('M,S,d',file=salida)
    for M in sample_size:
        for S in subsets:
            promedios = np.zeros(26)
            # Generar S subconjuntos aleatorios de tamaño M
            np.random.seed(42)  # Para reproducibilidad
            for s in range(1, S+1):
                # Seleccionar M filas aleatorias sin reemplazo
                subconjunto = datos_numericos.sample(n=M, replace=False)
    
                # Calcular promedios del subconjunto
                promedios_sub = subconjunto.mean()
                promedios += np.array(promedios_sub)
    
                # Mostrar resultados
                #print(f"\nSubconjunto {s} (M={M} filas aleatorias):")
                #print(promedios_sub.to_string())
        
                # Opcional: Guardar los índices de las filas seleccionadas
                #indices_seleccionados = subconjunto.index
                #print(f"Índices de filas seleccionadas: {indices_seleccionados.values}")
    
            #print("\nPromedios de todas las columnas (dataset completo):")
            #print(np.array(promedios_totales))
            #print("\nPromedios de todas las columnas (dataset muestreo):")
            #print(promedios/S)
            #print("\nDistancia de todas las columnas (dataset muestreo):")

           # Las siguientes líneas reportan qué tanto se aleja la muestra respecto al global
            d = np.linalg.norm(np.array(promedios_totales)-promedios/S)
            print(str(M)+','+str(S)+','+str(d),file=salida)
            print(str(M)+','+str(S)+','+str(d))
    salida.close()

