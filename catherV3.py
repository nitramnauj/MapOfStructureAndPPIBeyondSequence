
name = 'edges_d7NoLat.txt'

nodes = {}
gigante = open(name,'r')
for l in gigante:
    #print('')
    aux = l.split(',')
    nodes[aux[0]] = None
    nodes[aux[1][:-1]] = None
gigante.close()

cathList = open('cath-domain-list.txt','r')
#caths = []
count = 0

alfas = 0
betas = 0
alfabetas = 0
pocas = 0
especiales = 0

clases = {}
arquitecturas = {}
topologias = {}
homologias = {}

p = 0
dominios = open('dom_'+name,'w')
for l in cathList:
    if '#-' in l:
        count += 1
    if count == 2:
        aux = list(l)
        if aux[0] != '#':
            info = ''
            for k in range(len(aux)):
                if aux[k] != ' ':
                    if aux[k-1] == ' ':
                        info += ','+aux[k]
                    else:
                        info += aux[k]
                else:
                    pass
            #print(info)
            info = info.split(',')
            #print(info)
            #info = info[:-7]
            if info[0] in nodes:
                p += 1
                #print(p,info[0])
                if int(info[1]) == 1:
                    alfas += 1
                if int(info[1]) == 2:
                    betas += 1
                if int(info[1]) == 3:
                    alfabetas += 1
                if int(info[1]) == 4:
                    pocas += 1
                if int(info[1]) == 6:
                    especiales += 1
                if info[1] not in clases:
                   clases[info[1]] = None
                if info[1]+','+info[2] not in arquitecturas:
                    arquitecturas[info[1]+','+info[2]] = None
                if info[1]+','+info[2]+','+info[3] not in topologias:
                    topologias[info[1]+','+info[2]+','+info[3]] = None
                if info[1]+','+info[2]+','+info[3]+','+info[4] not in homologias:
                    homologias[info[1]+','+info[2]+','+info[3]+','+info[4]] = None
                info = info[0]+','+info[1]+','+info[2]+','+info[3]+','+info[4]
                print(info,file=dominios)
                dominios.flush()

            #print(info)
            #caths.append(info)
    if count == 3:
        break
cathList.close()
dominios.close()

print('Nodes:',p)
print('A:',alfas,'; B:',betas,'; AB:',alfabetas,'; FSS:',pocas,especiales)
print('ClasseS:',len(clases),'; Architectures:',len(arquitecturas),'; Topologies:',len(topologias),'; Homologous Superfamilies:',len(homologias))


'''
    domain = list(map(int,domain))
    if domain[0] not in clases:
        clases.append(domain[0])
    if domain[1] not in arquit:
        arquit.append(domain[1])
    if domain[2] not in topolo:
        topolo.append(domain[2])
    if domain[3] not in homolo:
        homolo.append(domain[3])
'''

'''
print(clases)
print(arquit)
print(topolo)
print(homolo)
'''
#https://files.rcsb.org/view/2IJ4.pdb
