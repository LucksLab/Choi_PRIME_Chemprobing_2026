### Rationale
Want $k_{add}$ comparisons against DMS data. For the fourU thermometer, I only have solid single-stranded data on A, G, and U. How would ATP/GTP compare against ---A/G--- in a loop? Is measured UTP real? UTP isn't supposed to be reactive at this pH...nor is GTP. 

### Hypothesis
- Very low amounts of methylation detected with 2D HSQC of 1 mM UTP. I hypothesize that there's modification happening with U's but just at significantly low amounts. 
	- I just my probing data because reactivity profile curve fits are very good. Temperature-dependence also show strong linearity.
	- Challenge is to actually measure this rate. 1 mM UTP seems too weak to get this, would need to increase.
- GTP modifies at two positions (at least). Tony believes that GTP I'm detecting is not real or just noise. I suspect that MarathonRT is detecting m1G (similarly low levels as m3U), but need to somehow show that this is the case. If I can separately quantify m1G vs m7G, then I could see where DMS G kadd sits. It's possible that m1G and m7G rates are similar, but just in different proportions. 
- ATP appears to primarily be modified at 1 position. So, ATP adduction should be most directly comparable to DMS A kadd. 

### Planning a reasonable set of experiments
- 5 mM GTP - 37°C
	- Goal to capture m1G / m7G kinetics separately
- 5 mM UTP - 37°C
	- Goal to see if I can even quantify modification rates
- 5 mM ATP -  25°C, 37°C, 45°C, 48°C, 
	- Need to make sure ATP kinetics doesn't get cut off at the start

### Trial 65°C ATP
- Workflow:
	- Prep everything except DMS (675 µL)
	- Transfer 550 µL to NMR tube.
	- Pre-incubate for 5 mins.
	- Lock, tune, shim, gain
	- Extract sample
	- Start reaction (note time too) + 55 µL 1.5% DMS
		- Mix by inverting
	- Insert sample
	- Shim
	- Start multi_zgvd
		- Start with 16 scans
		- 

| Components        | Vol. (µL) |     |
| ----------------- | --------- | --- |
| 5X folding buffer | 150       |     |
| D2O               | 75        |     |
| 1.5% DMS          | 75        |     |
| ddH2O             | 442.5     |     |
| NTP (100 mM)      | 7.5       |     |
| **Total**         | 750       |     |