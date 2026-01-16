#!/usr/bin/env python3
"""
Generate NCBI BioSample (Microbe.1.0-style) and SRA metadata files, plus fastq path
manifests, grouped by probe_reaction_groups.rg_id.

This combines the logic of biosample_prep.py and sra_prep.py so both are driven by
a single SQL query.

Typical usage:
  python biosample_sra_prep.py \
    --db ../../Core_nerd_analysis/nerd.sqlite \
    --microbe-template ./templates/Microbe.1.0.tsv \
    --sra-template ./templates/SRA_metadata.txt \
    --outdir to_upload
"""

import argparse
import csv
import sqlite3
from collections import defaultdict
from pathlib import Path


# --- constant description from your methods text (copied from sra_prep.py) ---
SRA_DESCRIPTION = (
    "Sequencing libraries were generated using a two-step PCR amplification workflow. "
    "First-strand cDNA served as input for PCR1, which was performed using high-fidelity "
    "polymerase and locus-specific primers to amplify the target region. PCR1 products were "
    "purified with SPRI beads, and a defined amount of purified amplicon was used as input "
    "for PCR2. PCR2 incorporated unique dual 8-bp indexes to enable multiplexed sequencing, "
    "with indexing primers dispensed into individual wells using an acoustic liquid handler. "
    "Following cleanup, individual libraries were quantified by fluorescence-based dsDNA "
    "assays and pooled in equimolar ratios. The final pooled library was assessed by "
    "Bioanalyzer (High Sensitivity DNA or DNA 1K) prior to sequencing. Libraries were "
    "sequenced on an Illumina MiSeq (2×75 bp) or NextSeq 1000/2000 (2×150 bp) platform "
    "with a 10–15% PhiX spike-in to ensure balanced base composition."
)

# Map your construct families to NCBI organism names (copied from biosample_prep.py)
ORGANISM_MAP = {
    "Salm_4U_thermometer": "Salmonella enterica",
    "HIV-1_TAR": "Human immunodeficiency virus 1",
    "P4P6_full": "Tetrahymena thermophila",
}


# ---- SQL (single source of truth) ----
# One row per (sequencing sample, reaction) with enough columns to build:
#   - BioSample (Microbe.1.0-style TSV)
#   - SRA run metadata (tab-delimited template)
#   - fastq path manifests
COMBINED_SQL = """
SELECT
    -- sequencing sample + run fields (needed for SRA + fastqs)
    ss.id               AS sample_id,
    ss.sample_name      AS sample_name,
    ss.fq_dir           AS fq_dir,
    ss.r1_file          AS r1_file,
    ss.r2_file          AS r2_file,
    ss.to_drop          AS to_drop,
    sr.id               AS run_id,
    sr.date             AS seq_run_date,
    sr.sequencer        AS sequencer,

    -- reaction fields (needed for BioSample; also used for grouping)
    pr.id               AS reaction_id,
    pr.temperature      AS temperature,
    pr.probe            AS probe,
    pr.probe_concentration AS probe_concentration,
    pr.replicate        AS replicate,
    pr.done_by          AS done_by,

    -- construct + reaction group fields (needed for organism + grouping)
    mc.family           AS construct_family,
    prg.rg_id           AS rg_id,
    prg.rg_label        AS rg_label

FROM probe_fmod_values      AS pfv
JOIN probe_fmod_runs        AS pfr ON pfv.fmod_run_id = pfr.id
JOIN sequencing_samples     AS ss  ON pfr.s_id        = ss.id
JOIN sequencing_runs        AS sr  ON ss.seqrun_id    = sr.id
JOIN probe_reactions        AS pr  ON pfv.rxn_id      = pr.id
JOIN probe_reaction_groups  AS prg ON pr.rg_id        = prg.rg_id
JOIN meta_constructs        AS mc  ON pr.construct_id = mc.id

WHERE ss.to_drop = 0

-- pfv can create many duplicates; keep one row per (sample, reaction)
GROUP BY ss.id, pr.id

ORDER BY prg.rg_id, mc.family, ss.sample_name, pr.id
"""


def get_connection(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def join_fq(fq_dir, fname) -> str:
    if not fq_dir:
        return fname or ""
    if not fname:
        return ""
    return str(Path(fq_dir) / fname)


def slugify_label(label: str) -> str:
    if label is None:
        return "NA"
    s = label.strip()
    bad = [' ', '/', '\\', ':', ';', ',', '(', ')', '[', ']', '{', '}', '"', "'"]
    for ch in bad:
        s = s.replace(ch, "_")
    while "__" in s:
        s = s.replace("__", "_")
    return s or "NA"


def instrument_model_from_sequencer(sequencer: str) -> str:
    """
    Map sequencing_runs.sequencer -> SRA instrument_model vocabulary.
    """
    if not sequencer:
        return "Illumina MiSeq"
    s = sequencer.strip().lower()
    if "miseq" in s:
        return "Illumina MiSeq"
    if "nextseq" in s:
        # adjust if you prefer "Illumina NextSeq 2000"
        return "NextSeq 1000"
    if "novaseq" in s:
        return "Illumina NovaSeq 6000"
    return "Illumina MiSeq"


def map_family_to_organism(family: str) -> str:
    if family is None:
        return ""
    return ORGANISM_MAP.get(family, family)


def format_collection_date(s: str) -> str:
    """
    Convert common date formats to YYYY-MM-DD for BioSample.
    Accepts:
      - 'YYYY-MM-DD' (passes through)
      - 'YYMMDD' or 'YYMMDD...' (e.g., '250208' -> 2025-02-08)
    """
    if not s:
        return ""
    s = str(s).strip()
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return s[:10]
    if len(s) >= 6 and s[:6].isdigit():
        yy = int(s[0:2])
        mm = s[2:4]
        dd = s[4:6]
        year = 2000 + yy
        return f"{year:04d}-{mm}-{dd}"
    return s


# ---------- BioSample (Microbe.1.0) helpers ----------

def read_template_comments(template_path: Path) -> list[str]:
    """
    Preserve initial comment lines from the Microbe template (lines starting with '#').
    """
    comments = []
    with open(template_path, "r") as f:
        for line in f:
            if line.startswith("#"):
                comments.append(line.rstrip("\n"))
            else:
                break
    return comments


def get_microbe_base_headers() -> list[str]:
    """
    Base Microbe.1.0 header from the NCBI template.
    (Copied from biosample_prep.py so your output matches.)
    """
    return [
        "*sample_name",
        "sample_title",
        "bioproject_accession",
        "*organism",
        "strain",
        "isolate",
        "host",
        "isolation_source",
        "*collection_date",
        "*geo_loc_name",
        "*sample_type",
        "altitude",
        "biomaterial_provider",
        "collected_by",
        "culture_collection",
        "description",
        "env_broad_scale",
        "env_local_scale",
        "env_medium",
        "lat_lon",
        "project_name",
    ]


# ---------- SRA template helpers ----------

def read_sra_headers(template_path: Path) -> list[str]:
    """
    Read the first non-empty line from SRA template and use it as the header.
    """
    with open(template_path, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.strip():
                return line.split("\t")
    raise RuntimeError(f"No header line found in {template_path}")


# ---------- combined fetch ----------

def fetch_rows(conn: sqlite3.Connection) -> list[dict]:
    cur = conn.cursor()
    cur.execute(COMBINED_SQL)
    return [dict(r) for r in cur.fetchall()]


def write_biosample_microbe_tsv(
    out_path: Path,
    microbe_template: Path,
    group_rows: list[dict],
) -> int:
    """
    Write one Microbe.1.0-style TSV for a single rg_id.
    Returns number of rows written.
    """
    base_headers = get_microbe_base_headers()
    extra_headers = [
        "sample_id",
        "probe",
        "probe_conc_M",
        "replicate",
        "reaction_group",
        "reaction_id",
        "construct_family",
        "temperature",
    ]
    all_headers = base_headers + extra_headers
    comments = read_template_comments(microbe_template)

    with open(out_path, "w", newline="") as out_f:
        for c in comments:
            out_f.write(c + "\n")

        writer = csv.DictWriter(
            out_f,
            fieldnames=all_headers,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()

        for r in group_rows:
            family = r.get("construct_family", "")
            organism = map_family_to_organism(family)
            collection_date = format_collection_date(r.get("seq_run_date", ""))

            rec = {h: "" for h in all_headers}

            # required / mapped fields
            rec["*sample_name"]      = r.get("sample_name", "")
            rec["*organism"]         = organism
            rec["*collection_date"]  = collection_date
            rec["*geo_loc_name"]     = "not applicable"
            rec["*sample_type"]      = "in vitro transcription"

            # required but not applicable
            rec["isolate"]          = "not applicable"
            rec["strain"]           = "not applicable"
            rec["host"]             = "not applicable"
            rec["isolation_source"] = "not applicable"

            # optional
            rec["sample_title"]          = ""
            rec["bioproject_accession"]  = ""
            rec["collected_by"]          = r.get("done_by", "") or ""
            rec["description"]           = ""

            # extra columns
            rec["sample_id"]        = r.get("sample_id", "")
            rec["reaction_id"]      = r.get("reaction_id", "")
            rec["construct_family"] = family
            rec["temperature"]      = r.get("temperature", "")
            rec["probe"]            = r.get("probe", "")
            rec["probe_conc_M"]     = r.get("probe_concentration", "")
            rec["replicate"]        = r.get("replicate", "")
            rec["reaction_group"]   = r.get("rg_label", "")

            writer.writerow(rec)

    return len(group_rows)


def write_sra_tsv_and_fastq_manifest(
    out_sra_path: Path,
    out_fastqs_path: Path,
    sra_template: Path,
    group_rows: list[dict],
) -> tuple[int, int]:
    """
    Write one SRA metadata TSV (from SRA template headers) + one fastq list for this rg_id.
    Deduplicates SRA rows by (sample_id, rg_id) and fastq paths globally within the rg.
    Returns (n_sra_rows, n_fastqs).
    """
    headers = read_sra_headers(sra_template)

    # dedupe SRA rows by (sample_id, rg_id)
    seen_sra = set()
    fastq_paths = []
    seen_fastq = set()

    n_sra = 0
    with open(out_sra_path, "w", newline="") as out_f:
        writer = csv.DictWriter(
            out_f,
            fieldnames=headers,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()

        for r in group_rows:
            key = (r.get("sample_id"), r.get("rg_id"))
            if key in seen_sra:
                continue
            seen_sra.add(key)

            instr_model = instrument_model_from_sequencer(r.get("sequencer", ""))

            rec = {h: "" for h in headers}
            rec["sample_name"]        = r.get("sample_name", "")
            rec["library_ID"]         = f'ss{r.get("sample_id")}_sr{r.get("run_id")}'
            rec["title"]              = r.get("sample_name", "")
            rec["library_strategy"]   = "OTHER"
            rec["library_source"]     = "SYNTHETIC"
            rec["library_selection"]  = "other"
            rec["library_layout"]     = "PAIRED"
            rec["platform"]           = "ILLUMINA"
            rec["instrument_model"]   = instr_model
            rec["design_description"] = SRA_DESCRIPTION
            rec["filetype"]           = "fastq"
            rec["filename"]           = r.get("r1_file", "") or ""
            rec["filename2"]          = r.get("r2_file", "") or ""

            writer.writerow(rec)
            n_sra += 1

            # fastq paths (also deduped)
            r1 = join_fq(r.get("fq_dir"), r.get("r1_file"))
            r2 = join_fq(r.get("fq_dir"), r.get("r2_file"))
            for p in (r1, r2):
                if p and p not in seen_fastq:
                    seen_fastq.add(p)
                    fastq_paths.append(p)

    with open(out_fastqs_path, "w") as f:
        for p in fastq_paths:
            f.write(p + "\n")

    return n_sra, len(fastq_paths)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, required=True, help="Path to nerd.sqlite")
    ap.add_argument("--microbe-template", type=Path, required=True, help="Path to templates/Microbe.1.0.tsv")
    ap.add_argument("--sra-template", type=Path, required=True, help="Path to templates/SRA_metadata.txt")
    ap.add_argument("--outdir", type=Path, default=Path("to_upload"), help="Output directory")
    args = ap.parse_args()

    assert args.db.exists(), f"DB not found: {args.db}"
    assert args.microbe_template.exists(), f"Microbe template not found: {args.microbe_template}"
    assert args.sra_template.exists(), f"SRA template not found: {args.sra_template}"

    args.outdir.mkdir(parents=True, exist_ok=True)

    conn = get_connection(args.db)
    rows = fetch_rows(conn)
    conn.close()

    if not rows:
        print("No rows found (after filtering ss.to_drop=0).")
        return

    grouped = defaultdict(list)
    for r in rows:
        grouped[(r["rg_id"], r["rg_label"])].append(r)

    print(f"Found {len(grouped)} reaction groups.")

    for (rg_id, rg_label), group_rows in grouped.items():
        label_slug = slugify_label(rg_label)

        biosample_path = args.outdir / f"rg{rg_id}_{label_slug}_BioSample.tsv"
        sra_path       = args.outdir / f"rg{rg_id}_{label_slug}_SRA.txt"
        fastqs_path    = args.outdir / f"rg{rg_id}_{label_slug}_fastqs.txt"

        n_bio = write_biosample_microbe_tsv(
            out_path=biosample_path,
            microbe_template=args.microbe_template,
            group_rows=group_rows,
        )

        n_sra, n_fq = write_sra_tsv_and_fastq_manifest(
            out_sra_path=sra_path,
            out_fastqs_path=fastqs_path,
            sra_template=args.sra_template,
            group_rows=group_rows,
        )

        print(f"rg_id={rg_id}  rows: biosample={n_bio}, sra={n_sra}, fastqs={n_fq}")
        print(f"  BioSample: {biosample_path}")
        print(f"  SRA:      {sra_path}")
        print(f"  fastqs:   {fastqs_path}")


if __name__ == "__main__":
    main()
