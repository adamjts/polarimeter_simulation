import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import axes3d
from astropy.table import Table, Column, vstack
from transforms3d.euler import euler2mat
from transforms3d.affines import compose

from marxs.source.labSource import FarLabPointSource, LabPointSource, LabPointSourceCone
from marxs.optics.baffle import Baffle
from marxs.optics.multiLayerMirror import MultiLayerMirror
from marxs.optics.grating import FlatGrating
from marxs.optics.detector import FlatDetector
from marxs.optics import OpticalElement
from marxs.optics.polarization import polarization_vectors

from energyDistributions import createEnergyTable




class SourceMLMirror(OpticalElement):
	#this will also alllow the elements to wiggle later. RN it goes light source --> MLMirror
	# The mirror is at the center of this object

	def defaultSource(self, openningAngle, sourceDistance):

		self.defaultSourcePosition = [0, sourceDistance,0]
		self.defaultSourceDirection = [0,-1,0]

		# Generate Source
		flux=100
		V=10
		I=0.1
		energies = createEnergyTable('C', V_kV = V, I_mA = I) 
		source = LabPointSourceCone(self.defaultSourcePosition, delta = openningAngle , energy= energies, direction = self.defaultSourceDirection, flux = flux) # Generate photons from original source
		return source

	def defaultMirror(self,reflFile, testedPolarization):
		#mirrorData Defaults - reference files
		self.reflFile = reflFile
		self.testedPolarization = testedPolarization

		#mirror Defauls
		self.defaultMirrorOrientation = euler2mat(-np.pi/4, 0, 0, 'syxz')
		self.defaultMirrorOrientation = np.dot(euler2mat(0,-np.pi/2,0,'syxz'),self.defaultMirrorOrientation)

		self.defaultMirrorPosition = np.array([0,0,0])

		self.defaultMirrorPos4d = compose(self.defaultMirrorPosition, self.defaultMirrorOrientation, np.array([1, 24.5, 12]), np.zeros(3))

		mirror = MultiLayerMirror(self.reflFile, self.testedPolarization,
        pos4d = self.defaultMirrorPos4d); return mirror


	def __init__(self, reflFile, testedPolarization, openningAngle = 0.05, sourceDistance = 500, **kwargs):
		super(SourceMLMirror, self).__init__(**kwargs)
		self.defaultApparatusPos4d = self.pos4d

		# Generate Default Mirror
		self.mirror = self.defaultMirror(reflFile, testedPolarization)
		self.source = self.defaultSource(openningAngle, sourceDistance)
		'''Default Setup:
		Z+ is out of the screen. X+ is to the right. Y+ is upwards.

		   Source
		   	|
		   	|
		   	|
		   	MLMirror------>

		   	self.pos4d is a record of all the transformations on the ENTIRE setup as a whole.
		   	The source comes in by default from the local y direction.
		   	The photons exit by default in the local x direction
		'''
	
	def updateSource(self, position=None, openningAngle = None, direction = None):
		if position is None:
			position = self.source.position
		if openningAngle is None:
			openningAngle = self.source.deltaphi
		if direction is None:
			direction = self.source.dir
		flux = 100
		V = 10
		I = 0.1
		energies = createEnergyTable('C', V_kV = V, I_mA = I) 
		self.source = LabPointSourceCone(position, delta = openningAngle, energy = energies, direction = direction, flux = flux)


	def updateMirror(self, positionMatrix):
		# Generate Mirror
		self.mirror = MultiLayerMirror(self.reflFile, self.testedPolarization, pos4d = positionMatrix)


	def __str__(self):

		report = "APPARATUS GEOMETRY ****************** (Global Coordinates) \n"
		report += "    -transformation record: \n" + str(self.pos4d)


		report += "\n \n"
		report += "CURRENT SETUP ****************** (Local Coordinates)\n"

		report += "Mirror:\n" 

		report += "    -center: " + str(self.mirror.geometry['center']) + "\n"
		report += "    -norm: "+ str(self.mirror.geometry['plane']) + "\n"
		
		report += " \n \n"
		report += "Source:\n"
		report += "    -position: " + str(self.source.position) + "\n"
		report += "    -direction: " + str(self.source.dir) + "\n"
		report += "    -solid angle: " + str(self.source.deltaphi) + "\n"

		report += "\n \n RAW_mirror: \n"
		report += str(self.mirror.geometry)

		return report
			

	def generate_photons(self, exposureTime):
		# Generate Initial Photons
		photons = self.source.generate_photons(exposureTime)
		reflectedPhotons = self.mirror.process_photons(photons)# Removing photons with zero probability 
		rowsToRemove = []

		for i in range(0,len(reflectedPhotons)):
			if (reflectedPhotons[i]['probability']==0):
				rowsToRemove.append(i)

		rowsToRemove = np.array(rowsToRemove)
		reflectedPhotons.remove_rows(rowsToRemove)

		# Transform the reflected photons from the local cooridinate system to the global coordinate system

		reflectedPhotons['dir'] = np.dot(self.pos4d, reflectedPhotons['dir'].T).T

		reflectedPhotons['pos'] = np.dot(self.pos4d, reflectedPhotons['pos'].T).T

		return reflectedPhotons



	def offset_mirror(self, offsetMatrix):
		# This is how we offset the mirror relative to its default position

		positionMatrix = np.dot(offsetMatrix, self.defaultMirrorPos4d)

		self.updateMirror(positionMatrix)

		# RESET SOURCE TO DO

	def move_mirror(self, moveMatrix):
		#This is how we move the mirror relative to its current position

		positionMatrix = np.dot(moveMatrix, self.mirror.pos4d)

		self.updateMirror(positionMatrix)

	def offset_source(self, offsetVector):
		# This is how we offset the source from its default position
		position = self.defaultSourcePosition + np.array(offsetVector)

		self.updateSource(position = position)

	def move_source(self,offsetVector):
		# This is how we move the mirror relative to its current position

		position = self.source.position + np.array(offsetVector)

		self.updateSource(position = position)

	def offset_apparatus(self,offsetMatrix):
		self.pos4d = np.dot(offsetMatrix, self.defaultApparatusPos4d)











