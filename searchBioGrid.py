entrada = open('BIOGRID-ALL-5.0.251.mitab.txt')
uniprot_interactions = {}
for line in entrada:
        if '#ID Interactor A' not in line:
                aux = line[:-1].split('\t')
                #print(aux[2])
                try:
                        uniprot = aux[2].split('swiss-prot:')
                        uniprot = uniprot[1].split('|')[0]
                        #print(uniprot)
                        if uniprot not in uniprot_interactions:
                                uniprot_interactions[uniprot] = 0
                        else:
                                uniprot_interactions[uniprot] += 1

                except:
                        continue

entrada.close()

salida = open('biogrid_by_uniprot.csv','w')
print('Uniprot,BiogridCounts',file=salida)
for up in uniprot_interactions:
        print(up+','+str(uniprot_interactions[up]),file=salida)
salida.close()
