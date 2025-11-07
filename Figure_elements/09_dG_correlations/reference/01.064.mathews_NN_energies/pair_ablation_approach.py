#In this file, test that DG DMS correlates with the free energy cost of opening a pair and allowing adjacent
# pairs to stack.  In the Turner rules, this is the same as removing the pair completely.
#Using WT.fasta and A8C.fasta and corresponding ct files, run through each nucleotide and ablate it along with pairing
# partner.  DDG is the free energy difference of ablated and non-ablated.
#This will only work for one specific RNA thermomemeter because of hard coded assumptions for the structure.


import subprocess

#function to extract the free energy change from an efn2 output file
#extract on the dg from structure 1
#input is a string with the filename, return is a string of the free energy
def readenergy(outfilename):
    outfile=open(outfilename)
    #the first line is the free energy for structure #1
    firstline=outfile.readline()
    #the free energy is preceded by =
    start=firstline.find("= ")
    #the free energy is followed by ±
    end=firstline[start+2:].find(" ")
    return firstline[start+2:start+2+end]


inseqs=["WT.fasta","A8C.fasta"]
incts=["WT.ct","A8C.ct"]
outfiles="WTablation.out","A8Cablation.out"

for seq,ct,out in zip(inseqs,incts,outfiles):

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

    # get the folding free energy of the full structure:
    subprocess.call([f'efn2 {ct} tempenergy.out -t 293.15'], shell=True)
    energy = readenergy("tempenergy.out")

    #read the ct file to get all pairing information
    inputct=open(ct)
    firstline = inputct.readline()
    firstspace = firstline.find(" ")
    #ct files are 1 indexed, the pairs list needs to also be 1-indexed, so I placed a 0 for the zero position:
    pairs=[0]
    # now read the nucleotide information
    for line in inputct:
        line.rstrip()
        linelist = line.split()
        #note the last line will be empty (extra carriage return as per unix standards)
        if (len(linelist)>0):
            pairs.append(int(linelist[4]))
    inputct.close()


    #now iterate over the nucleotides in the sequence.  Act on A and C
    for nucposition in range(0,len(fullsequence)):
        #for the stem loop of interest, skip the first nucleotide
        if (fullsequence[nucposition]=="A" or fullsequence[nucposition]=="C") and nucposition!=0:
            #generate a temporary dot-bracket  file with the pairs ablated
            outdb=open("temp.db","w")
            firststring=""
            secondstring=""
            for i in range(1,len(pairs)):
                #now write the pairs
                if i!=(nucposition+1) and i!=(pairs[nucposition+1]): #not the two nucs to ablate
                    # VERY SPECIFIC FOR THIS STEM LOOP
                    #hard wire the "pair" between 8 and 31 (a single mismatch in WT)
                    if not((nucposition+1==8) and (i==8 or i==31)):
                        firststring+=fullsequence[i-1]
                        if pairs[i]>i:
                            secondstring+="("
                        elif pairs[i]==0:
                            secondstring+="."
                        else:
                            secondstring+=")"
            outdb.write(">temp file\n")
            outdb.write(firststring+"\n")
            outdb.write(secondstring+"\n")
            outdb.close()

            # now turn the dot-bracket into a ct file:
            subprocess.call([f'dot2ct temp.db temp.ct'], shell=True)
            subprocess.call([f'efn2 temp.ct tempenergy.out -t 293.15'], shell=True)
            ablateenergy = readenergy("tempenergy.out")

            ddg = float(ablateenergy)-float(energy)

            outwrite.write(str(nucposition+1)+"\t"+fullsequence[nucposition]+"\t"+"{:.2f}".format(ddg)+"\n")
    outwrite.close()