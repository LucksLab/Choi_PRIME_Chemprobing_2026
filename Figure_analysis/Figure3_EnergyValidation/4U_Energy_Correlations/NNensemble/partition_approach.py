"""
CLI wrapper for RNAstructure (UNIX), originally written by Dave Mathews and
adapted into a CLI. Computes the energetic penalty of forcing a nucleotide
site to be unpaired using the partition function (ensemble-based approach).

Need to make sure RNAstructure is installed and available in your PATH.
"""

import argparse
import csv
import os
import subprocess
from pathlib import Path


def read_sequence(seq_path: Path) -> str:
    """Return the nucleotide sequence from a FASTA file."""
    fullsequence = []
    with seq_path.open() as seqread:
        for line in seqread:
            line = line.rstrip()
            if not line or line.startswith(">"):
                continue
            fullsequence.append(line.replace(" ", ""))
    return "".join(fullsequence)


def run_partition(seq_path: Path, pfs_path: Path, temperature: float, constraint_path: Path | None = None) -> None:
    """Run RNAstructure partition function with optional constraint file."""
    cmd = [
        "partition",
        str(seq_path),
        str(pfs_path),
        "-t",
        f"{temperature}",
    ]
    if constraint_path:
        cmd.extend(["-c", str(constraint_path)])
    subprocess.check_call(cmd)


def ensemble_energy(pfs_path: Path) -> float:
    """Return ensemble energy from RNAstructure output."""
    efe = subprocess.check_output(["EnsembleEnergy", str(pfs_path), "--silent"])
    efe_list = efe.decode().split()
    return float(efe_list[4])


def write_constraint(constraint_path: Path, position: int) -> None:
    """Write constraint file that forces the provided position to be single stranded."""
    with constraint_path.open("w") as constraint:
        constraint.write("DS:\n")
        constraint.write("-1\n")
        constraint.write("SS:\n")
        constraint.write(f"{position}\n")  # RNAstructure uses 1-indexed positions
        constraint.write("-1\n")
        constraint.write("mod:\n")
        constraint.write("-1\n")
        constraint.write("Pairs:\n")
        constraint.write("-1 -1\n")
        constraint.write("FMN:\n")
        constraint.write("-1\n")
        constraint.write("Forbids:\n")
        constraint.write("-1 -1\n")


def process_sequence(seq_path: Path, temperature: float, output_csv: Path) -> None:
    """Compute DDG for all A/C nucleotides and write results to CSV."""
    sequence = read_sequence(seq_path)
    pfs_path = seq_path.with_suffix(seq_path.suffix + ".pfs")
    constraint_path = Path("constraint.con")

    run_partition(seq_path, pfs_path, temperature)
    base_energy = ensemble_energy(pfs_path)

    with output_csv.open("w", newline="") as outwrite:
        writer = csv.writer(outwrite)
        writer.writerow(["site", "base", "dG"])

        for nucposition, base in enumerate(sequence, start=1):
            if base not in {"A", "C"}:
                continue

            write_constraint(constraint_path, nucposition)
            run_partition(seq_path, pfs_path, temperature, constraint_path)
            constrained_energy = ensemble_energy(pfs_path)
            ddg = constrained_energy - base_energy

            writer.writerow([nucposition, base, f"{ddg:.2f}"])

    if constraint_path.exists():
        constraint_path.unlink()
    
    if pfs_path.exists():
        pfs_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute partition function DDG for nucleotides made single-stranded."
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input FASTA file",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        required=True,
        help="Temperature (Kelvin) to pass to RNAstructure",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output CSV file. Defaults to <input_basename>_ensemble.csv",
        default=None,
    )
    args = parser.parse_args()

    seq_path = Path(args.input)
    if not seq_path.exists():
        raise FileNotFoundError(f"Input FASTA not found: {seq_path}")

    output_csv = Path(args.output) if args.output else Path(
        f"{seq_path.stem}_ensemble.csv"
    )

    process_sequence(seq_path, args.temperature, output_csv)
    print(f"Wrote results to {output_csv}")


if __name__ == "__main__":
    main()
