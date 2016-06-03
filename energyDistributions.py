import numpy as np
import matplotlib.pyplot as plt

from source_modeling.source_spectrum import SourceSpectrum
from source_modeling.labx_tubespec import labx_tubespec


def createEnergyTable(sourceType, V_kV = 10., I_mA = 0.1):
	spec = SourceSpectrum(sourceType, V_kV, I_mA)

	# Calculate the spectrum - puts it in spec.tubespec,
	#  units of phots/ (sec bin steradian)
	labx_tubespec(spec)

	# units of phots/ (sec bin steradian mA)
	spec.tubespec = spec.tubespec/(spec.sI)
	table = np.zeros((2, len(spec.es)))
	table[0] = spec.es
	table[1] = spec.tubespec
	return table
