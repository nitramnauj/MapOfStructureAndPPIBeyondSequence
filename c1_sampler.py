import pandas as pd
import numpy as np

# Configuración
# Los valores M y S deben coincidir con los de c0_sample_chooser.py

nombres = ['d5LatN0','d5NoLatN0',
           'd6LatN0','d6NoLatN0',
           'd7LatN0','d7NoLatN0',
           'd8LatN0','d8NoLatN0',
           'd9LatN0','d9NoLatN0']

for name in nombres:

    df = pd.read_csv(name+'.csv')
    datos_numericos = df.iloc[:, 1:-1]  # Excluye primera y última columna
    df["SUM"] = datos_numericos.sum(axis=1)

    M = 2000              # Cantidad de vectores (debe ser < N)
    S = 2500                 # Número de subconjuntos a generar
    np.random.seed(42)  # Para reproducibilidad
    output_averages = open('Samples_Random/size'+name+'/averages_'+name+'.csv','w')
    to_print = 'FILE,av_RCC1,av_RCC2,av_RCC3,av_RCC4,av_RCC5,av_RCC6,av_RCC7,av_RCC8,av_RCC9,av_RCC10,av_RCC11,av_RCC12,av_RCC13,'
    to_print += 'av_RCC14,av_RCC15,av_RCC16,av_RCC17,av_RCC18,av_RCC19,av_RCC20,av_RCC21,av_RCC22,av_RCC23,av_RCC24,av_RCC25,av_RCC26,'
    to_print += 'sd_RCC1,sd_RCC2,sd_RCC3,sd_RCC4,sd_RCC5,sd_RCC6,sd_RCC7,sd_RCC8,sd_RCC9,sd_RCC10,sd_RCC11,sd_RCC12,sd_RCC13,'
    to_print += 'sd_RCC14,sd_RCC15,sd_RCC16,sd_RCC17,sd_RCC18,sd_RCC19,sd_RCC20,sd_RCC21,sd_RCC22,sd_RCC23,sd_RCC24,sd_RCC25,sd_RCC26'
    print(to_print,file=output_averages)
    for s in range(1, S+1):
        # Seleccionar M filas aleatorias sin reemplazo
        subconjunto = datos_numericos.sample(n=M, replace=False)
        promedio = subconjunto.mean().values
        desviacion = subconjunto.std().values
        print('sample_'+name+'_'+str(s)+','+','.join(map(str,promedio))+','+','.join(map(str,desviacion)),file=output_averages)
    
        # Mostrar resultados
        #print(f"\nSubconjunto {s} (M={M} filas aleatorias):")

        indices_seleccionados = subconjunto.index
        output_subset = open('Samples_Random/size'+name+'/sample_'+name+'_'+str(s)+'.csv','w')
        print('PDBID,RCC1,RCC2,RCC3,RCC4,RCC5,RCC6,RCC7,RCC8,RCC9,RCC10,RCC11,RCC12,RCC13,RCC14,RCC15,RCC16,RCC17,RCC18,RCC19,RCC20,RCC21,RCC22,RCC23,RCC24,RCC25,RCC26,C,SUM',file=output_subset)
        for i in indices_seleccionados:
            print(','.join(map(str,df.loc[i].values)),file=output_subset)
        output_subset.close()
    output_averages.close()

