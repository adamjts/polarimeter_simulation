import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import axes3d
from astropy.table import Table, Column, vstack
from transforms3d.euler import euler2mat
from transforms3d.affines import compose

import os

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
			# Remove Photons that Miss
			if (reflectedPhotons[i]['probability']==0):
					rowsToRemove.append(i)

			# Remove negligible Photons
			if (reflectedPhotons[i]['probability']<=(5e-10)):
				rowsToRemove.append(i)

		rowsToRemove = np.array(rowsToRemove)

		if (len(rowsToRemove)>0):
			reflectedPhotons.remove_rows(rowsToRemove)

		# Transform the reflected photons from the local cooridinate system to the global coordinate system

		reflectedPhotons['dir'] = np.dot(self.pos4d, reflectedPhotons['dir'].T).T

		reflectedPhotons['pos'] = np.dot(self.pos4d, reflectedPhotons['pos'].T).T

		reflectedPhotons['polarization'] = np.dot(self.pos4d, reflectedPhotons['polarization'].T).T

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




class MLMirrorDetector(OpticalElement):

	def defaultMirror(self,reflFile, testedPolarization):
		#mirrorData Defaults - reference files
		self.reflFile = reflFile
		self.testedPolarization = testedPolarization

		#mirror Defauls
		self.defaultMirrorOrientation = euler2mat(-np.pi/4, 0, 0, 'syxz')
		self.defaultMirrorOrientation = np.dot(euler2mat(0,-np.pi/2,0,'syxz'),self.defaultMirrorOrientation)
		self.defaultMirrorOrientation = np.dot(euler2mat(np.pi,0,0,'syxz'),self.defaultMirrorOrientation)

		self.defaultMirrorPosition = np.array([0,0,0])

		self.defaultMirrorPos4d = compose(self.defaultMirrorPosition, self.defaultMirrorOrientation, np.array([1, 24.5, 12]), np.zeros(3))

		mirror = MultiLayerMirror(self.reflFile, self.testedPolarization,
        pos4d = self.defaultMirrorPos4d); return mirror


	def defaultDetector(self, detectorDistance):
		self.defaultDetectorOrientation = euler2mat(0, 0 , -np.pi/2, 'syxz')
		self.defaultDetectorPosition = np.array([0, detectorDistance, 0])
		self.defaultDetectorPos4d = compose(self.defaultDetectorPosition, self.defaultDetectorOrientation, [1, 12.288, 12.288], np.zeros(3))
		detector = FlatDetector(pixsize=24.576e-3, pos4d = self.defaultDetectorPos4d)

		return detector




	def __init__(self, reflFile, testedPolarization, detectorDistance = 50, **kwargs):
		super(MLMirrorDetector, self).__init__(**kwargs)
		self.defaultApparatusPos4d = self.pos4d

		# Generate Default Mirror
		self.mirror = self.defaultMirror(reflFile, testedPolarization)
		# Generate Default Detector
		self.detector = self.defaultDetector(detectorDistance)
		'''Default Setup:
		Z+ is out of the screen. X+ is to the right. Y+ is upwards.

		  			 detector
		   			   /|\
		  			 	|
					   	|
		 	>-->-->--MLMirror

		   	self.pos4d is a record of all the transformations on the ENTIRE setup as a whole
		'''

	def __str__(self):
		report = "APPARATUS GEOMETRY ****************** (Global Coordinates) \n"
		report += "    -transformation record: \n" + str(self.pos4d)


		report += "\n \n"
		report += "CURRENT SETUP ****************** (Local Coordinates)\n"

		report += "Mirror:\n" 
		report += "    -center: " + str(self.mirror.geometry['center']) + "\n"
		report += "    -norm: "+ str(self.mirror.geometry['plane']) + "\n"
		

		report += " \n \n"
		report += "Detector: \n"
		report += "    -center: " + str(self.detector.geometry['center']) + "\n"
		report += "    -norm: "+ str(self.detector.geometry['plane']) + "\n"

		report += "\n \n"
		report += "RAW_mirror: \n"
		report += str(self.mirror.geometry)

		report += "\n \n"
		report += "RAW_detector: \n"
		report += str(self.detector.geometry)

		return report

	def updateDetector(self, detectorPos4d):
		self.detector = FlatDetector(pixsize=24.576e-3, pos4d = detectorPos4d)




	def detect_photons(self, photons):
		reflectedPhotons = self.mirror.process_photons(photons)


		#remove the zero probabilities
		rowsToRemove = []

		for i in range(0,len(reflectedPhotons)):
			if (reflectedPhotons[i]['probability']==0):
				rowsToRemove.append(i)

		rowsToRemove = np.array(rowsToRemove)

		if (len(rowsToRemove) > 0):
			reflectedPhotons.remove_rows(rowsToRemove)

		detectedPhotons = self.detector.process_photons(reflectedPhotons)

		return detectedPhotons

#	def move_detector(self, moveMatrix):





#********************    SIMULATIONS    ***********************************************************************************************************


class staticSimulation():

	def __init__(self, firstMirrorREFL = './mirror_files/A12113.txt', firstMirrorPOL = './mirror_files/ALSPolarization.txt', secondMirrorREFL= './mirror_files/A12113.txt', secondMirrorPOL = './mirror_files/ALSPolarization.txt'):

		self.first = SourceMLMirror(firstMirrorREFL, firstMirrorPOL)
		self.second = MLMirrorDetector(secondMirrorREFL, secondMirrorPOL)


		self.distanceBetweenHalves = 50
		self.angleOffset = 0

		Rotation = euler2mat(0,0,0,'syxz')
		FirstHalfPlacement = compose([-self.distanceBetweenHalves,0,0], Rotation, [1,1,1], [0,0,0]) #This will move the first half away from the second by 50 mm

		self.first.offset_apparatus(FirstHalfPlacement)

	def __str__(self):
		report = 'Static Setup: \n'
		report += '    -Distance Between Halves: ' + str(self.distanceBetweenHalves) + "\n"
		report += '    -Angle Offset: ' + str(self.angleOffset) + "\n \n"
		report += 'Individual Component Details under self.first and self.second. (ex: print (SimulationName).first). Each subcomponent accessible through self.first.source / self.second.mirror' 

		return report

	def configure_mirrors(self,firstMirrorREFL = './mirror_files/A12113.txt', firstMirrorPOL = './mirror_files/ALSPolarization.txt', secondMirrorREFL= './mirror_files/A12113.txt', secondMirrorPOL = './mirror_files/ALSPolarization.txt'):
		self.first = SourceMLMirror(firstMirrorREFL, firstMirrorPOL)
		self.second = MLMirrorDetector(secondMirrorREFL, secondMirrorPOL)

	def offset_angle(self, angle):
		self.angleOffset = angle

		Rotation = euler2mat(0,angle,0,"syxz")

		matrix = compose([0,0,0],Rotation,[1,1,1],[0,0,0])

		self.first.offset_apparatus(matrix)



	def run(self, exposureTime = 1000):
		# Generating photons that travel down the beamline
		print "Generating Cross Photons..."
		cross = self.first.generate_photons(exposureTime)

		# Receive Photons on other side
		print "Receiving Photons..."
		self.results = self.second.detect_photons(cross)

		return self.results

class rotation():
	def __init__(self):
		#self.numberOfAngles = 3 #NUMBER OF ANLGES THAT WILL BE TESTED
		#self.exposureTime = 1000

		# Make a folder to hold the trials

		if not os.path.exists('./RotatingSimulationTrials'):
			os.mkdir('./RotatingSimulationTrials')

		
		# Determine current trial number

		self.trialNumber = 0

		while os.path.isdir('./RotatingSimulationTrials/Trial' + str(self.trialNumber)):
			self.trialNumber = self.trialNumber + 1

		

	def __str__(self):
		return "rotation.run( [static_simulation], [number_of_angles = 3], [exposure_time = 1000])"


	def theTrialNumber(self):

		self.trialNumber = 0
		while os.path.isdir('./RotatingSimulationTrials/Trial' + str(self.trialNumber)):
			self.trialNumber = self.trialNumber + 1

		return self.trialNumber

	def makeTrialFolder(self, trialNumber = None):

		if trialNumber == None:
			trialNumber = self.trialNumber

		os.mkdir('./RotatingSimulationTrials/Trial' + str(trialNumber))


	def run(self, staticSimulation, numAngles = 3, exposureTime = 1000):
		# Will also return angle and total probability as 2D array

		# Make a Folder to Hold This Trial
		self.makeTrialFolder(self.theTrialNumber())


		# These two lines are purely for the returned statistic
		probabilities = np.array([])
		angles = np.array([])

		# Create an instance of the simulation
		sim = staticSimulation #There should be one passed in so all its configurations already get handled

		for i in range(0, numAngles):
			angle = i * (2*np.pi/numAngles)
			print "\nRunning Angle: " + str(angle) + "..."

			sim.offset_angle(angle)

			results = sim.run(exposureTime)

			results.write('./RotatingSimulationTrials/Trial' + str(self.trialNumber) + '/Angle' + str(i+1)+ 'of' + str(numAngles) + '.fits')

			# For returning angle-probability relationship
			angles = np.append(angles, [angle])

			probability = np.sum(results['probability'])
			probabilities =np.append(probabilities, [probability])



		# Set static simulation back to angle zero:
		sim.offset_angle(0)

		return [angles, probabilities]









'''

class dataSheet():
	def __init__(self, pathway, name):

		self.pathway = pathway

		self.NFiles = len([f for f in os.listdir(pathway)
                if os.path.isfile(os.path.join(name, f))])

		self.filename = pathway + name + '.fits'

		if not os.path.exists(self.filename):

			self.dataTable = Table

			self.dataTable['Angle'] = []

			for i in range(0,len(self.NFiles)):
				inc = 2*np.pi / self.NFiles
				angle = i * inc

				self.dataTable['Angle'][i] = angle


			self.dataTable.write(self.filename)
		else:
			self.dataTable = Table.read(self.filename)



	def add_total_probabilities(self, *args):

		filenames = args

		self.dataTable = Table.read(self.filename)

		self.dataTable['Total Probability'] = []

		probabilities = []

		for i in range(0, len(args)):
			photonTable = Table.read( self.pathway + "/" +filenames[i])
			probability = np.sum(photonTable['probability'])

			self.dataTable['Total Probability'] = np.append(self.dataTable['Total Probability'], [probability])

		self.dataTable.write(self.filename)





'''








#*********************    PLOTTING     ****************************

class DataDetails():
	#This is for a single angle
	def __init__(self, data):
		self.data = data.copy()

	def filterProbabilities(self):
		# Removes from self.data photons w/ probability < median probability
		medianProbability = np.median(self.data['probability'])

		rowsToRemove = []
		for i in range(0,len(self.data)):
			if (self.data[i]['probability'] <= medianProbability):
				rowsToRemove.append(i)

		rowsToRemove = np.array(rowsToRemove)
		self.data.remove_rows(rowsToRemove)

	def outliers(self, quality = 'probability', highLow = 'high'):
		# Returns Table of outliers
		outliers = self.data.copy()

		Q3 = np.percentile(self.outliers[quality], 75 )
		Q1 = np.percentile(self.outliers[quality], 25)
		IQR = Q3 - Q1

		rowsToRemove = []

		if (highLow == 'high'):
			boundary = Q3 + (1.5 * IQR)
			for i in range(0,len(outliers)):
				if (self.outliers[i][quality] <= boundary):
					rowsToRemove.append(i)
		elif (highLow == 'low'):
			boundary = Q1 - (1.5*IQR)
			for i in range(0,len(outliers)):
				if (self.outliers[i][quality] >= boundary):
					rowsToRemove.append(i)
		else:
			print 'ERROR'

		rowsToRemove = np.array(rowsToRemove)

		outliers.remove_rows(rowsToRemove)

		return outliers
'''
	def groupPhotonsAngle(self, quality = 'polangle', increment = 0.1):
		# This returns the sum of the probabilities of phots within the same increment
		number_of_increments = (2*np.pi) / increment

		groupData = self.data.copy()

		probabilities=np.array([])

		angleIncrements = np.arange((increment/2), 2*np.pi, increment)

		for inc in range(0, int(number_of_increments + 1)):
			lowerPercentile = (100/number_of_increments) * inc
			upperPercentile = (100/number_of_increments) * (inc+1)

			lowerBound = np.percentile((2*np.pi), lowerPercentile)
			upperBound = np.percentile((2*np.pi), upperPercentile)

			probabilityPerIncrement = 0

			for i in range(0, len(groupData)):
				angle = groupData['polangle'][i]
				if ((angle >= lowerBound) and (angle < upperBound)):
					probabilityPerIncrement += groupData['probability'][i]


			probabilities = np.append(probabilities, [probabilityPerIncrement])


		return np.array([angleIncrements, probabilities])'''












'''

class plotter():
	def __init__(self):
		plt.clf()

	def probability_polarization(self, dataTable):


		
	def outliers(self, quality = 'probability'):
		# Returns table of photons whose 'quality' is an outlier. Quality could be probability, polarization, etc.

	def hist(self, resolution):
		# Histogram with resultion corresponding to bin size.



'''











