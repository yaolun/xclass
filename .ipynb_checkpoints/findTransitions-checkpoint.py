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



# GUI for get transition
import task_LoadASCIIFile

# load the ascii data
data = 'spw0.imcontsub.scriptExtraction.forXCLASS.txt'
NumHeaderLines = 0
restfreq = 0
vlsr = 0
expdata = task_LoadASCIIFile.LoadASCIIFile(data, NumHeaderLines, restfreq, vlsr)

# call GetTransition function
import task_GetTransitions
selectMolecule = []
freqWidth = 5.0
ElowMin = 0.0
ElowMax = 1000.0
freqMin = expdata[:,0].min()
freqMax = expdata[:,0].max()
task_GetTransitions.GetTransitions(expdata, freqMin, freqMax, selectMolecule, freqWidth, ElowMin, ElowMax, expdata)