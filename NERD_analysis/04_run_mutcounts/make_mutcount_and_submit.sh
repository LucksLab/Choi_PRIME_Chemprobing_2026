#!/usr/bin/env bash
# make_mutcount_and_submit.sh
set -euo pipefail

# --- Config ---
TEMPLATE="/home/ekc5108/b1044/Computational_Output/EKC/EKC.01_SHAPE_standardization/EKC.01.065.refactoring_data_analysis/nerd/examples/all_mutcounts/configs/mutcount_template_rxngroup.yaml"
OUTDIR="/home/ekc5108/b1044/Computational_Output/EKC/EKC.01_SHAPE_standardization/EKC.01.065.refactoring_data_analysis/nerd/examples/all_mutcounts/configs"
LOGDIR="$(dirname "$OUTDIR")/slurm_logs"

# Slurm resources
PARTITION="buyin"
ACCOUNT="b1044"
CPUS=4
MEM="8G"
TIME="4:00:00"

# Input list of reaction groups (one per line). Defaults to reaction_groups.txt
INPUT="${1:-"/home/ekc5108/b1044/Computational_Output/EKC/EKC.01_SHAPE_standardization/EKC.01.065.refactoring_data_analysis/nerd/examples/all_mutcounts/reaction_groups.txt"}"

# --- Checks ---
if [[ ! -f "$TEMPLATE" ]]; then
  echo "Template not found: $TEMPLATE" >&2
  exit 1
fi
if [[ ! -f "$INPUT" ]]; then
  echo "Input list not found: $INPUT" >&2
  echo "Create a file with one reaction group per line, e.g.:"
  echo -e "75_2_A8C\n70_1\n45_2_A8C" >&2
  exit 1
fi

mkdir -p "$OUTDIR" "$LOGDIR"

# --- Main loop ---
# Sort/uniq to avoid duplicates
while IFS= read -r RG; do
  [[ -z "$RG" ]] && continue           # skip empty lines
  YAML="$OUTDIR/mutcount_${RG}.yaml"
  JOB_NAME="mutcount_${RG}"

  # Generate YAML by replacing RXNGROUP with current reaction group
  sed "s/RXNGROUP/${RG}/g" "$TEMPLATE" > "$YAML"
  echo "Wrote $YAML"

  # Submit job
  sbatch -p "$PARTITION" -A "$ACCOUNT" -c "$CPUS" --mem="$MEM" -t "$TIME" \
    --job-name "$JOB_NAME" -o "$LOGDIR/${JOB_NAME}.%j.out" \
    --wrap="nerd run mut_count $YAML"

done < <(sort -u "$INPUT")