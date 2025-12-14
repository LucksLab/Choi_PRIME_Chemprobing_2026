
### Rationale
Want to get temp-dependence k_add curves for ATP and GTP (bonus CTP and UTP).

### Reaction setup

- 5 mM NTP in 0.15% DMS reaction
- folding buffer is Schwalbe buffer
- Using deuterated ethanol

| Components   | Vol. (µL) |
| ------------ | --------- |
| 100% d6-EtOH | 98.5      |
| 100% DMS     | 1.5       |
| **Total**    | 100       |

| Components        | Vol. (µL) |
| ----------------- | --------- |
| 5X folding buffer | 150       |
| D2O               | 75        |
| 1.5% DMS          | 75        |
| ddH2O             | 412.5     |
| NTP (100 mM)      | 37.5      |
| **Total**         | 750       |

- ATPs:
	- 30_1 (not done), 20_1, 20_2, 37_1, 37_2, 42_1, 42_2, 48_1, 48_2
- GTPs:
	- 20_1, 37_1, 37_2, 42_1, 42_2, 48_1, 48_2
- UTPs:
	- 20_1, 30_1 (made this for 2D HSQC)
- CTPs:
	- 20_1

**Preparing reagents**
1. Prep pre-reaction mix (everything except DMS) individually.
2. Prep 1.5% DMS. (closer to reaction)
	- This is left at RT or 4°C not at 37°C to prevent excessive evaporation.

**Temperature pre-equilibration**
1. Pre-warm NMR tube inside the NMR machine (A600 or HFCN600).
2. Equilibrate pre-reaction mix to 37°C and bring warmed tubes to IMSERC.

**Reaction initiation**
1. Initiate reaction by adding 75 µL 1.5% DMS into pre-reaction mix.
2. Mix by inverting and note reaction start time.
3. Release NMR tube from machine that has been pre-warming.
4. Transfer 550 µL reaction into NMR tube and insert back into NMR machine (as quickly as possible).
5. Pre-incubate for 3 minutes before locking, tuning, shimming. 
	1. Note gain and use for others.
6. Initiate multi-zgvd program (kinetic reads).

### Experiments
*All at pH 6.5 (temp-adjusted), 0.15% DMS, Schwalbe buffer*
1. 5 mM ATP 37°C rep 1
	- Reaction start: 2024-04-12T18:45:00
	- Acquisition start: 2024-04-12T18:53:03
	- Time offset (seconds): 483
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 15 s delay (2.5 min total), 36 reads (1.5 hrs)
2. 5 mM ATP 37°C rep 2
	- Reaction start: 2024-04-12T20:29:42
	- Acquisition start: 2024-04-12T20:36:55
	- Time offset (seconds): 433
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 15 s delay (2.5 min total), 36 reads (1.5 hrs)
3. 5 mM ATP 20°C rep 1
	- Reaction start: 2024-04-13T01:27:47
	- Acquisition start: 2024-04-13T01:44:05
	- Time offset (seconds): 978.0
	- mnova fit for DMS: XXX
	- Setting: 152 scans, 16 s delay (10 min total), 60 reads (10 hrs)
	- A500 (gain 32.00)
1. 5 mM ATP 42°C rep 1
	- Reaction start: 2024-04-13T20:31:40
	- Acquisition start: 2024-04-13T20:39:50
	- Time offset (seconds): 490
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 15 s delay (2.5 min total), 36 reads (1.5 hrs)
2. 5 mM ATP 42°C rep 2
	- Reaction start: 2024-04-13T21:31:41
	- Acquisition start: 2024-04-13T21:38:25
	- Time offset (seconds): 404
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 15 s delay (2.5 min total), 36 reads (1.5 hrs)
3. 5 mM ATP 48°C rep 1
	- Reaction start: 2024-04-13T22:26:26
	- Acquisition start: 2024-04-13T22:31:14
	- Time offset (seconds): 288
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 15 s delay (2.5 min total), 36 reads (1.5 hrs)
4. 5 mM ATP 48°C rep 2
	- Reaction start: 2024-04-13T23:06:37
	- Acquisition start: 2024-04-13T23:12:42
	- Time offset (seconds): XXX
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 15 s delay (2.5 min total), 36 reads (1.5 hrs)
5. 5 mM UTP 20°C rep 1
	- Reaction start: 2024-04-13T00:02:43
	- Acquisition start: 2024-04-13T00:13:30
	- HFCN600 (gain 50.80)
	- Time offset (seconds): 647
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 58 s delay (5 min total), 120 reads (10 hrs)
6. 5 mM GTP 25°C rep 1
	- Reaction start: 2024-04-13T10:26:31
	- Acquisition start: 2024-04-13T10:45:03
	- Time offset (seconds): 1112.0
	- mnova fit for DMS: XXX
	- Setting: 80 scans, 34 s delay (10 min total), 60 reads (10 hrs)
	- HFCN600 (gain 101 (#1, #2, #3, and #8) then dropped to 50.80 manually for all others)
7. 5 mM UTP 30°C rep 1 (endpoint ONLY)
	- C13CPD
		- Gain 101
		- 64 scans - 4 mins 2s
	- Water suppression
		- Gain 50.80
		- 32 scans - 4 mins 2s
	- C13DEPTQ135
		- Gain 101
		- 256 scans 15 mins 22 s
	- HSQC
		- Gain 101
		- 64 scans 9 hrs
	- Realized that I did not use 13C DMS for this...
1. 5 mM CTP 25°C rep 1
	- Reaction start: 2024-04-13T23:52:40
	- Acquisition start: 2024-04-14T00:09:23
	- Time offset (seconds): 1003
	- mnova fit for DMS: XXX
	- Setting: 152 scans, 44 s delay (10 min total), 60 reads (10 hrs)
	- A600 (gain 45.20)
2. 5 mM CTP 37°C rep 1
	- Reaction start: 2024-04-14T11:27:43
	- Acquisition start: 2024-04-14T11:35:28
	- Time offset (seconds): 465
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 15 s delay (2.5 min total), 36 reads (1.5 hrs)
	- A600 (gain XXX)
3. 5 mM GTP 33°C rep 1
	- Reaction start: 2024-04-14T10:57:29
	- Acquisition start: 2024-04-14T11:23:53
	- Time offset (seconds): 1584.0
	- mnova fit for DMS: XXX
	- Setting: 36 scans, 31 s delay (5 min total), 24 reads (2 hrs)
	- HFCN (gain 45.20)
4. 5 mM CTP 37°C rep 2
	- Reaction start: 2024-04-14T13:07:16
	- Acquisition start: 2024-04-14T13:14:32
	- Time offset (seconds): 436
	- mnova fit for DMS: XXX
	- Setting: 32 scans, 15 s delay (2.5 min total), 36 reads (1.5 hrs)
	- A600 (gain )
5. 5 mM GTP 42°C rep 1
	- Reaction start: 2024-04-14T13:13:09
	- Acquisition start: 2024-04-14T13:26:09
	- Time offset (seconds): 780
	- mnova fit for DMS: XXX
	- Setting: 12 scans, 12 s delay (2 min total), 24 reads (48 mins)
	- HFCN (gain 45.20)
6. 5 mM CTP 42°C rep 1
	- Reaction start: 2024-04-14T14:51:03
	- Acquisition start: 2024-04-14T14:57:24
	- Time offset (seconds): 381
	- mnova fit for DMS: XXX
	- Setting: 22 scans, 23 s delay (2 min total), 24 reads (44 mins)
	- A600 (gain 50.8)
7. 5 mM CTP 42°C rep 2
	- Reaction start: 2024-04-14T15:46:35
	- Acquisition start: 2024-04-14T15:53:57
	- Time offset (seconds): 442
	- mnova fit for DMS: XXX
	- Setting: 22 scans, 23 s delay (2 min total), 24 reads (44 mins)
	- A600 (gain 50.8)
8. 5 mM CTP 48°C rep 1
	- Reaction start: 2024-04-14T16:44:59
	- Acquisition start: 2024-04-14T16:50:48
	- Time offset (seconds): 349
	- mnova fit for DMS: XXX
	- Setting: 16 scans, 15 s delay (1.5 min total), 20 reads (30 mins)
	- A600 (gain 50.8)
9. 5 mM CTP 48°C rep 2
	- Reaction start: 2024-04-14T17:25:54
	- Acquisition start: 2024-04-14T17:31:42
	- Time offset (seconds): 348
	- mnova fit for DMS: XXX
	- Setting: 16 scans, 15 s delay (1.5 min total), 20 reads (30 mins)
	- A600 (gain 50.8)
10. 5 mM GTP 48°C rep 2
	- Reaction start: 2024-04-14T18:08:41
	- Acquisition start: 2024-04-14T18:15:01
	- Time offset (seconds): 380
	- mnova fit for DMS: XXX
	- Setting: 16 scans, 15 s delay (1.5 min total), 20 reads (30 mins)
	- A600 (gain 50.8)