# Data Deposition

This folder contains code used to prepare samples for deposition.

## SRA

Simple hierarchy is: BioProject > BioSample > SRA (fastq file). Each project can have multiple samples, each sample can have multiple SRA entries. We need to populate biosample metadata and SRA metadata.

### Plan

1. Use Jupyter notebooks to access nerd db file to fill the following template sheets:
    a. `/SRA/biosample_prep.ipynb` to fill a BioSample template sheet (about biological sample).
    b. `/SRA/sta_prep.ipynb` to fill SRA metadata template sheet (about sequencing).
2. Use aspera to upload files.
3. Do steps 1 and 2 in batches (by reaction group maybe).

## RMDB

TBD
