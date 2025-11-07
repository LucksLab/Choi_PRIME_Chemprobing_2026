import sqlite3
import glob
import pandas as pd

def extract_info_from_log(log_file, sample_name):
    """
    Extracts information from a ShapeMapper log file.

    Parameters:
        log_file (str): Path to the ShapeMapper log file.
        sample_name (str): Name of the sample to check against the R1 file.

    Returns:
        tuple: Contains the following elements:
            - run_datetime (str): The datetime when the ShapeMapper run started.
            - version (str): The version of ShapeMapper used.
            - r1_file (str): The R1 file used in the run.
            - untreated (int): Indicates if the sample was untreated (1 if untreated, 0 otherwise).
            - denatured (int): Indicates if the sample was denatured (1 if denatured, 0 otherwise).
            - sample_check (bool): Indicates if the sample name matches the R1 file.
    """

    with open(log_file) as f:
        lines = f.readlines()

    # find all lines containing "Started ShapeMapper" and get index of most recent one
    detect_shapemapper_runs = [i for i, line in enumerate(lines) if 'Started ShapeMapper' in line]
    assert len(detect_shapemapper_runs) > 0, 'No ShapeMapper runs detected in log file'

    most_recent_run = detect_shapemapper_runs[-1]
    lines = lines[most_recent_run:]

    # extract date and version from:  "Started ShapeMapper v2.2.0 at 2023-04-22 17:19:59"
    version_date_line = lines[0]
    run_datetime = version_date_line.split(' at ')[1].rstrip()
    version = version_date_line.split(' ')[2]
    run_args = lines[2]
    assert 'args: ' in run_args, 'args line not found in log file'
    
    # get index of 'modified'
    modified_index = run_args.split(' --').index('modified')
    assert modified_index > 0, 'modified not found in run_args'

    # extract R1 file
    r1_file = run_args.split(' --')[modified_index + 1].split(' ')[-1]
    assert (r1_file is not None) or (r1_file == ''), 'R1 file not found in run_args'

    untreated = 0
    denatured = 0
    # check if untreated sample provided
    if 'untreated' in run_args.split(' --'):
        untreated = 1
    elif 'denatured' in run_args.split(' --'):
        denatured = 1

    # confirm sample_name matches r1_file
    sample_check = sample_name in r1_file

    return run_datetime, version, r1_file, untreated, denatured, sample_check

def fetch_s_id(db_file, sample_name):
    """
    Fetches the ID of a sample from the sequencing_samples table.

    Parameters:
        db_file (str): Path to the database file.
        sample_name (str): Name of the sample to fetch the ID for.

    Returns:
        int: The ID of the sample.
    """
    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT id FROM sequencing_samples WHERE sample_name = ?', (sample_name,))
    result = c.fetchall()  # Fetch only one row
    conn.close()

    if result is None:
        raise ValueError(f"No sample found with name: {sample_name}")
    elif len(result) > 1:
        raise ValueError(f"Multiple samples found with name: {sample_name}")
    else:
        return result[0][0]  # Extract ID from tuple

def get_max_id(db_file, table, id_col):
    """
        Fetches the maximum ID from a specified table and column.

        Parameters:
            db_file (str): Path to the database file.
            table (str): Name of the table to query.
            id_col (str): Name of the ID column to find the maximum value.

        Returns:
            int: The maximum ID value plus one, or 1 if the table is empty.
        """
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(f"SELECT MAX({id_col}) FROM {table}")
    max_id = c.fetchone()[0]
    return max_id + 1 if max_id else 1



def fetch_construct_seq(db_file, s_id):
    """
    Fetches the construct sequence for a given sample ID.

    Parameters:
        db_file (str): Path to the database file.
        s_id (int): Sample ID to fetch the construct sequence for.

    Returns:
        str: The construct sequence with T's converted to U's.
    """

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT construct_id FROM probing_reactions WHERE s_id = ?', (s_id,))
    construct_id = c.fetchone()[0]
    c.execute('SELECT sequence FROM constructs WHERE id = ?', (construct_id,))
    construct_seq = c.fetchone()[0]
    dict_convertTU = {'T': 'U', 't': 'u'}
    construct_seq = ''.join([dict_convertTU.get(base, base) for base in construct_seq])
    conn.close()
    return construct_seq

def fetch_rxn_id(db_file, s_id):
    """
    Fetches the reaction ID for a given sample ID.

    Parameters:
        db_file (str): Path to the database file.
        s_id (int): Sample ID to fetch the reaction ID for.

    Returns:
        int: The reaction ID.
    """

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT id, treated FROM probing_reactions WHERE s_id = ?', (s_id,))
    result = c.fetchone()
    conn.close()
    
    rxn_id = result[0]
    treated = result[1]
    return rxn_id, treated

def fetch_nt_ids(db_file, s_id):
    """
    Fetches the nucleotide IDs and sequence for a given sample ID.

    Parameters:
        db_file (str): Path to the database file.
        s_id (int): Sample ID to fetch the nucleotide IDs and sequence for.

    Returns:
        tuple: A tuple containing a list of nucleotide IDs and the nucleotide sequence with T's converted to U's.
    """
    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT construct_id FROM probing_reactions WHERE s_id = ?', (s_id,))
    construct_id = c.fetchone()[0]
    c.execute('SELECT id, base FROM nucleotides WHERE construct_id = ?', (construct_id,))
    selected_nts = sorted(c.fetchall())
    conn.close()

    nt_ids = [nt[0] for nt in selected_nts]
    nt_seq = ''.join([nt[1] for nt in selected_nts])
    dict_convertTU = {'T': 'U', 't': 'u'}
    nt_seq = ''.join([dict_convertTU.get(base, base) for base in nt_seq])
    return nt_ids, nt_seq