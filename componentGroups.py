import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import axes3d
from astropy.table import Table, Column, vstack
from transforms3d.euler import euler2mat

from marxs.source.labSource import FarLabPointSource, LabPointSource, LabPointSourceCone
from marxs.optics.baffle import Baffle
from marxs.optics.multiLayerMirror import MultiLayerMirror
from marxs.optics.grating import FlatGrating
from marxs.optics.detector import FlatDetector
from marxs.optics.polarization import polarization_vectors

from energyDistributions import createEnergyTable




class SourceMLMirror():
	#this will also alllow the elements to wiggle later. RN it goes light source --> MLMirror
	# The mirror is at the center of this object
	def __init__(self, reflFile, testedPolarization, openningAngle, sourceDistance = 500, **kwargs):

        # parameters for coneSource -- THESE WILL ALL BE WOBBLED LATER
		self.sourcePos = [0,sourceDistance, 0]
		self.sourceDirection = [0,-1,0]
		self.delta = openningAngle/2 

		#mirrorData
		self.reflFile = reflFile
		self.testedPolarization = testedPolarization
		# Generate Mirror
		self.mirror = MultiLayerMirror(self.reflFile, self.testedPolarization,
        position=np.array([0, 0, 0]), orientation=euler2mat(0, 0, np.pi/4, 'syxz'))



	def __str__(self):
		return "Geometry: " + str(self.geometry) + "\nDistance between components: " + str(self.sourcePos[2]) + "mm"

	def generate_photons(self, exposureTime, flux=100, V=10, I=0.1):
		# Generate Initial Photons

		energies = createEnergyTable('C', V_kV = V, I_mA = I) 

		source = LabPointSourceCone(self.sourcePos, delta = self.delta, energy= energies, direction = self.sourceDirection, flux = flux) # Generate photons from original source
		photons = source.generate_photons(exposureTime)


		reflectedPhotons = self.mirror.process_photons(photons)



		# Removing photons with zero probability
		rowsToRemove = []
		for i in range(0,len(photons)):
			if (photons[i]['probability']==0):
				rowsToRemove.append(i)

		rowsToRemove = np.array(rowsToRemove)
		photons.remove_rows(rowsToRemove)


		return reflectedPhotons

	#def rotate_mirror(rotationMatrix):
		#self.mirror = MultiLayerMirror(self.reflFile, self.testedPolarization, #position=np.array([0, 0, 0]), orientation=np.dot( rotationMatrix, euler2mat(0, 0, np.pi/4, 'syxz'))