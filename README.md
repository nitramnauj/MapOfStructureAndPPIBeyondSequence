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

