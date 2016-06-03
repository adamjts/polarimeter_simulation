import numpy as np

from pella import pella_s, pella_rprime, pella_tau


class SourceSpectrum(object):
	def __init__(self, material, V, I):
		# Setup energies for the continuum, etc.
		self.emax = 10.0	  # keV
		self.emin = 0.10	  # keV
		self.estep = 0.010	  # keV
		self.tName = material
		self.lines_off = 0
		self.tEKa = 0
		self.tEKb = 0
		self.tELa = 0
		self.tELb = 0
		self.tEMa = 0
		self.tEMb = 0
		self.FlKa = 0
		self.FlKb = 0
		self.FlLa = 0
		self.FlLb = 0
		self.FlMa = 0
		self.FlMb = 0
		self.es = 0
		self.tubespec = 0
		self.sI = I
		self.tZ = 0
		self.tA = 0
		self.trho = 0
		self.sV = V   # kV
		self.akev = 12.39824		# keV Angstrom* product
		self.electron = 1.602E-19
		self.espermA = 0.001/self.electron
		self.melectron = 9.11E-28
		self.mproton = 1.673E-24


def labx_linetoc(spec, E, line_select):
	#stuff labx_linetoc(spec.tEKa,'Ka')
	#FUNCTION labx_linetoc, E, line_select
	#
	# This function calculates the line-to-continuum ratio for a given
	# line type (Kalpha, etc.) using eq. (35) in Pella et al.
	#
	# 4/15/93 - dd
	#
	
	# Over voltage ratio
	
	U = spec.sV/E
	
	# Basic line to coninuum ratio
	S = pella_s(spec.tZ, line_select, spec.tName)

	# R' is small correction
	linetoc = 1000.*(E*E/spec.akev) * pella_rprime(U) * S * pella_tau(U)

	return linetoc


def labx_tubeinuum(spec, E):
	#FUNCTION labx_tubeinuum, E
	
	# Simple Kramer's equation: (photons/sec per eV per steradian)
	# photons/sec/eV/steradian = 1/(4pi steradian) * K * (photons/electron/eV) * electrons/sec
	flux = 1./(4*np.pi) * 2.2e-9 * spec.tZ * ((spec.sV/E)-1) * spec.espermA * spec.sI

	# DO NOT use for now
	# Include self absorbtion (eq. (17) from Pella et al.)
	# continuum = flux*pella_selfabs(E)

	continuum = flux

	# Set any values that are less than zero to zero
	continuum *= (continuum > 0.)

	return continuum


def labx_tubelines(spec):
	#PRO labx_tubelines
	#
	# This procedure calculates the intensity of the lines from a source
	# based on the continuum value and the line-to-continuum ratio.
	# The line fluxes (phots/sec steradian) are left in the common
	# variables spec.FlKa, etc.
	#
	# 4/15/93 - dd
	#

	if(spec.tEKa > 0.):
		spec.FlKa = labx_linetoc(spec, spec.tEKa, 'Ka')*labx_tubeinuum(spec, spec.tEKa)
	if(spec.tEKb > 0.):
		spec.FlKb = labx_linetoc(spec, spec.tEKb, 'Kb')*labx_tubeinuum(spec, spec.tEKb)
	if(spec.tELa > 0.):
		spec.FlLa = labx_linetoc(spec, spec.tELa, 'La')*labx_tubeinuum(spec, spec.tELa)
	if(spec.tELb > 0.):
		spec.FlLb = labx_linetoc(spec, spec.tELb, 'Lb')*labx_tubeinuum(spec, spec.tELb)
	if(spec.tEMa > 0.):
		spec.FlMa = labx_linetoc(spec, spec.tEMa, 'Ma')*labx_tubeinuum(spec, spec.tEMa)
	if(spec.tEMb > 0.):
		spec.FlMb = labx_linetoc(spec, spec.tEMb, 'Mb')*labx_tubeinuum(spec, spec.tEMb)
