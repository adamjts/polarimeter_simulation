Jason Frost
8/11/15

polarimeter_simulation

OVERVIEW: This directory contains the files required to run a MARXS software
simulation of a soft x-ray polarimeter designed with multilayer mirrors. MARXS
must be installed separately. As of August 2015 it is still in development, but
is available on GitHub.

********************************************************************************

labSimulation.py: This is the python script to run the simulation. Run by
entering "python labSimulation.py" into the command line. It contains a number
of potentially useful functions for running the simulation that can be used and
combined in various ways. At the very end of the file, the desired functions for
a given simulation are called with specific parameters. Some examples are
commented. Make sure to choose or write the specific simulation at the end of
the file that you want to run.

energyDistributions.py: This file pulls all of the functions from the
source_modeling folder together and is used by labSimulation.py to model certain
x-ray sources.

source_modeling: This directory contains files used to calculate the emission
spectrum for certain x-ray sources. Some of the files were converted from IDL to
python and are now used indirectly through energyDistributions.py

mirror_files: Each mirror has a unique table listing reflectivity values. See
the multilayer mirror class documentation in MARXS for the required format if
you want to add a new mirror.

sample_data: This directory contains a few saved numpy arrays of photon counts
from simulations that involved a full source rotation, as well as the
corresponding graphs of those arrays. Some simulated images are also included.