#!/bin/bash

# This script runs the global fitting of the distributions of the EKC.01.061.analyze_fit_distributions module.

# create sqlite db
# global_refit_results = pd.DataFrame(store_results, columns=['site', 'log_kappa', 'log_kdeg', 'log_fmod_0', 'r2', 'stderr_log_kappa', 'stderr_log_kdeg', 'stderr_log_fmod_0'])
# global_refit_results['rg_id'] = rg_id

glob_results_db=/projects/b1044/Computational_Output/EKC/EKC.01_SHAPE_standardization/EKC.01.061.analyze_fit_distributions/global_refit_results.db

# create table
# sqlite3 $glob_results_db <<EOF
# CREATE TABLE IF NOT EXISTS global_refit_results (
#     site INTEGER,
#     log_kappa REAL,
#     log_kdeg REAL,
#     log_fmod_0 REAL,
#     r2 REAL,
#     stderr_log_kappa REAL,
#     stderr_log_kdeg REAL,
#     stderr_log_fmod_0 REAL,
#     rg_id INTEGER
# );
# EOF

main_db=/projects/b1044/Computational_Output/EKC/EKC.01_SHAPE_standardization/EKC.01.060.developing_DB_input/new.db
rg_ids=$(sqlite3 $main_db "
    SELECT DISTINCT rg.rg_id
    FROM reaction_groups rg
    WHERE rg.rg_id IN (
        SELECT rg.rg_id
        FROM probing_reactions pr
        JOIN fmod_vals fv ON pr.id = fv.rxn_id
        JOIN nucleotides n ON fv.nt_id = n.id
        JOIN constructs c ON pr.construct_id = c.id
        JOIN sequencing_samples ss ON pr.s_id = ss.id
        JOIN reaction_groups rg ON rg.rxn_id = pr.id
        JOIN sequencing_runs sr ON ss.seqrun_id = sr.id
        WHERE pr.reaction_time IN (
            SELECT pr2.reaction_time
            FROM probing_reactions pr2
            GROUP BY pr2.reaction_time
            HAVING COUNT(DISTINCT pr2.id) > 1
        )
        AND fv.fmod_val IS NOT NULL
        AND pr.RT = 'MRT'
        AND fv.valtype = 'modrate'
    );
")
echo $rg_ids
rg_ids_array=($rg_ids)
# rg_id=${rg_ids_array[2]}

# python /projects/b1044/Computational_Output/EKC/EKC.01_SHAPE_standardization/EKC.01.061.analyze_fit_distributions/fitting_module/timecourse_fitting.py $rg_id $glob_results_db

# run global fitting for each rg_id
for rg_id in $rg_ids; do
    echo "Running global fitting for rg_id: $rg_id"
    time python -u /projects/b1044/Computational_Output/EKC/EKC.01_SHAPE_standardization/EKC.01.061.analyze_fit_distributions/fitting_module/timecourse_fitting.py $rg_id $glob_results_db
done