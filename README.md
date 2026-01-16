# Choi_PRIME_Chemprobing_2026

This repository accompanies the manuscript and provides all code, configurations, and Jupyter notebooks used to perform and reproduce the analyses. It contains:

- the complete **primary analysis pipeline** (FASTQ → mutational counting → kinetic fitting → energetics) implemented with **`nerd`**,  
- the **organized SQLite database** storing all results and metadata, and  
- all **figure-generation notebooks** used in the manuscript.

---

## Nerd vs Figure Analysis

### `nerd` (primary analysis)
`nerd` is the command-line workflow used to run the full chemical-probing analysis pipeline:

1. **Import sample metadata** via YAML.  
2. **Process raw sequencing reads (FASTQ)** into mutation counts.  
3. **Fit time-course data** to extract kinetic parameters (`k_add`, `k_deg`, `k_obs`).  
4. **Store all results and experimental metadata** in a structured SQLite database (`nerd.sqlite`).  

All primary analyses used in the manuscript were executed with `nerd`. Configuration files for each run are included for transparency and reproducibility. For installation and detailed usage, see the separate `nerd` repository.

### `Figure_analysis` (manuscript figures)
The `Figure_analysis` directory contains Jupyter notebooks that **read `nerd` outputs** (e.g., kinetic rates, fit diagnostics, per-nucleotide energetics) and perform all **downstream processing and visualization** used to generate the manuscript figures.  
Each notebook corresponds to a figure or supplementary figure in the paper.

---

## Figure Analysis Quickstart

1. Install required Python packages:  
   `pandas`, `numpy`, `matplotlib`, `seaborn`, `lmfit`  
   (`sqlite3` is included with standard Python).  
2. Open any notebook under `/Figure_analysis`.  
3. Set the path to the provided `nerd.sqlite` (or `new.db`) file.  
4. Run the notebook top-to-bottom to reproduce the figure.

---

## Directory Map

- **`/Core_nerd_analysis`**  
  Primary `nerd` runs, YAML configs, and all pipeline outputs.  
  Includes:
  - sample definitions  
  - mutational counting runs  
  - time-course and temperature-gradient kinetic fits  
  - the main databases: `nerd.sqlite` and `new.db`

- **`/Data_deposition`**  
  Notebooks and metadata used for preparing SRA/RMDB deposition files.

- **`/Figure_analysis`**  
  Jupyter notebooks for generating all manuscript figures:
  - `Figure1_KineticModelForm`
  - `Figure2_ProbeKinetics`
  - `Figure3_EnergyValidation`
  - `Figure4_DynamicEnsemble`
  - `Figure5_TertiaryContacts`
  - `Methods_ConstructDesign`
  - `SFig1_ODEvAnalytical`
  - `SFig3_MutsPerRead`
  - `SFig4_DegGlobal`
  - `SFig5_TempgradQuality`
  - `SFig7_NmrDegValidation`
  - `SFig8_NmrAddValidation`
  - `SFig9_ReplicateReproducibility`
  - `SFig11_EnergyCorrelations`
  - `SFig12_HIV_P4P6_Qc`
  - `SFig14_P4P6Replicates`
  - `SFig15_P4P6OtherContexts`
  - `SFig16_UnifiedEnergyScale`

---

## License
MIT — see `LICENSE`.
