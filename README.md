# MapOfStructureAndPPIBeyondSequence
Codes to reproduce cosine similarity network analysis.<br />

All random choosing has been fixed with a random seed (42) to ensure reproducibility.

These codes work with .csv files formated as follows:

PDBID,RCC1,RCC2,RCC3,RCC4,RCC5,RCC6,RCC7,RCC8,RCC9,RCC10,RCC11,RCC12,RCC13,RCC14,RCC15,RCC16,RCC17,RCC18,RCC19,RCC20,RCC21,RCC22,RCC23,RCC24,RCC25,RCC26,C<br />
101mA00,2,1,7,0,13,0,5,8,0,2,0,0,0,4,103,0,0,0,0,0,0,0,0,0,0,2,1<br />
102lA00,9,6,10,0,5,2,19,5,0,0,0,0,1,13,85,0,0,0,0,0,0,0,0,0,0,2,1<br />
102mA00,2,1,7,0,14,0,7,8,0,2,0,0,0,4,103,0,0,0,0,0,0,0,0,0,0,2,1<br />

Where:<br />
\<PDBID\> is the string vector name, or the PDB chain for PDB structures.<br />
\<RCC1\>, \<RCC2\>, ..., \<RCC26\> are 26 numbers (integers for rcc collections).<br />
\<C\> is a string tag for the vector, or the CATH class for the corresponding protein domain.<br />

**Angles between vectors in a file**<br />
To get the angles between a sample of posible pairs of vectors in a \<input_file_name\>.csv file, just run _sampleAngles.py_.<br />
To use another file, change **input_name** variable to the corresponding file name. Currently is "d7NoLatN0.csv".<br />
To change the sample size, change the values inside **sample_size** list. Currently is 11, to calculate 10^11 pairs.<br />
This will create (if not already exists) an output directory named Angles, where the output file is named \<input_file_name\>_angulos_n.csv, where **n** is the value in **sample_size**.

To generate a number **S** of different samples for a \<input_file_name\> file, each one with **M** vectors (where **M**<**N**, **N** the number of vectors), just run _c1_sampler.py_.<br />
To get the samples for different input files, change **files** list, without extension.<br />
To get samples of different size, change **M** value.<br />
To change the number of samples, change **S** value.<br />
This will create **S** output files with **M** vectors each one. Also, it will create **S** output files with the average and standard deviation values for each one of the 26 \<RCC\> values.

To generate a **M** synthetic vectors for each sample, just run _c2_generator-v4.py_.<br />
This code takes the distribution of the 26 \<RCC\> values, and the sum of the corresponding 26 \<RCC\> values for a given vector in a sample, to generate a new synthetic vector.<br />
It also takes the corresponding _curves_ file into account, which describes the global distribution of vectors, not only the current sample.<br />
To get the samples for different input files, change **averages** list, without extension.<br />
To get samples of different size, change **M** value.<br />
To change the number of samples, change **S** value.<br />
This will create **S** output files with **M** synthetic vectors each one.

To calculate the angles between all possible pairs inside all samples, run _c4_angleNhistoCalculator.py_ and input "d7NoLat,Random" or "d7NoLat,Synthetic", or the corresponding case you are testing.<br />
This script doesn't save the angles, instead outputs a histogram of the values.<br />
This script outputs a file, _pars_name.csv_, with the pairs of parallel angles in a given sample.

To find the vectors with at least one parallel, just run _atLeastOne.py_.<br />
This script will output a file where each line is a vector which is parallel to another one in the input file.<br />
To change the input and output files, change the **input_file** and **output_file** values.<br />
To change the angular threshold value to consider a vector "parallel", change **angle** value.

To find the pair of parallel vectors with the thershold used in the previous script, just run _fasterNetworker.py_.<br />
This script will output a file named edges_<input_file>.txt, where each line is an edge in a network of parallelism.<br />
It could be run with whichever input file formated as follows:

PDBID,RCC1,RCC2,RCC3,RCC4,RCC5,RCC6,RCC7,RCC8,RCC9,RCC10,RCC11,RCC12,RCC13,RCC14,RCC15,RCC16,RCC17,RCC18,RCC19,RCC20,RCC21,RCC22,RCC23,RCC24,RCC25,RCC26,C<br />
101mA00,2,1,7,0,13,0,5,8,0,2,0,0,0,4,103,0,0,0,0,0,0,0,0,0,0,2,1<br />
102lA00,9,6,10,0,5,2,19,5,0,0,0,0,1,13,85,0,0,0,0,0,0,0,0,0,0,2,1<br />
102mA00,2,1,7,0,14,0,7,8,0,2,0,0,0,4,103,0,0,0,0,0,0,0,0,0,0,2,1<br />

To draw the network gotten with the previous script, just run _orgColorGCC.py_.<br />
This will use _human_pbds.txt_, _musMusculus_pdbs.txt_ and _sCerevisiae_pdbs.txt_ as dictionaries to color the nodes with color depending of the species.<br />

To know the number of different Classes, Architectures, Topologies and Homologous Superfamilies, just run _catherV3.py_.<br />
This script uses _cath-domain-list.txt_ and edges_<input_file>.txt to label each PDBID with the corresponding CATH domain.

To draw the network with color by class, just run _classColor.py_.<br />
This script uses edges_<input_file>.txt to label each pair of nodes with their corresponding class as in CATH and colors them.<br />
The output is a file with the edges and the classes for them in a edges_<input_file>_classes.csv file, and a \<input_file\>_plot.png file.

To find the Giant Connected Component (GCC), just runt _findGCC.py_.<br />
This will output a GCC_\<input_file\>.csv file, with only the edges of the GCC.

To know the number of edges for each node (its degree), just run _degreeCounter.py_.<br />
This will output a file with the list of degrees, and how many nodes have such degree.<br />
To fit to the degree distribution gotten with the previous script some exponential models, run _multiple.py_.<br />
This will output the coefficients for the three models described in the main paper (power-law included).

To know the degree distribution by organism, just run _orgCounter.py_.<br />
This script takes the edges_\<input_file\>.txt file and an organism list, such as _human_pdbs.txt_, to print for each node its degree and its Uniprot ID in a degreeByNode_\<organism\>.csv file.

To know the BioGrid counts for each protein, just run the _searchBioGrid.py_ script.<br />
This will read the _BIOGRID-ALL-5.0.251.mitab.txt_ file and count how many interactors has certain uniprot. Then it will print them in an output file, _biogrid_by_uniprot.csv_.

To calculate the degree distribution by organism, with consideration of the BioGrid counts, just run _degreeByNodeByOrg.py_.<br />
This script will take the degreeByNode_\<organism\>.csv file and the _biogrid_by_uniprot.csv_ as inputs.<br />
This will output the nodes, degree and uniprot for the proteins for certain organism.

To analyze the parallelism between the chains in a complex, just run _complexParallelis.py_.<br />
This script takes the file _d7NoLat_benchmark-pdb1.txt_ file as input and creates a _PerComplex_ directory.<br />
The script will output the number of parallel pairs found for all the chains in a complex, and the arithmetic mean for all the complexes in the input file.<br />
In the _PerComplex_ directory, the script will print the vectors separated by complex.

