# Map of Structure and PPI Beyond Sequence

This repository contains Python scripts to reproduce the cosine similarity network analysis described in the associated study.  
All random selections are fixed with a random seed (`42`) to ensure reproducibility.

## 📁 Data Format

The scripts operate on `.csv` files formatted as follows:

```
PDBID,RCC1,RCC2,...,RCC26,C
101mA00,2,1,7,0,13,0,5,8,0,2,0,0,0,4,103,0,0,0,0,0,0,0,0,0,0,2,1
102lA00,9,6,10,0,5,2,19,5,0,0,0,0,1,13,85,0,0,0,0,0,0,0,0,0,0,2,1
102mA00,2,1,7,0,14,0,7,8,0,2,0,0,0,4,103,0,0,0,0,0,0,0,0,0,0,2,1
```

Where:

- **`PDBID`** — Identifier for the vector (e.g., PDB chain for protein structures).
- **`RCC1` to `RCC26`** — 26 integer values representing RCC collections.
- **`C`** — A string tag for the vector (e.g., CATH class for the protein domain).

## 🚀 Usage

### 1. Compute Angles Between Vectors
Run `sampleAngles.py` to calculate angles between pairs of vectors in a given CSV file.  
- Modify `input_name` to point to your file (default: `"d7NoLatN0.csv"`).  
- Adjust `sample_size` to set the number of angle pairs to compute.  
- Outputs are saved in the `Angles/` directory as `<input_file_name>_angulos_n.csv`.

### 2. Generate Random Samples
Run `c1_sampler.py` to create `S` random samples of size `M` from an input file.  
- Edit the `files` list to specify input files (without extensions).  
- Set `M` (sample size) and `S` (number of samples).  
- Outputs include sample files and corresponding statistics (mean and standard deviation for each RCC).

### 3. Generate Synthetic Vectors
Run `c2_generator-v4.py` to produce synthetic vectors based on RCC distributions.  
- Modify the `averages` list to select input files.  
- Adjust `M` and `S` as needed.  
- Uses a global `curves` file to inform the distribution.

### 4. Calculate Angle Distributions
Run `c4_angleNhistoCalculator.py` and follow prompts (e.g., enter `"d7NoLat,Random"` or `"d7NoLat,Synthetic"`).  
- Generates angle histograms and outputs parallel pairs to `pars_name.csv`.

### 5. Find Parallel Vectors
Run `atLeastOne.py` to identify vectors with at least one parallel partner.  
- Set `input_file`, `output_file`, and angular threshold (`angle`).  
Run `fasterNetworker.py` to list all parallel pairs (edges) as `edges_<input_file>.txt`.

### 6. Visualize Networks
Run `orgColorGCC.py` to draw the network, coloring nodes by species using provided organism PDB lists.  
Run `classColor.py` to color edges by CATH class, producing `edges_<input_file>_classes.csv` and `<input_file>_plot.png`.

### 7. Analyze Network Properties
- **Giant Connected Component:** Use `findGCC.py` to extract GCC edges into `GCC_<input_file>.csv`.  
- **Node Degrees:** Use `degreeCounter.py` to compute degree distribution.  
- **Model Fitting:** Use `multiple.py` to fit exponential/power-law models to the degree distribution.  
- **Organism-Specific Analysis:** Use `orgCounter.py` to output `degreeByNode_<organism>.csv`.  
- **CATH Classification:** Use `catherV3.py` with `cath-domain-list.txt` and edge files.

### 8. Integrate BioGRID Data
Run `searchBioGrid.py` to count interactors per UniProt entry in BioGRID, saving results to `biogrid_by_uniprot.csv`.  
Then, run `degreeByNodeByOrg.py` to combine degree and BioGRID data per organism.

### 9. Complex-Level Analysis
Run `complexParallelis.py` to analyze parallelism between chains within complexes (input: `d7NoLat_benchmark-pdb1.txt`).  
- Outputs the average number of parallel pairs per complex.  
- Saves per-complex vector data in the `PerComplex/` directory.

### 10. Simulate Complex Assembly
Run `complexBuilder_v6.py` to simulate complex assembly via stepwise vector addition.  
- Reads all files in `PerComplex/`.  
- Outputs assembly trajectories, e.g.:

```
Found trajectory:
  Step 1: 2qhl_D00
  Step 2: 2qhl_A00 (angle: 4.70°)
  Step 3: 2qhl_B00 (angle: 2.31°)
  Step 4: 2qhl_E00 (angle: 2.10°)

Length of the trajectory: 4 steps
Used vectors: ['2qhl_D00', '2qhl_A00', '2qhl_B00', '2qhl_E00']
Number of used vectors: 4
Value of the final sum: 265.0283
```

## 📝 Notes

- Ensure all required input files (e.g., organism lists, CATH list, BioGRID data) are in the working directory.
- File paths and parameters (e.g., sample sizes, thresholds) are configured within each script.
- Output directories (e.g., `Angles/`, `PerComplex/`) are created automatically if they do not exist.
