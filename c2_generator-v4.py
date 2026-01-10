# Quinto código para ejecturar
import numpy as np
import pandas as pd
import os

averages = ['d5LatN0','d5NoLatN0',
            'd6LatN0','d6NoLatN0',
            'd7LatN0','d7NoLatN0',
            'd8LatN0','d8NoLatN0',
            'd9LatN0','d9NoLatN0']

averages = ['d7NoLatN0']

M = 2000 # Population
S = 2500 # Samples

# Crear directorios de salida
dir_name = "Samples_Synthetic"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

poblacion = M
muestras = S

def curva(ne,c):
    a = c[0]
    m = c[1]
    s = c[2]
    binomio = (ne-m)**2
    frac = binomio/(2*s**2)
    return a*np.exp(-frac)

def rccModel(me,ajuste):
    c1 = ajuste[0]
    c2 = ajuste[1]
    c3 = ajuste[2]
    c4 = ajuste[3]
    return curva(me,c1)+curva(me,c2)+curva(me,c3)+curva(me,c4)

def rccGenerator(rcc,ajustes,valor,incertidumbre):
    random = np.random.normal(0,incertidumbre)
    if random > 0:
        val = np.rint(rccModel(rcc,ajustes)+random)
    else:
        #val = np.rint(-1*random)
        val = 0
    return int(val)

def massiveGenerator(case,elementos,fln,average_data,curve_settings):
    output = open('Samples_Synthetic/size'+case+'/synthetic_'+case+'_'+str(fln)+'.txt','w')
    print('SYNTH_ID,RCC1,RCC2,RCC3,RCC4,RCC5,RCC6,RCC7,RCC8,RCC9,RCC10,RCC11,RCC12,RCC13,RCC14,RCC15,RCC16,RCC17,RCC18,RCC19,RCC20,RCC21,RCC22,RCC23,RCC24,RCC25,RCC26,C',file=output)
    sumsFile = 'Samples_Random/size'+case+'/sample_'+case+'_'+str(fln)+'.csv'
    
    valores = average_data[:26]
    errores = average_data[26:]

    sumes_file = pd.read_csv(sumsFile)
    condition_sums = sumes_file.iloc[:,-1].tolist()
    condition_class = sumes_file.iloc[:,-2].tolist()
    pdb_names = sumes_file.iloc[:,0].tolist()
    rccs = np.arange(1,27,1)
    for q in range(elementos):
        rcc = []
        condition = int(condition_sums[q])
        structure = int(condition_class[q])
        synth_name = 'synth_'+pdb_names[q]
        t = 0
        for x in range(len(rccs)):
            rcc.append(rccGenerator(x+1,curve_settings,valores[x],errores[x]))
        rcc = np.array(rcc)
        while np.sum(rcc) == 0:
            rcc = []
            for x in range(len(rccs)):
                rcc.append(rccGenerator(x+1,curve_settings,valores[x],errores[x]))
            rcc = np.array(rcc)
        w = 0
        while np.sum(rcc) not in range(int(condition*0.8),int(condition*1.2)) and w == 0:
            mult = np.sum(rcc)/condition
            try:
                rcc = list(map(int,rcc/mult))
            except:
                rcc = np.array(rcc)
                w = 1
            '''
            rcc = []
            for x in range(len(rccs)):
                rcc.append(rccGenerator(x+1,ajustes,valores[x],errores[x]))
            '''
            t += 1
            if t == 10000:
                #print(np.sum(rcc))
#                print(case+'sub'+str(fln),q,condition)
                texto = str(np.sum(rcc))
#                print(list(rcc))

                rcc = np.array(rcc)
#                print(rcc)
                w = 1
        while np.sum(rcc) == 0:
            rcc = []
            for x in range(len(rccs)):
                rcc.append(rccGenerator(x+1,curve_settings,valores[x],errores[x]))
            rcc = np.array(rcc)

        #print(rcc,' en ', 'random'+case+'sub'+str(fln))
        rcc = list(rcc)

        extra1 = np.random.randint(0,26)
        rcc[extra1] += 1
        extra2 = np.random.randint(0,26)
        while extra2 == extra1:
            extra2 = np.random.randint(0,26)
        if rcc[extra2] > 0:
            rcc[extra2] -= 1
        rcc.append(structure)


        # Here the random vector is printed in 'sim_af_d7Lat_N.txt'
        #line_to_print = 'af_'+case+str(fln)+'{:06x}' #.format(fln*elements+count)
        #for r in range(26):
        #    line_to_print += ','+str(rcc[r])
        #print(line_to_print.format(fln*elementos+q),file=output)

        print(synth_name+','+','.join(map(str,rcc)),file=output)
        #print(q,rcc)
        output.flush()
    output.close()
    sumes_file.close()

    return rcc

#log = open('log.txt','w')
for name in range(len(averages)):
    dir_name = 'Samples_Synthetic/size'+averages[name]
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    curvesFile = 'curvesFrom'+averages[name]+'.txt'
    file = open(curvesFile, 'r')
    ajustes = []
    for line in file:
        aux = line.split(',')
        aux = list(map(float,aux))
        ajustes.append(aux)
    file.close()
    
    rccAverageFile = 'Samples_Random/size'+averages[name]+'/averages_'+averages[name]+'.csv'
    df_averages = pd.read_csv(rccAverageFile)
    #log.flush()
    for fl in range(muestras):
        try:
            average_values = df_averages[df_averages.iloc[:,0] == 'sample_'+averages[name]+'_'+str(fl+1)].iloc[0,1:].tolist()
            vector = massiveGenerator(averages[name],poblacion,fl+1,average_values,ajustes)
            #print(averages[name]+'sub'+str(fl))
            #texto = averages[name]+'sub'+str(fl)
            #log.write(texto+'\n')
        except:
            pass
    print('samples '+averages[name]+' listo')

#log.close()

