#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./upload_ascp_sequential.sh fastqs.txt uploads/edr.choi_gmail.com_DXDctDev/some_dir
#   remember to put in a directory to be detected on wizard preload
#
# fastqs.txt: one local filepath per line
# remote_dir: your NCBI upload folder (after the colon). No trailing slash needed.

FILES_LIST="${1:-}"
REMOTE_DIR="${2:-}"

if [[ -z "$FILES_LIST" || -z "$REMOTE_DIR" ]]; then
  echo "Usage: $0 fastqs.txt uploads/<your_ncbi_upload_folder>"
  exit 1
fi

if [[ ! -f "$FILES_LIST" ]]; then
  echo "ERROR: file list not found: $FILES_LIST"
  exit 1
fi

# ---- CONFIG (match your working command) ----
ASCP_BIN="${ASCP_BIN:-ascp}"
ASCP_KEY="${ASCP_KEY:-$HOME/.aspera/aspera.openssh}"
ASCP_USER_HOST="${ASCP_USER_HOST:-subasp@upload.ncbi.nlm.nih.gov}"

ASCP_OPTS=(
  -i "$ASCP_KEY"
  -QT
  -l100m
  -k1
  -d
)

LOGDIR="${LOGDIR:-ascp_logs}"
mkdir -p "$LOGDIR"

# --- derive summary name from REMOTE_DIR (last path component) ---
REMOTE_DIR_TRIMMED="${REMOTE_DIR%/}"          # drop trailing slash if any
SUM_DIR="$(basename "$REMOTE_DIR_TRIMMED")"   # e.g., rg10_25_2
SUMMARY="$LOGDIR/${SUM_DIR}_summary.tsv"

: > "$SUMMARY"
echo -e "file\texit_code\tstatus" >> "$SUMMARY"

echo "[INFO] Uploading files listed in: $FILES_LIST"
echo "[INFO] Destination: $ASCP_USER_HOST:$REMOTE_DIR_TRIMMED"
echo "[INFO] Key: $ASCP_KEY"
echo "[INFO] Summary: $SUMMARY"
echo

# sequential loop
while IFS= read -r f || [[ -n "$f" ]]; do
  # skip blanks/comments
  [[ -z "$f" ]] && continue
  [[ "$f" =~ ^# ]] && continue

  if [[ ! -f "$f" ]]; then
    echo "[WARN] Missing file (skipping): $f"
    echo -e "${f}\tNA\tMISSING" >> "$SUMMARY"
    continue
  fi

  echo "[INFO] Uploading: $f"
  set +e
  "$ASCP_BIN" "${ASCP_OPTS[@]}" "$f" "$ASCP_USER_HOST:$REMOTE_DIR_TRIMMED"
  ec=$?
  set -e

  if [[ $ec -eq 0 ]]; then
    echo "[OK]   Uploaded: $f"
    echo -e "${f}\t${ec}\tSUCCESS" >> "$SUMMARY"
  else
    echo "[FAIL] Upload failed (exit $ec): $f"
    echo -e "${f}\t${ec}\tFAIL" >> "$SUMMARY"
    # To stop immediately on first failure, uncomment:
    # exit $ec
  fi

  echo
done < "$FILES_LIST"

echo "[INFO] Done. Summary written to: $SUMMARY"