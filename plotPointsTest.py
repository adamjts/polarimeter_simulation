import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import axes3d
from astropy.table import Table, Column, vstack
from transforms3d.euler import euler2mat

from marxs.source.labSource import FarLabPointSource, LabPointSource
from marxs.optics.baffle import Baffle
from marxs.optics.multiLayerMirror import MultiLayerMirror
from marxs.optics.grating import FlatGrating
from marxs.optics.detector import FlatDetector
from marxs.optics.polarization import polarization_vectors

from energyDistributions import createEnergyTable

'''This is a collection of functions that can be useful in using the MARXS software to simulate a soft X-ray polarimeter.
'''

def sourceMirrorDetector(mirror='A12113', sourceAngle=0, time=1., sourceOffset=0, detOffset=0, source='C',
		apDims=[0.125, 0.125], V=10., I=0.1):
    '''Sets up and runs the following simulation.
    
    Layout:
    --------------------------------------
    Source                        Detector
      |                              ^
      |                             /|\
     \|/                             |
      v                              |
    Mirror  ->   (Grating)   ->   Mirror
    --------------------------------------
    
    
    Parameters
	----------
	mirror: string
		the serial number of the mirror (in the mirror reflectivity file's name)
	sourceAngle: float
		the angle the source is rotated from the +z axis (counter-clockwise looking from the +x axis)
	time: float
		the amount of time that is being simulated
	sourceOffset: float
		the distance between the center of the first mirror and the photons beam axis
		(in the direction of the +y axis before rotation)
	detOffset: float
		the distance between the center of the second mirror and the photons beam axis
		(in the direction of the +y axis before rotation)
	source: string OR 1D array of length 2
		if string: the chemical symbol/formula for the material of the source (ex: 'C' for carbon, or 'AlO' for aluminum oxide)
		if array: the mean and std. deviation for a normal energy distribution
	apDims: 1D array of length 2 OR None
		NOTE: the type of input to this parameter determines whether FarLabPointSource or LabPointSource is used
		if array: the y and z dimensions of the aperture for a far lab source
		if None: None is the input, this causes the program to use the slightly more realistic, but much slower, lab source
	V: float
		the voltage of the source in kV
	I: float
		the current of the source in mA
    '''
    
    # paths to mirror files
    string1 = './mirror_files/' + mirror + '.txt'
    string2 = './mirror_files/ALSpolarization.txt'
    
    # inputs not accounted for by parameters
    sourceDist = 8149.7
    sourceRadius = 192.
    apertureRadius = 20.
    sourceAngle *=  np.pi/180
    detDist = -9532.5
    detRadius = 50.
    detAngle = 0 * np.pi/180    # from the +z axis, counter-clockwise looking from the +x axis
    
    # calculate rotation matrices
    # looking from the axis of rotation the rotation is counter-clockwise
    r1 = euler2mat(np.pi/4, sourceAngle, 0, 'syxz')
    r2 = euler2mat(-np.pi/4, detAngle, 0, 'syxz')
    r3 = euler2mat(np.pi/2, detAngle, 0, 'syxz')
    r4 = euler2mat(np.pi/2, sourceAngle, 0, 'syxz')
    
    # choose an energy distribution based on the source
    if isinstance(source, basestring):
        energies = createEnergyTable(source, V_kV = V, I_mA = I)   # photons/sec/steradian
        rate = sum(energies[1])   # photons/sec/steradian
    elif hasattr(source, 'shape') and (source.shape == np.array([0,0]).shape):
        energies = normalEnergyFunc(source[0], source[1])
    else:
        print 'source must be a string describing the source material or a 1D array of length 2'

    # choose a model for the source based on whether aperture dimensions were given
    if apDims != None:
        solidAngle = apDims[0] * apDims[1] / (sourceRadius - apertureRadius)**2
        rate *= solidAngle
        source = FarLabPointSource([sourceDist, sourceRadius * np.sin(-sourceAngle), sourceRadius * np.cos(-sourceAngle)],
            position = [sourceDist, apertureRadius * np.sin(-sourceAngle), apertureRadius * np.cos(-sourceAngle)],
            energy = energies, flux = rate, orientation = r4, zoom = [1, apDims[0], apDims[1]])
    else:
        source = LabPointSource([sourceDist, sourceRadius * np.sin(sourceAngle), sourceRadius * np.cos(sourceAngle)],
            direction='-z', energy = energies, flux = 1e9)
    
    # initialize both mirrors and the detector
    mirror1 = MultiLayerMirror(string1, string2,
        position=np.array([sourceDist, sourceOffset * np.cos(sourceAngle), sourceOffset * np.sin(sourceAngle)]), orientation=r1)
    mirror2 = MultiLayerMirror(string1, string2,
        position=np.array([detDist, detOffset * np.cos(detAngle), detOffset * np.cos(detAngle)]), orientation=r2)
    detector = FlatDetector(pixsize=24.576e-3,
        position = np.array([detDist, detRadius * np.sin(-detAngle), detRadius * np.cos(-detAngle)]),
        zoom = np.array([1, 12.288, 12.288]), orientation = r3)
    #preDetector = FlatDetector(pixsize=24.576e-3, position = np.array([detDist + 20, 0, 0]), zoom = np.array([1, 100, 100]))
    #testDetector = FlatDetector(pixsize=24.576e-3, position = np.array([detDist + 1e4, 0, 0]), zoom = np.array([1, 50, 50]))
    '''
    photons = source.generate_photons(time)
    #photons = generateTestPhotons([sourceDist, sourceRadius * np.sin(sourceAngle), sourceRadius * np.cos(sourceAngle)])
    photons = mirror1.process_photons(photons)
    photons = photons[photons['probability'] > 0]
    photons = mirror2.process_photons(photons)
    photons = photons[photons['probability'] > 0]
    photons = detector.process_photons(photons)
    
    return photons
    '''
    # run the simulation
    parts = 8
    for i in range(0, parts):
        photons = source.generate_photons(time / parts)
        photons = mirror1.process_photons(photons)
        photons = photons[photons['probability'] > 0]
        #photons = testDetector.process_photons(photons)
        #photons = preDetector.process_photons(photons)
        #if i == 0:
        #   pre_all_photons = photons.copy()
        #else:
        #   pre_all_photons = vstack([pre_all_photons, photons])
        photons = mirror2.process_photons(photons)
        photons = photons[photons['probability'] > 0]
        photons = detector.process_photons(photons)
        if i == 0:
            all_photons = photons.copy()
        else:
            all_photons = vstack([all_photons, photons])
            #print all_photons
            
    #plotPoints(pre_all_photons, 50, 40, 'path_', angle = sourceAngle, all = False)

    return all_photons
    


def plotPoints(photons, xlim, ylim, filename, angle = 0, all = True):
    p = photons[photons['probability'] > 0].copy()
    #p = photons
    r = np.random.uniform(size=len(p))

    q = p[p['probability'] > r]
    #print 'angle = ' + str(angle) + ': ' + str(len(q)) + ' counts'

    fig = plt.figure()
    fig.clf()
    ax = fig.gca()
    p = p[p['probability'] > 1e-5]
    #print p[p['probability'] > 1e-10]
    if all:
        ax.plot(p['det_x'], p['det_y'], '.', color='blue', label='Probability > 1e-5')
    ax.plot(q['det_x'], q['det_y'], '.', color='red', label='Chosen')
    plt.legend(loc = 'best')
    ax.set_xlim([-xlim, xlim])
    ax.set_ylim([-ylim, ylim])
    ax.set_xlabel('Detector x coordinate (mm)')
    ax.set_ylabel('Detector y coordinate (mm)')
    #ax.set_title('')
    #ax.scatter(edgecolor = 'none')
    #plt.hist2d(x, y, weights, bins)
    #np.digitize
    #plt.imshow()  check origin?
    #fig.savefig(filename + str(angle) + '.png')
    plt.show()



def fullRotation(exp_time, offset = 0, ):
    '''The source and first mirror are rotated around 360 degrees, and the simulation is run at 10 degree intervals.
    '''
    counts = np.zeros(36)
    for i in np.arange(0, 360, 10):
        print 'angle: ' + str(i)
        photons = sourceMirrorDetector(sourceAngle = i, time = float(exp_time), sourceOffset = offset, detOffset = offset)
        p = photons[photons['probability'] > 0].copy()
        #p['probability'] *= 100
        for j in range(0, 20):
            r = np.random.uniform(size=len(p))
            q = p[p['probability'] > r]
            counts[i / 10] += len(q)
        print counts
    
    return counts
        
    #np.save('full_rot_counts_C_source', counts)
