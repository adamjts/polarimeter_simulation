import numpy as np
import matplotlib.pyplot as plt

from source_spectrum import SourceSpectrum
from labx_tubespec import labx_tubespec

#PRO source_spectrum
#
# Plots the spectrum of the source as configured
#

def createEnergyFunc(sourceType):
	spec = SourceSpectrum(sourceType)

	# Calculate the spectrum - puts it in spec.tubespec,
	#  units of phots/ (sec bin steradian)
	labx_tubespec(spec)

	# units of phots/ (sec bin steradian mA)
	spec.tubespec = spec.tubespec/(spec.sI)
	table = np.zeros((2, len(spec.es)))
	table[0] = spec.es
	table[1] = spec.tubespec
	return table


spec = SourceSpectrum('AlO')

# Calculate the spectrum - puts it in spec.tubespec,
#  units of phots/ (sec bin steradian)
labx_tubespec(spec)

# units of phots/ (sec bin steradian mA)
spec.tubespec = spec.tubespec/(spec.sI)

#plot_oo, lx_es, lx_tubespec, psym=10, $
#	xrange = [0.1,10.], yrange = [1.E8, 1.E14], $
#        title = 'Source spectrum', $
#	xtitle = 'Energy (keV, bin size = '+ $
#		STRING(lx_estep*1000.0,FORMAT="(F6.2)")+' eV)', $
#	ytitle = 'Flux  ( photons / sec bin steradian mA )'

# Use 1.0 mA for the current for the plot becasue it's in units
# of per mA and another current value would confuse.
#save_sI = spec.sI
#spec.sI = 1.0
#notes = [1,1,0,0,0,0,0,0,0,0,0]
#labx_annotate, notes, 0.15, 0.28
#spec.sI = save_sI

#print spec.es
#print spec.tubespec

fig = plt.figure()
ax = fig.gca()
ax.set_xscale('log')
ax.set_yscale('log')
plt.xlabel('Energy (keV)')
plt.ylabel('Number of photons')

plt.plot(spec.es, spec.tubespec)
plt.show()
