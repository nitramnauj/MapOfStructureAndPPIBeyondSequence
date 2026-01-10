# MapOfStructureAndPPIBeyondSequence
Codes to reproduce cosine similarity network analysis.

These codes work with .csv files formated as follows:

PDBID,RCC1,RCC2,RCC3,RCC4,RCC5,RCC6,RCC7,RCC8,RCC9,RCC10,RCC11,RCC12,RCC13,RCC14,RCC15,RCC16,RCC17,RCC18,RCC19,RCC20,RCC21,RCC22,RCC23,RCC24,RCC25,RCC26,C<br />
101mA00,2,1,7,0,13,0,5,8,0,2,0,0,0,4,103,0,0,0,0,0,0,0,0,0,0,2,1<br />
102lA00,9,6,10,0,5,2,19,5,0,0,0,0,1,13,85,0,0,0,0,0,0,0,0,0,0,2,1<br />
102mA00,2,1,7,0,14,0,7,8,0,2,0,0,0,4,103,0,0,0,0,0,0,0,0,0,0,2,1<br />

Where:<br />
\<PDBID\> is the string vector name, or the PDB chain for PDB structures.<br />
\<RCC1\>, \<RCC2\>, ..., \<RCC26\> are 26 numbers (integers for rcc collections).<br />
\<C\> is a string tag for the vector, or the CATH class for the corresponding protein domain.<br />

To get the angles between a sample of posible pairs of vectors in a \<input_file_name\>.csv file, just run _sampleAngles.py_.<br />
To use another file, change **input_name** variable to the corresponding file name. Currently is "d7NoLatN0.csv".<br />
To change the sample size, change the values inside **sample_size** list. Currently is 11, to calculate 10^11 pairs.<br />
This will create (if not already exists) an output directory named Angles, where the output file is named \<input_file_name\>_angulos_n.csv, where **n** is the value in **sample_size**.
