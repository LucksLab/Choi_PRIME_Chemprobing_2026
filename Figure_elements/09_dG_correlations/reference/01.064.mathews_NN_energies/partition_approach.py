# FROM DAVE MATHEWS
# modified to work with unix

#In this file, test that DG DMS correlates with the partition function cost of making one nucleotide unpaired.
#Using WT.fasta and A8C.fasta, run through each nucleotide and force the nucleotide unpaired.  DDG is the ensemble
#free energy cost of forcing a nucleotide unpaired.

import subprocess

inseqs=["WT.fasta","A8C.fasta", "HIV_WT.fasta", "HIV_A35G.fasta", "HIV_C30U.fasta", "HIV_UUCGES.fasta", "HIV_UUCGGS.fasta", "P4P6_wt_nobc.fasta", "P4P6_wt_bc.fasta"]
outfiles="WTensemble.out","A8Censemble.out", "HIV_WTensemble.out", "HIV_A35Gensemble.out", "HIV_C30Uensemble.out", "HIV_UUCGESensemble.out", "HIV_UUCGGSensemble.out", "P4P6_wt_nobcensemble.out", "P4P6_wt_bcensemble.out"

for seq,out in zip(inseqs,outfiles):

    seqread=open(seq)
    outwrite=open(out,"w")
    outwrite.write("nucleotide#\tidentity\tDG\n")

    #read the sequence into fullsequence
    fullsequence=""
    for line in seqread:
        line=line.rstrip()
        if (line[0]!=">"):
            #we are past the sequence name
            line=line.replace(" ","")
            fullsequence+=line
    seqread.close()

    # now run the partition function without constraint:
    subprocess.call([f'partition {seq} {seq}.pfs -t 293.15'], shell=True)
    efe = subprocess.check_output([f'EnsembleEnergy {seq}.pfs --silent'], shell=True)
    efe_list = efe.split()
    eenergy = efe_list[4]

    #now iterate over the nucleotides in the sequence.  Act on A and C
    for nucposition in range(0,len(fullsequence)):
        if fullsequence[nucposition]=="A" or fullsequence[nucposition]=="C":
            #generate a constraint file
            constraint=open("constraint.con","w")
            constraint.write("DS:\n")
            constraint.write("-1\n")
            constraint.write("SS:\n")
            constraint.write(str(nucposition+1)+"\n")#note that RNAstructure treats sequences with 1-indexing
            constraint.write("-1\n")
            constraint.write("mod:\n")
            constraint.write("-1\n")
            constraint.write("Pairs:\n")
            constraint.write("-1 -1\n")
            constraint.write("FMN:\n")
            constraint.write("-1\n")
            constraint.write("Forbids:\n")
            constraint.write("-1 -1\n")

            constraint.close()

            # now run the partition function with constraint:
            subprocess.call([f'partition {seq} {seq}.pfs -c constraint.con -t 293.15'], shell=True)
            constrainedefe = subprocess.check_output([f'EnsembleEnergy {seq}.pfs --silent'], shell=True)
            constrainedefe_list = constrainedefe.split()
            constrainedeenergy = constrainedefe_list[4]

            ddg = float(constrainedeenergy)-float(eenergy)

            outwrite.write(str(nucposition+1)+"\t"+fullsequence[nucposition]+"\t"+"{:.2f}".format(ddg)+"\n")
    outwrite.close()