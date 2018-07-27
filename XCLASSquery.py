import matplotlib
matplotlib.use('Agg')
#
import sys
import os

# get environment variable for XCLASS root directory
XCLASSRootDir = str(os.environ.get('XCLASSRootDir', ''))
XCLASSRootDir = XCLASSRootDir.strip()
if (XCLASSRootDir != ""):
    NewModulesPath = XCLASSRootDir + "/build_tasks/"
else:
    # use the following line to define XCLASS root directory manually
    NewModulesPath = "/home/bettyjo/yaolun/XCLASS-Interface/build_tasks/"

# extend sys.path variable
if NewModulesPath not in sys.path:
    sys.path.append(NewModulesPath)

# Update XCLASS database

# import task_UpdateDatabase
# DBUpdateNew = 'new'
# task_UpdateDatabase.UpdateDatabase(DBUpdateNew)

def XCLASSquery(freqlow, freqhigh):
    # call GetTransition function
    # import ListDatabase package
    import task_ListDatabase
    from astropy.table import Table
    import numpy as np
    # call ListDatabase function
    FreqMin = freqlow
    FreqMax = freqhigh
    ElowMin = 0.0
    ElowMax = 3000.0
    SelectMolecule = []
    OutputDevice = 'quiet'
    Contents = task_ListDatabase.ListDatabase(FreqMin, FreqMax, ElowMin, ElowMax,
                                              SelectMolecule, OutputDevice)
    # parse the Contents array
    output = Table(np.array([c.split() for c in Contents]),
      names=('name', 'upper_state', 'lower_state', 'freq[MHz]', 'error_freq[MHz]', 'Einstein_A', 'lower_energy[K]', 'upper_state_degeneracy'),
      dtype=('U34','U34', 'U34', 'f8', 'f8', 'f8', 'f8', 'f8'))

    return output

# a = XCLASSquery(354554, 354556)
# a.show_in_notebook()
