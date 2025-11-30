import pandas as pd

# Cargar el archivo CSV

distances = [5,6,7,8,9]
condition = ['','No']

for d in distances:
    for c in condition:
        name = 'd'+str(d)+c+'LatN0.csv'
        df = pd.read_csv(name)

        # Seleccionar todas las columnas excepto la primera y la última
        data = df.iloc[:, 1:-1]

        # Calcular promedio y desviación estándar
        resultados = pd.DataFrame({
                    'Promedio': data.mean(),
                    'Desviacion_Estandar': data.std()
                    })

        # Mostrar resultados
        print(resultados)

        # Si quieres guardar los resultados en un nuevo CSV:
        resultados.to_csv('values_d'+str(d)+c+'Lat.csv')
