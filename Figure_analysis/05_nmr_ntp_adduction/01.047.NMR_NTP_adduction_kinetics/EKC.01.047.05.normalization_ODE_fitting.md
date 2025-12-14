### Rationale

Goal is to get robust measurements of $k_{add}$ for ATP, GTP, CTP, UTP. Suffer from a major challenge of multiple DMS products. Decided that at this point, I will measure decay in unmodified NTP for this manuscript. This clearly warrants a deeper quantitation of each product, but a rough kadd will suffice as long as it is robust.
  
### Experimental method

- 5 mM (nominal) NTP was probed at various temperatures in pH-adjusted buffer that match probing buffer (150 mM bis-tris (pK<sub>a</sub> 6.35), 15 mM KHPO<sub>4</sub>, 25 mM KCl, pH 6.5
- Reaction started, transferred to a pre-warmed NMR tube, then time-resolved 1D NMR
- All reaction time offsets were measured and adjusted as x-axis offset in the data
- I also more carefully measured concentration of NTPs, so I can use this for ODE's later.

### Mnova analysis

- Used "Reaction monitoring wizard" to import all fids within folders
- Applied auto phase correction and baseline correction
- When necessary, I do baseline correction within the local ppm around the peaks
- Peak assignment TODO
- need to fill in details on what's what for each NTP
- Output here are raw peak integrals for various peaks that were visible

### Peak pre-normalization

- Pre-normalization is taking the dividing each raw peak integral by the sum of all peaks in the 8ppm and 6ppm regions (these correspond to adjacent carbons within the base and sugar).
- Rationale here is that there are baseline correction artifacts during mnova analysis that causes random spikes sometimes.
- Sum of peaks within a region (like around 8ppm) must be linear (or no change), but often this is not the case. This pre-normalization often works well to reveal improved decay curves.
- However, these are NOT true percentages at this point. Peak integral-to-proton ratio is not the same for each of the products, cannot assume that these are percentages although they look like percentages. This is why I'm calling this pre-normalization.
- My primary purpose and goal is: 1) get clean exponential decay curves, 2) use these to estimate max peak integral (this is what's equivalent to 100% of product).
- I will then use this to normalize raw peak integrals to product %.
- I do this for both NTPs and DMS.
- There are varying levels of fit quality for NTP peaks, ideally they would all agree with each other.
- I'll use my best judgement and perhaps some fit criteria to decide on which ones I'll use in my fits.
- Hypothesis is that these rates should obey Arrhenius.
- Pre-normalization is actually done below.

### Data fitting

- Technically I can fit the data to the integrated model. However, at 5 mM NTP (15.64 mM DMS), I feel like I'd be breaking the key assumption. Best to do ODE
- This is what the code below will do

### Results from initial fit
- Looks amazing!! There are a couple that needs to be fixed in mnova (baseline adjustment maybe, there are some random spikes)
- I've gotten agreement between some subset of peak6, peak6_raw, peak8 and peak8_raw. I think all of them are equally valid. I would think raw is stronger..? 
	- Should I just pick one and stick with it?
- We've got linear ln(kadd) vs. 1/T curves, and they are **ABOVE** DMS ln(kapp). This is great! Means we could potentially plug-in.
- But currently, GTP/ATP/CTP doesn't look significantly different. May be down to errors. GTP is definitely capturing N7. 
	- Got this idea of getting the ratio of the peaks at ~2. These are my new -CH3 position specificity. So, use 8ppm 6ppm to get %decay of unmodified NTP. Then use ~2ppm to get regioselectivity.
	- Assume k_add rates are the same, but multiplied by %.

#### ATP
20°C rep 1 peak6
![[20_1_peak6_fit.png]]

20°C rep 1 peak 8
![[20_1_peak8_fit.png]]
20°C rep 1 peak 8 raw
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/20_1_peak8_raw_fit.png]]
37°C rep 1 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/37_1_peak6_fit.png]]
37°C rep 1 peak6 raw
![[37_1_peak6_raw_fit.png]]
37°C rep 1 peak8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/37_1_peak8_fit.png]]

37°C rep 2 peak6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/37_2_peak6_fit.png]]

37°C rep 2 peak8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/37_2_peak8_fit.png]]
42°C rep 1 peak6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/42_1_peak6_fit.png]]

42°C rep 1 peak8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/42_1_peak8_fit.png]]
42°C rep 2 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/42_2_peak6_fit.png]]
42°C rep 2 peak 8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/42_2_peak8_fit.png]]
48°C rep 1 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/48_1_peak6_fit.png]]
48°C rep 1 peak 6 raw
![[48_1_peak6_raw_fit.png]]
48°C rep 1 peak 8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/ATP_peak_percentages/48_1_peak8_fit.png]]
48°C rep 2 peak 6
![[48_2_peak6_fit.png]]
48°C rep 2 peak 6 raw
![[48_2_peak6_raw_fit.png]]
#### CTP
25°C rep 1 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/25_1_peak6_fit.png]]

25°C rep 1 peak8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/25_1_peak8_fit.png]]
25°C rep 1 peak 8 raw
![[25_1_peak8_raw_fit.png]]
37°C rep 1 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/37_1_peak6_fit.png]]
37°C rep 1 peak 8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/37_1_peak8_fit.png]]
37°C rep 2 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/37_2_peak6_fit.png]]
37°C rep 2 peak 8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/37_2_peak8_fit.png]]

42°C rep 1 peak 8
![[42_1_peak8_raw_fit.png]]
42°C rep 1 peak 8 raw
![[42_1_peak8_raw_fit.png]]
42°C rep 2 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/42_2_peak6_fit.png]]
42°C rep 2 peak 6 raw
![[42_2_peak6_raw_fit.png]]
42°C rep 2 peak 8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/42_2_peak8_fit.png]]
42°C rep 2 peak 8 raw fit
![[42_2_peak8_raw_fit.png]]
48°C rep 1 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/48_1_peak6_fit.png]]
48°C rep 1 peak 8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/CTP_peak_percentages/48_1_peak8_fit.png]]
48°C rep2 peak 8
![[48_2_peak8_fit.png]]
48°C rep2 peak 8 raw
![[48_2_peak8_raw_fit.png]]
#### GTP
25°C rep 1 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/GTP_peak_percentages/25_1_peak6_fit.png]]
25°C rep 1 peak 8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/GTP_peak_percentages/25_1_peak8_fit.png]]
33 rep 1 peak 6
![[33_1_peak6_fit.png]]
33 rep 1 peak 6 raw
![[33_1_peak6_raw_fit.png]]
33 rep 1 peak 8
![[33_1_peak8_fit.png]]
33 rep 1 peak 8 raw
![[33_1_peak8_raw_fit.png]]
42 rep 1 peak 6
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/GTP_peak_percentages/42_1_peak6_fit.png]]
48 rep 1 peak 8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/GTP_peak_percentages/48_1_peak8_fit.png]]

### UTP
20 rep 1 peak8
![[EKC.01.047.NMR_NTP_adduction_kinetics/data/peak_analysis/UTP_peak_percentages/20_1_peak8_raw_fit.png]]