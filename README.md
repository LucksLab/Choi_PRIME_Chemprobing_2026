# Choi_PRIME_Chemprobing_2026

**Ubiquitous low-energy RNA fluctuations and energetic coupling measured by chemical probing** (2026)  
**Authors:** Edric K. Choi, Ritwika Bose, David H. Mathews, Anthony M. Mustoe*, Julius B. Lucks*

This repository accompanies the manuscript *“Ubiquitous low-energy RNA fluctuations and energetic coupling measured by chemical probing”* and provides all data, analysis code, and figure-generation workflows used in the study.

The repository is organized to enable transparency, reproducibility, and reuse, from processed sequencing data through kinetic modeling and final figures.

---

## Repository structure
```
.
├── Core_nerd_analysis/
├── Data_deposition/
├── Figure_analysis/
└── README.md
```

### `Core_nerd_analysis/`
This directory contains the primary data processing and kinetic modeling outputs generated using the `nerd` framework.

- Configuration files used to run `nerd`
- Processing from FASTQ files to mutation counts
- Nonlinear time-course fitting to extract kinetic parameters (e.g., k_obs, k_deg)
- All results stored in a centralized SQLite database (`nerd.sqlite`), organized by experimental metadata (construct, temperature, condition, replicate, etc.)

All `nerd` analyses have been pre-run for this repository. The SQLite database at
`Core_nerd_analysis/nerd.sqlite` serves as the single source of truth for all downstream analyses.

---

### `Figure_analysis/`
This directory contains secondary analysis and figure-generation code that operates on the processed `nerd` outputs.

- Jupyter notebooks and scripts load data directly from `nerd.sqlite`
- Includes all analyses used to generate:
  - Main text figures
  - Supplementary figures
  - Extended data analyses
- The file `code_figure_method_map.csv` provides an exhaustive mapping between manuscript figures/methods and the exact code used to generate them

This directory is the recommended entry point for readers interested in reproducing figures or exploring the analyses presented in the paper.

---

### `Data_deposition/`
This directory contains materials related to public data deposition.

- CSV files listing all SRA accession numbers associated with this study
- Metadata tables linking experimental samples to deposited sequencing runs
- Helper scripts used during submission to NCBI SRA

Raw sequencing data are publicly available through the SRA and are not duplicated in this repository.

---

## How to run the analyses

### Recommended workflow
All primary processing has already been completed. To reproduce figures or explore analyses:

1. Clone this repository
2. Create a Python environment and install required dependencies
3. Run the notebooks in `Figure_analysis/`

All notebooks assume access to `Core_nerd_analysis/nerd.sqlite` and do not require reprocessing
of raw FASTQ files.

---

### Running `nerd` from scratch (optional)
To rerun the full processing pipeline from raw sequencing data:

- See the `nerd` documentation: `https://github.com/LucksLab/nerd`
- Configuration files used in this study are provided in `Core_nerd_analysis/`

Re-running `nerd` is not required to reproduce any analyses or figures in the manuscript.

---

## Software environment
Analyses were performed in Python using standard scientific libraries (NumPy, pandas, SciPy, lmfit, matplotlib, seaborn, etc.).  
Exact dependencies can be inferred from the notebooks and scripts in `Figure_analysis/`.

---

## License
- **Code** in this repository is released under the MIT License.
- **Data and derived results** (including `nerd.sqlite` and CSV files) are released under the Creative Commons Attribution 4.0 International (CC-BY 4.0) License.

---

## Citation
If you use data or code from this repository, please cite:

Choi EK, Bose R, Mathews DH, Mustoe AM*, Lucks JB*.  
*Ubiquitous low-energy RNA fluctuations and energetic coupling measured by chemical probing.*  
2026.
