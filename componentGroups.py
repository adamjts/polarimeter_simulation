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
		'''Default Setup:
		Z is out of the screen. X+ is to the right. Y+ is upwards.

		   Source
		   	|
		   	|
		   	|
		   	MLMirror------>
		'''
        # parameters for coneSource -- THESE WILL ALL BE WOBBLED LATER
		self.sourcePos = [0, sourceDistance , 0]
		self.sourceDirection = [0,-1,0]
		self.delta = openningAngle/2 

		#mirrorData
		self.reflFile = reflFile
		self.testedPolarization = testedPolarization
		self.defaultOrientation = euler2mat(-np.pi/4, 0, 0, 'syxz')
		self.defaultOrientation = np.dot(euler2mat(0,-np.pi/2,0,'syxz'),self.defaultOrientation)
		# Generate Mirror
		self.mirror = MultiLayerMirror(self.reflFile, self.testedPolarization,
        position=np.array([0, 0, 0]), orientation=self.defaultOrientation) #should rotate about y



	def __str__(self):
		report = "CURRENT SETUP\n"

		report += "Mirror:\n" 

		report += "    -center: " + str(self.mirror.geometry['center']) + "\n"
		report += "    -norm: "+ str(self.mirror.geometry['plane']) + "\n"
		
		report += " \n \n"
		report += "Source:\n"
		report += "    -position: " + str(self.sourcePos)+ "\n"
		report += "    -direction: " + str(self.sourceDirection)+ "\n"
		report += "    -solid angle: " + str(self.delta) + " steradians"+ "\n"

		report += "\n \n RAW: \n"
		report += str(self.mirror.geometry)

		return report
			

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

	def offset_mirror_orientation(self, rotationMatrix):
		# This is used to rotate the mirror relative to its default orientation
		rotationMatrix = np.array(rotationMatrix)
		self.mirror = MultiLayerMirror(self.reflFile, self.testedPolarization,
			position=np.array([0, 0, 0]), orientation=np.dot(rotationMatrix,self.defaultOrientation))

	def offset_mirror_position(self, position):
		# This is used to place the mirror relative to its default position
		position = np.array(position)
		self.mirror = MultiLayerMirror(self.reflFile, self.testedPolarization,
			position=position, orientation=self.defaultOrientation)

	def move_mirror_orientation(self,rotationMatrix):
		# This is used to rotate the mirror relative to its current orientation
		#NOT DONE. 
		rotationMatrix = np.array(rotationMatrix)

		#Find matrix necessary to get it to its current position. Then dot these.
		#in other words... firs find the matrix which maps [1,0,0] to mirror.geometry['plane']

	def move_mirror_position(self, displacement):
		# This is used to move the mirror relative to its current position
		displacement = displacement + [0]
		self.mirror.geometry['center'] += np.array(displacement)








