# Data Deposition

This folder contains code and templates used to prepare data for public deposition.

## For reviewers
Reviewer link: https://dataview.ncbi.nlm.nih.gov/object/PRJNA1400640?reviewer=pm19k19g8br0n19kjdvas8p4k9
CSV of all accession files used in this study: /Data_deposition/SRA_accession_01272026.tsv

## SRA

Simple hierarchy is: BioProject > BioSample > SRA (FASTQ). Each project can have multiple samples, each sample can have multiple SRA entries.
We populate BioSample metadata and SRA metadata from the `nerd` database.

### Workflow

1. Generate template-filled metadata from the database:
   - `SRA/biosample_sra_prep.py`
   - Templates live under `SRA/templates/`
2. Stage files for upload under `SRA/to_upload/`.
3. Upload with Aspera:
   - `SRA/run_all_aspera_uploads.sh` or `SRA/upload_ascp_sequential.sh`
4. Perform uploads in batches as needed.


## RMDB

TBD. Add RMDB preparation steps here as they are finalized.
