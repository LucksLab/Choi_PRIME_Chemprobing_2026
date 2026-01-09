#!/bin/zsh

# 4U WT
./get_coords "AGGUUGAACUUUUGAAUAGUGAUUCAGGAGGUUAAUGGAAG" "..(((((.(((((((((....))))))))).)))))....." "fourU_WT.csv"

# 4U A8C
./get_coords "AGGUUGACCUUUUGAAUAGUGAUUCAGGAGGUUAAUGGAAG" "..(((((((((((((((....)))))))))))))))....." "fourU_A8C.csv"

# HIV WT
./get_coords "TAAGGCAGATCTGAGCCTGGGAGCTCTCTGCCAATCC" "...((((((...((((......))))))))))....." "hiv_WT.csv"

# HIV A35G
./get_coords "TAAGGCAGATCTGAGCCTGGGGGCTCTCTGCCAATCC" "...((((((...(((((....)))))))))))....." "hiv_A35G.csv"

# HIV C30U
./get_coords "TAAGGCAGATCTGAGCTTGGGAGCTCTCTGCCAATCC" "...((((((...(((((....)))))))))))....." "hiv_C30U.csv"

# HIV UUCG
./get_coords "TAAGGCAGATCTGAGCTTGGGAGCTCTCTGCCAATCC" "...((((((...(((((....)))))))))))....." "hiv_UUCGES.csv"

# HIV UUCG GS
./get_coords "TAAGGCAGATCTGAGCTTCGGCTCTCTGCCAATCC" "...((((((...((((....))))))))))....." "hiv_UUCGGS.csv"

# P4P6 bc
./get_coords "AAAGGAATTGCGGGAAAGGGGTCAACAGCCGTTCAGTACCAAGTCTCAGGGGAAACTTTGAGATGGCCTTGCAAAGGGTATGGTAATAAGCTGACGGACATGGTCCTAACCACGCAGCCAAGTCCTAAGTCAACAGATCTTCTGTTGATATGGATGCAGTTCAACCAAATCAAAAAACCGCCTAGTTCGCTAGGCGGAAAA" "....(...((((((...((((((.....(((.((((.(((..(((((((((....)))))))))..(((.....)))....)))......)))))))....))))))..)).))))..)..((((..((((((((((...))))))))).)))))......................((((((((....))))))))...." "p4p6_bc.csv"

# P4P6 no_bc
./get_coords "AAAGGAATTGCGGGAAAGGGGTCAACAGCCGTTCAGTACCAAGTCTCAGGGGAAACTTTGAGATGGCCTTGCAAAGGGTATGGTAATAAGCTGACGGACATGGTCCTAACCACGCAGCCAAGTCCTAAGTCAACAGATCTTCTGTTGATATGGATGCAGTTCAACCAAATCA" "....(...((((((...((((((.....(((.((((.(((..(((((((((....)))))))))..(((.....)))....)))......)))))))....))))))..)).))))..)..((((..((((((((((...))))))))).)))))................." "p4p6_nobc.csv"