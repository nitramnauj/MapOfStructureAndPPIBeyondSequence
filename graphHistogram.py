import matplotlib.pyplot as plt
import numpy as np

distancias = [5,6,7,8,9]
laterales = ['','No']

muestras = ['full','rand','synt']

for d in distancias:
    for s in laterales:
        for m in muestras:
            eje_x = []
            eje_y = []
            if m == 'rand' and s == 'No':
                archivo = open('histogram_'+m+'_d'+str(d)+s+'Lat_1_2500.csv')
            else:
                archivo = open('histogram_'+m+'_d'+str(d)+s+'Lat.csv')
            for line in archivo:
                aux = list(map(float,line[:-1].split(',')))
                eje_x.append(aux[0])
                eje_y.append(aux[1])
            archivo.close()
            eje_x = np.array(eje_x)
            eje_y = np.array(eje_y)
            eje_y = 100*eje_y/sum(eje_y)

            if s == '':
                style = 'solid'
            else:
                style = 'dashed'

            if m == 'full':
                col = 'orange'
            elif m == 'rand':
                col = 'green'
            else:
                col = 'red'
            
            plt.plot(eje_x,eje_y,linestyle=style,color=col)
    plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
    plt.title(f'Angle distribution at {d} $\AA$')
    plt.xlabel('Angle between any 2 cRCC (°)')
    plt.ylabel('Frequency (%)')
    #plt.savefig(f'angleDistribution_d{d}.png')
    plt.show()
    plt.clf()

