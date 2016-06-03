import numpy as np

def pella_s(Z, line_select, target_name):
	#FUNCTION pella_s, Z, line_select, target_name
	#
	
	if(len(target_name) == 0):
		target_name = ' '

	CuK_fact = 0.27

	if line_select == 'Ka':
		ap = 3220000.
		bp = 97600.
		dp = -0.39
		# Special for Beryllium
		# 6/14/94  Use 5kV  C data for this tweak, as a guess
		if (Z == 4):
			ap = 30. * ap
			dp = 30. * dp
		# Special for Boron
		# Copy Carbon values...
		if (Z == 5):
			ap = 30. * ap
			dp = 30. * dp
		# Special for Carbon
		# 6/14/94  Use 5kV  C data for this tweak
		if (Z == 6):
			ap = 30. * ap
			dp = 30. * dp
		# Special for MgO
		# 6/14/94  Use 5kV MgO data for this tweak
		if (Z == 12 or target_name == 'MgO'):
			ap = 2.4 * ap
			dp = 2.4 * dp
		# Special for Aluminum
		# 6/14/94  Use 5kV  Al data for this tweak
		if (Z == 13):
			ap = 3.0 * ap
			dp = 3.0 * dp
		# For Si use Special for Aluminum
		# 6/14/94  Use 5kV  Al data for this tweak
		if (Z == 14):
			ap = 3.0 * ap
			dp = 3.0 * dp
		# Special for Ti
		# 12/21/94  Use 9kV  Ti data for this tweak
		if (Z == 22):
			ap = 1.05 * ap
			dp = 1.05 * dp
		# Special for Nickel - use Cu values
		if (Z == 28):
			ap = 0.27 * ap
			dp = 0.27 * dp
		# Special for Copper
		# 7/1/94  Use 9.8kV  Cu data for this tweak
		if (Z == 29):
			ap = CuK_fact * ap
			dp = CuK_fact * dp

	elif line_select == 'Kb':
		ap = 513000.
		bp = 205000.
		dp = -0.014
		# Special for MgO
		# 6/14/94  Use 5kV MgO data for this tweak
		if (Z == 12 or target_name == 'MgO'):
			ap = 2.4 * ap
			dp = 2.4 * dp
		# Special for Aluminum
		# 6/14/94  Use 5kV  Al data for this tweak
		if (Z == 13):
			ap = 3.0 * ap
			dp = 3.0 * dp
		# Special for Ti
		# 12/21/94  Use 9kV  Ti data for this tweak
		if (Z == 22):
			ap = 1.33 * ap
			dp = 1.33 * dp
		# Special for Copper
		# 7/1/94  Use 9.8kV  Cu data for this tweak
		if (Z == 29):
			ap = CuK_fact * ap
			dp = CuK_fact * dp

	elif line_select == 'La':
		ap = 20200000.
		bp = 2650000.
		dp = 0.21
		# Special for MgO - giant kludge to do a compound!
		# 6/14/94  Use 5kV MgO data for this tweak
		if (target_name == 'MgO'):
			ap = 12. * ap
			dp = 12. * dp
		# Special for AlO - giant kludge to do a compound!
		# Upper limit to O line strength due to smd Al.941028.pha data
		if (target_name == 'AlO'):
			ap = 0.5 * ap
			dp = 0.5 * dp
		# Special for SiO - giant kludge to do a compound!
		if (target_name == 'SiO'):
			ap = 50. * ap
			dp = 50. * dp
		# Special for Ti
		# 6/16/94  Use 5kV Ti data for this tweak
		if (Z == 22):
			ap = 3.6 * ap
			dp = 3.6 * dp
		# Special for Cr
		# 6/16/94  Use 5kV Cr data for this tweak
		if (Z == 24):
			ap = 4.5 * ap
			dp = 4.5 * dp
		# Special for Fe
		# 6/5/95  Use 10kV Fe data for this tweak
		if (Z == 26):
			ap = 4.25 * ap
			dp = 4.25 * dp
		# Special for Cu
		# 6/16/94  Use 5kV Cu data for this tweak
		if (Z == 29):
			ap = 4. * ap
			dp = 4. * dp
		# Special for Nb
		#  copied from Mo
		if (Z == 41):
			ap = 0.6*3.3 * ap
			dp = 0.6*3.3 * dp
		# Special for Mo
		# 6/16/94  Use 5kV Mo data for this tweak
		# 12/21/94 Use 9kV Mo data for this tweak
		if (Z == 42):
			ap = 0.6*3.3 * ap
			dp = 0.6*3.3 * dp
		# Special for Ag
		#  copied from Mo
		if (Z == 47):
			ap = 0.6*3.3 * ap
			dp = 0.6*3.3 * dp
		# Special for Sn
		#  copied from Mo
		if (Z == 50):
			ap = 0.6*3.3 * ap
			dp = 0.6*3.3 * dp

	elif line_select == 'Lb':
		ap = 17600000.
		bp = 6050000.
		dp = -0.09
		# Special for Ti
		# 6/16/94  Use 5kV Ti data for this tweak
		if (Z == 22):
			ap = 3.6 * ap
			dp = 3.6 * dp
		# Special for Cr
		# 6/16/94  Use 5kV Cr data for this tweak
		if (Z == 24):
			ap = 4.5 * ap
			dp = 4.5 * dp
		# Special for Cu
		# 6/16/94  Use 5kV Cu data for this tweak
		if (Z == 29):
			ap = 4. * ap
			dp = 4. * dp
		# Special for Nb
		#   copied from Mo
		if (Z == 41):
			ap = 0.6*3.3 * ap
			dp = 0.6*3.3 * dp
		# Special for Mo
		# 6/16/94  Use 5kV Mo data for this tweak
		# 12/19/94 data too
		if (Z == 42):
			ap = 0.6*3.3 * ap
			dp = 0.6*3.3 * dp
		# Special for Ag
		#   copied from Mo
		if (Z == 47):
			ap = 0.6*3.3 * ap
			dp = 0.6*3.3 * dp
		# Special for Sn
		#   copied from Mo
		if (Z == 50):
			ap = 0.6*3.3 * ap
			dp = 0.6*3.3 * dp

	elif line_select == 'Ma':
		ap = 20200000.
		bp = 2650000.
		dp = 0.21
		if(Z == 42):
			ap = 18. * ap
			dp = 18. * dp
		if(Z == 74):
			ap = 8. * ap
			dp = 8. * dp

	elif line_select == 'Mb':
		ap = 17600000.
		bp = 6050000.
		dp = -0.09
		if(Z == 42):
			ap = 18. * ap
			dp = 18. * dp
		if(Z == 74):
			ap = 8. * ap
			dp = 8. * dp

	else:
		print ' labx_linetoc: no information on line type = ' + line_select
		return 0.

	fp = (ap/(bp+Z**4)+dp)

	return fp


def pella_rprime(U):
	#FUNCTION pella_rprime, U
	exponent = -0.5*((U-1)/(1.17*U+3.2))**2
	return np.exp(exponent)


def pella_tau(U):
	#FUNCTION pella_tau, U
	return (U*np.log(U)/(U-1.)) - 1.
