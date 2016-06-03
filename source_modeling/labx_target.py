def labx_target(spec):
	#PRO labx_target
	#
	# This procedure sets up the parameters for an x-ray target using
	# the characters in spec.tName as the input.
	#
	# 4/15/93 - dd
	# 12/21/94 dd Update energies from Bearden

	#@labx_common

	# Default target
	#if spec.tName not in globals():
	#	spec.tName = 'Cu'

	# Setup other constants needed - NOW DONE IN spec INIT
	#spec.akev = 12.39824		# keV Angstrom* product
	#spec.electron = 1.602E-19
	#spec.espermA = 0.001/spec.electron
	#spec.melectron = 9.11E-28
	#spec.mproton = 1.673E-24
	
	# Setup target values as desired.
	
	if spec.tName == 'Be':
		spec.tZ = 4.
		spec.tA = 9.012
		spec.trho = 1.85 # 
		# lines from this target
		spec.tEKa = 0.1085
		spec.tEKb = -1
		spec.tELa = -1
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'B':
		spec.tZ = 5.
		spec.tA = 10.81
		spec.trho = 2. # Guess
		# lines from this target
		spec.tEKa = 0.1833
		spec.tEKb = -1
		spec.tELa = -1
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'C':
		spec.tZ = 6.
		spec.tA = 12.01
		spec.trho = 2.15 # Graphite
		# lines from this target
		spec.tEKa = 0.277366
		spec.tEKb = -1
		spec.tELa = -1
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1
	
	elif spec.tName == 'O':
		spec.tZ = 8.
		spec.tA = 16.0
		spec.trho = 4.26 # TiO2
		# lines from this target
		spec.tEKa = 0.524904
		spec.tEKb = -1
		spec.tELa = -1
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Mg':
		spec.tZ = 12.
		spec.tA = 24.3
		spec.trho = 1.74
		# lines from this target
		spec.tEKa = 1.25361
		spec.tEKb = 1.30220
		spec.tELa = -1
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	# Super-d-duper kludge to get MgO spectrum - what a hacker!
	elif spec.tName == 'MgO':
		spec.tZ = 12.
		spec.tA = 24.3
		spec.trho = 1.74
		# lines from this target
		spec.tEKa = 1.25361
		spec.tEKb = 1.30220
		spec.tELa = 0.524904
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Al':
		spec.tZ = 13.
		spec.tA = 26.98
		spec.trho = 2.7
		# lines from this target
		spec.tEKa = 1.48629
		spec.tEKb = 1.55757
		spec.tELa = -1
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1
	
	# Super-d-duper kludge to get AlO spectrum - what a hacker!
	elif spec.tName == 'AlO':
		spec.tZ = 13.
		spec.tA = 26.98
		spec.trho = 2.7
		# lines from this target
		spec.tEKa = 1.48629
		spec.tEKb = 1.55757
		spec.tELa = 0.524904
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Si':
		spec.tZ = 14.
		spec.tA = 28.08
		spec.trho = 2.32
		# lines from this target
		spec.tEKa = 1.73998
		spec.tEKb = 1.83594
		spec.tELa = -1
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1
	
	# Super-d-duper kludge to get SiO2 spectrum - what a hacker!
	elif spec.tName == 'SiO':
		spec.tZ = 14.
		spec.tA = 28.08
		spec.trho = 2.32
		# lines from this target
		spec.tEKa = 1.73998
		spec.tEKb = 1.83594
		spec.tELa = 0.524904
		spec.tELb = -1
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Ti':
		spec.tZ = 22.
		spec.tA = 47.9
		spec.trho = 4.5
		# lines from this target
		spec.tEKa = 4.51090
		spec.tEKb = 4.93186
		spec.tELa = 0.452160
		spec.tELb = 0.458345
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Cr':
		spec.tZ = 24.
		spec.tA = 52.
		spec.trho = 7.14
		# lines from this target
		spec.tEKa = 5.41479
		spec.tEKb = 5.94677
		spec.tELa = 0.572932
		spec.tELb = 0.582898
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Fe':
		spec.tZ = 26.
		spec.tA = 56.
		spec.trho = 7.87
		# lines from this target
		spec.tEKa = 6.400
		spec.tEKb = 7.059
		spec.tELa = 0.704
		spec.tELb = 0.717
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Ni':
		spec.tZ = 28.
		spec.tA = 58.69
		spec.trho = 8.90
		# lines from this target
		spec.tEKa = 7.47815
		spec.tEKb = 8.26466
		spec.tELa = 0.8515
		spec.tELb = 0.8688
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Cu':
		spec.tZ = 29.
		spec.tA = 63.5
		spec.trho = 8.96
		# lines from this target
		spec.tEKa = 8.04787
		spec.tEKb = 8.90539
		spec.tELa = 0.929682
		spec.tELb = 0.949838
		spec.tEMa = -1
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Zr': 
		spec.tZ = 40.
		spec.tA = 91.22
		spec.trho = 6.52
		# lines from this target
		spec.tEKa = 15.746
		spec.tEKb = 17.6678
		spec.tELa = 2.04236
		spec.tELb = 2.1244
		spec.tEMa = 0.170
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Nb': 
		spec.tZ = 41.
		spec.tA = 92.9
		spec.trho = 8.57
		# lines from this target
		spec.tEKa = 16.6151
		spec.tEKb = 18.6225
		spec.tELa = 2.16589
		spec.tELb = 2.2574
		spec.tEMa = 0.180
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Mo': 
		spec.tZ = 42.
		spec.tA = 95.9
		spec.trho = 10.2
		# lines from this target
		spec.tEKa = 17.4795
		spec.tEKb = 19.6085
		spec.tELa = 2.29319
		spec.tELb = 2.4
		spec.tEMa = 0.193
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Ag': 
		spec.tZ = 47.
		spec.tA = 107.868
		spec.trho = 10.5
		# lines from this target
		spec.tEKa = 22.1629
		spec.tEKb = 24.94
		spec.tELa = 2.9843
		spec.tELb = 3.1509
		spec.tEMa = 0.3
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'Sn': 
		spec.tZ = 50.
		spec.tA = 118.71
		spec.trho = 7.28
		# lines from this target
		spec.tEKa = 25.2713
		spec.tEKb = 28.4860
		spec.tELa = 3.44398
		spec.tELb = 3.6628
		spec.tEMa = 0.4
		spec.tEMb = -1
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	elif spec.tName == 'W':
		spec.tZ = 74.
		spec.tA = 183.9
		spec.trho = 19.35
		# lines from this target
		spec.tEKa = 58.864
		spec.tEKb = 67.586
		spec.tELa = 8.396
		spec.tELb = 9.959
		spec.tEMa = 1.775
		spec.tEMb = 1.835
		# line fluxes, -1 if not defines/calculated 
		spec.FlKa = -1
		spec.FlKb = -1
		spec.FlLa = -1
		spec.FlLb = -1
		spec.FlMa = -1
		spec.FlMb = -1

	else:
		print ' labx_target: No information on target: ' + spec.tName
