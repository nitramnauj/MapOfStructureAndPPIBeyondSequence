# Map of Structure and PPI Beyond Sequence

This repository contains Python scripts to reproduce the cosine similarity network analysis described in the associated study.  
All random selections are fixed with a random seed (`42`) to ensure reproducibility.

## 🗃️ Key Modules Overview

```
DATA PREPARATION
├── sampleAngles.py: Pairwise angle calculations
├── c1_sampler.py: Random sampling
└── c2_generator-v4.py: Synthetic vector generation

NETWORK CONSTRUCTION
├── fasterNetworker.py: Core parallelism detection
├── atLeastOne.py: Filter vectors with parallels
└── c4_angleNhistoCalculator.py: Histogram generation

NETWORK ANALYSIS
├── findGCC.py: Giant component extraction
├── degreeCounter.py: Degree distribution
├── multiple.py: Model fitting
└── orgCounter.py: Organism-specific stats

VISUALIZATION
├── orgColorGCC.py: Species-based coloring
└── classColor.py: CATH-based coloring

EXTERNAL DATA
├── catherV3.py: CATH classification
├── searchBioGrid.py: BioGRID integration
└── degreeByNodeByOrg.py: Combined analysis

COMPLEX ANALYSIS
├── complexParallelis.py: Intra-complex parallels
└── complexBuilder_v6.py: Assembly simulation
```

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

## 🧬🖥️ Usage

### 1. Compute Angles Between Vectors ⚔️
Run `sampleAngles.py` to calculate angles between pairs of vectors in a given CSV file.  
- Modify `input_name` to point to your file (default: `"d7NoLatN0.csv"`).  
- Adjust `sample_size` to set the number of angle pairs to compute.  
- Outputs are saved in the `Angles/` directory as `<input_file_name>_angulos_n.csv`.

### 2. Generate Random Samples 🦠
Run `c1_sampler.py` to create `S` random samples of size `M` from an input file.  
- Edit the `files` list to specify input files (without extensions).  
- Set `M` (sample size) and `S` (number of samples).  
- Outputs include sample files and corresponding statistics (mean and standard deviation for each RCC).

### 3. Generate Synthetic Vectors 👾
Run `c2_generator-v4.py` to produce synthetic vectors based on RCC distributions.  
- Modify the `averages` list to select input files.  
- Adjust `M` and `S` as needed.  
- Uses a global `curves` file to inform the distribution.
This will take some time.

### 4. Calculate Angle Distributions 📊
Run `c4_angleNhistoCalculator.py` and follow prompts (e.g., enter `"d7NoLat,Random"` or `"d7NoLat,Synthetic"`).  
- Generates angle histograms and outputs parallel pairs to `pars_name.csv`.
This will take some time.

### 5. Find Parallel Vectors 🧠
Run `atLeastOne.py` to identify vectors with at least one parallel partner.  
- Set `input_file`, `output_file`, and angular threshold (`angle`).  
Run `fasterNetworker.py` to list all parallel pairs (edges) as `edges_<input_file>.txt`.
This will take some time.

### 6. Visualize Networks 🌃
Run `orgColorGCC.py` to draw the network, coloring nodes by species using provided organism PDB lists.  
Run `classColor.py` to color edges by CATH class, producing `edges_<input_file>_classes.csv` and `<input_file>_plot.png`.

### 7. Analyze Network Properties 🔬
- **Giant Connected Component:** Use `findGCC.py` to extract GCC edges into `GCC_<input_file>.csv`.  
- **Node Degrees:** Use `degreeCounter.py` to compute degree distribution.  
- **Model Fitting:** Use `multiple.py` to fit exponential/power-law models to the degree distribution.  
- **Organism-Specific Analysis:** Use `orgCounter.py` to output `degreeByNode_<organism>.csv`.  
- **CATH Classification:** Use `catherV3.py` with `cath-domain-list.txt` and edge files.

### 8. Integrate BioGRID Data 🖥️
Run `searchBioGrid.py` to count interactors per UniProt entry in BioGRID, saving results to `biogrid_by_uniprot.csv`.  
Then, run `degreeByNodeByOrg.py` to combine degree and BioGRID data per organism.

### 9. Complex-Level Analysis 🤖
Run `complexParallelis.py` to analyze parallelism between chains within complexes (input: `d7NoLat_benchmark-pdb1.txt`).  
- Outputs the average number of parallel pairs per complex.  
- Saves per-complex vector data in the `PerComplex/` directory.

### 10. Simulate Complex Assembly 🏗️
Run `complexBuilder_v6.py` to simulate complex assembly via stepwise vector addition.  This will take some time.
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

This means that chain D00 interacts with chain A00, forming a subunit "DA". Then, it will interact with chain B, to form a DAB subunit, etc.<br />
The reported angle in each step is the angle between the chain and the previous subunit.<br />
The length of the trajectory is the number of steps needed to includ all possible chainds, wheres the number of used vectors is the number of chains that could be included to build the complex.<br />
The value of the final sum is the length of the sum vector after all the building steps.

## 📝 Notes

- Ensure all required input files (e.g., organism lists, CATH list, BioGRID data) are in the working directory.
- File paths and parameters (e.g., sample sizes, thresholds) are configured within each script.
- Output directories (e.g., `Angles/`, `PerComplex/`) are created automatically if they do not exist.

# 🔄 Example Workflow

This example walks through the main analysis pipeline from raw data to network visualization and complex assembly.

## **Step 1: Prepare Your Data**
Place your input CSV file (e.g., `d7NoLatN0.csv`) in the working directory. Ensure it follows the required format:
- 26 RCC columns
- Final column `C` for class/tag

## **Step 2: Calculate Angles Between Vectors**
```bash
# Sample 10^11 random pairs from the dataset
python sampleAngles.py
```
*Output:* Creates `Angles/angles_d7NoLatN0_11.csv`

## **Step 3: Generate Random Samples & Synthetic Counterparts**
```bash
# Create 10 samples of 1000 vectors each
python c1_sampler.py
# Output: sample_d7NoLatN0_1.csv ... d7NoLatN0_sample_10.csv
# Output: average_d7NoLatN0_1.csv ... average_d7NoLatN0_10.csv

# Generate synthetic vectors matching each sample's statistics
python c2_generator-v4.py
# Output: synthetic_d7NoLatN0_1.csv ... synthetic_d7NoLatN0_10.csv
```

## **Step 4: Build Parallelism Network**
```bash
# Find all parallel pairs (angle < 5 degrees)
python fasterNetworker.py
# Output: edges_d7NoLatN0.txt

# Visualize with organism-based coloring
python orgColorGCC.py
# Output: Network plot (visual)
```

## **Step 5: Analyze Network Properties**
```bash
# Extract the Giant Connected Component
python findGCC.py
# Output: GCC_d7NoLatN0.csv

# Calculate degree distribution
python degreeCounter.py
# Output: degree_distribution_d7NoLatN0.csv

# Fit power-law and exponential models
python multiple.py
# Output: Model coefficients and fit statistics
```

## **Step 6: Integrate External Data**
```bash
# Add CATH classification to nodes
python catherV3.py
# Output: edges_d7NoLatN0_cath.csv

# Count BioGRID interactions for each protein
python searchBioGrid.py
# Output: biogrid_by_uniprot.csv

# Combine degree with organism information
python orgCounter.py
# Output: degreeByNode_human.csv, degreeByNode_musMusculus.csv, etc.

# Cross-reference with BioGRID
python degreeByNodeByOrg.py
# Output: enhanced_degree_by_organism.csv
```

## **Step 7: Complex-Level Analysis**
```bash
# Analyze parallelism within protein complexes
python complexParallelis.py
# Output: Average parallel pairs per complex
# Output: PerComplex/ directory with individual complex files

# Simulate complex assembly via vector addition
python complexBuilder_v6.py
# Output: Assembly trajectories for each complex
# Example output for complex 2qhl:
"""
Found trajectory:
  Step 1: 2qhl_D00
  Step 2: 2qhl_A00 (angle: 4.70°)
  Step 3: 2qhl_B00 (angle: 2.31°)
  Step 4: 2qhl_E00 (angle: 2.10°)
Length of the trajectory: 4 steps
Used vectors: 4 of 5
Final vector length: 265.0283
"""
```

## **Minimal Pipeline**
For a quick test of the main functionality:
```bash
# 1. Generate network from your data
python fasterNetworker.py

# 2. Extract and visualize the GCC
python findGCC.py
python orgColorGCC.py

# 3. Calculate basic statistics
python degreeCounter.py
python catherV3.py
```

## **Troubleshooting Tips**
1. **File not found errors**: Ensure all input files are in the working directory
2. **Memory issues**: Reduce sample sizes in `c1_sampler.py` (set smaller `M` value)
3. **Slow execution**: For large datasets, consider reducing the angle threshold in `fasterNetworker.py`
4. **Missing dependencies**: Install required packages: `pip install numpy matplotlib networkx`

## **Typical Runtime**
- Small dataset (~1,000 vectors): Few seconds
- Medium dataset (~10,000 vectors): 10-20 minutes
- Large dataset (~100,000 vectors): Several hours or days

This workflow reproduces the main analyses from the study, from basic parallelism detection to complex biological interpretation.
