#!/usr/bin/env bash
set -euo pipefail

UPLOAD_DIR="to_upload"
REMOTE_BASE="uploads/edr.choi_gmail.com_DXDctDev"

SCRIPT="./upload_ascp_sequential.sh"

if [[ ! -x "$SCRIPT" ]]; then
  echo "ERROR: $SCRIPT not found or not executable"
  exit 1
fi

shopt -s nullglob

for fastq_list in "$UPLOAD_DIR"/*_fastqs.txt; do
  # Extract rg_id (strip path and suffix)
  fname=$(basename "$fastq_list")
  rg_id="${fname%_fastqs.txt}"

  remote_dir="${REMOTE_BASE}/${rg_id}"

  echo "============================================"
  echo "Uploading FASTQs for ${rg_id}"
  echo "  List:   ${fastq_list}"
  echo "  Remote: ${remote_dir}"
  echo "============================================"

  "$SCRIPT" "$fastq_list" "$remote_dir"
done

echo "All uploads completed."