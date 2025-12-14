### Rationale
Want to translate NMR kinetic traces to molarity for NTP modification if possible. Want to quantify NTPs to get exact concentration.

### Extinction coefficient of NTPs
- Taken from https://cshprotocols.cshlp.org/content/2006/1/pdb.rec403.full. This is also what I used to quantify rNTP stocks that I made before.

> Dissolve each NTP (ribonucleoside triphosphates) in H2O at an approximate concentration of 100 mM. Use 0.05 M Tris base (or 0.1 N NaOH as appropriate) and a micropipette to adjust the pH of each of the solutions to 7.0 (use pH paper to check the pH). Dilute an aliquot of the neutralized NTP appropriately, and read the optical density at the wavelengths given in the table below. Calculate the actual concentration of each NTP. Dilute the solutions with H2O to a final concentration of 50 mM NTP. Store each separately at -70°C in small aliquots.


| Base | Wavelength (nm) | Extinction Coefficient (E)(M-1cm-1) |
| ---- | --------------- | ----------------------------------- |
| A    | 259             | $1.54 \times 10^4$                  |
| G    | 253             | $1.37 \times 10^4$                  |
| C    | 271             | $0.91 \times 10^4$                  |
| T    | 267             | 9.60 x 103                          |

### Calculating optimal sensitivity for Synergy H1
- Plate reader specs say best precision at 0-2 OD, 200 µL
	- p. 55 https://www.agilent.com/cs/library/packageinsert/public/SynergyH1_IFU_8041005IAW.D.pdf
- ATP OD of 2 at 200 µL
	- $A = \epsilon b C$
	- 5.93 mm or 0.593 cm path length for 200 µL (super rough estimate)
	- 2 = 1.54 x 10^4 x 0.593 x C
	- C = 0.0000219005278 (21.9 µM)
- Ran into trouble because even water was giving OVERFLOW. Then I realized that water absorbs in the UV range. 
- I figured it would be annoying to have to subtract background. I'm sure there's a way because the Take3 plates work for DNA/RNA quantification, but I need a spectra to cover different max absorbance wavelengths for each NTP.
- So I used Nanodrop instead.

### Quantification with NanoDrop
- Turned on automatic pathlength correction.
	- My understanding is if you're very concentrated then the stage will be narrower to get a 'good' reading. This is then adjusted to 10 mm path length when reported. 
	- This makes it difficult to really determine what's true dynamic range? Which dilutions can I trust. 

**Dilution series 1**

| Dilution | Sample    | Vol. (µL) | ddH2O (µL) |
| -------- | --------- | --------- | ---------- |
| 1/10     | undiluted | 2         | 18         |
| 1/20     | 1/10      | 5         | 5          |
| 1/40     | 1/20      | 5         | 5          |
| 1/60     | 1/10      | 1         | 5          |
| 1/100    | 1/10      | 2         | 18         |
| 1/200    | 1/100     | 5         | 5          |
| 1/400    | 1/200     | 5         | 5          |
| 1/600    | 1/100     | 1         | 5          |
**Dilution series 2** (1/10 dilution of Dilution series 1)

| Dilution | Sample | Vol. (µL) | ddH2O (µL) |
| -------- | ------ | --------- | ---------- |
| 1/100    | 1/10   | 1         | 9          |
| 1/200    | 1/20   | 1         | 9          |
| 1/400    | 1/40   | 1         | 9          |
| 1/600    | 1/60   | 1         | 9          |
| 1/1000   | 1/100  | 1         | 9          |
| 1/2000   | 1/200  | 1         | 9          |
| 1/4000   | 1/400  | 1         | 9          |
| 1/6000   | 1/600  | 1         | 9          |
- I ended up taking out 1/6 dilutions (1: 1/60, 1: 1/600, 2: 1/600, 2: 1/6000 because they looked like outliers and they were not serially diluted technically)
- Also took out all 2: 1/100 and 1/1000
- The rest were combined and fitted to a linear regression. 


### ATP
![[ATP_dilution_series.png | 300]]

| Variable                            | Value      |
| ----------------------------------- | ---------- |
| Wavelength at Max Abs. (nm)         | 259        |
| Absorbance (au)                     | 2465.33557 |
| Extinction Coefficient (E)(M-1cm-1) | 1.54E+04   |
| Path Length (cm)                    | 1          |
| Concentration (M)                   | 0.16008673 |
| **Concentration (mM)**              | **160.09** |

### GTP
![[GTP_dilution_series.png | 300]]

| Variable                            | Value      |
| ----------------------------------- | ---------- |
| Wavelength at Max Abs. (nm)         | 252.4      |
| Absorbance (au)                     | 1713.09599 |
| Extinction Coefficient (E)(M-1cm-1) | 1.37E+04   |
| Path Length (cm)                    | 1          |
| Concentration (M)                   | 0.1250435  |
| **Concentration (mM)**              | **125.04** |

### CTP
![[CTP_dilution_series.png | 300]]

| Variable                            | Value      |
| ----------------------------------- | ---------- |
| Wavelength at Max Abs. (nm)         | 265        |
| Absorbance (au)                     | 1338.88544 |
| Extinction Coefficient (E)(M-1cm-1) | 9.10E+03   |
| Path Length (cm)                    | 1          |
| Concentration (M)                   | 0.14713027 |
| **Concentration (mM)**              | **147.13** |

### UTP
![[UTP_dilution_series.png | 300]]

| Variable                            | Value      |
| ----------------------------------- | ---------- |
| Wavelength at Max Abs. (nm)         | 461.496048 |
| Absorbance (au)                     | 1368.4032  |
| Extinction Coefficient (E)(M-1cm-1) | 9.60E+03   |
| Path Length (cm)                    | 1          |
| Concentration (M)                   | 0.142542   |
| **Concentration (mM)**              | **142.54** |

### Final concentrations
- Nominal concentrations were all 100 mM, but these concentrations show they are all more concentrated that labeled. 

| Nucleotide | Concentration (mM) |
| ---------- | ------------------ |
| ATP        | **160.09**         |
| GTP        | **125.04**         |
| CTP        | **147.13**         |
| UTP        | **142.54**         |
