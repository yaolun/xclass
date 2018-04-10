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

# # import MAGIX package
# import task_MAGIX

# # define parameters for MAGIX
# # TODO: need to fix the paths, after I figure out what are they.
# MAGIXExpXML = "Reflectance_Data.xml"
# MAGIXInstanceXML = "parameters.xml"
# MAGIXFitXML = "algorithm-settings.xml"
# MAGIXRegXML = "Generalized_Drude-Lorentz__sym__freq-damping+Rp.xml"
# MAGIXOption = ""

# # start MAGIX function
# task_MAGIX.MAGIX(MAGIXExpXML, MAGIXInstanceXML, MAGIXFitXML, MAGIXRegXML, MAGIXOption)


# Update XCLASS database

# import task_UpdateDatabase
# DBUpdateNew = 'new'
# task_UpdateDatabase.UpdateDatabase(DBUpdateNew)

# GUI for get transition
# import task_LoadASCIIFile

# load the ascii data
# data = 'spw0.imcontsub.scriptExtraction.forXCLASS.txt'
# NumHeaderLines = 0
# restfreq = 0
# vlsr = 0
# expdata = task_LoadASCIIFile.LoadASCIIFile(data, NumHeaderLines, restfreq, vlsr)

# call GetTransition function
# import task_GetTransitions
# selectMolecule = []
# freqWidth = 5.0
# ElowMin = 0.0
# ElowMax = 3000.0
# freqMin = expdata[:,0].min()
# freqMax = expdata[:,0].max()
# task_GetTransitions.GetTransitions(expdata, freqMin, freqMax, selectMolecule, freqWidth, ElowMin, ElowMax, expdata)


# tutorial for myXCLASS
import task_myXCLASS
import task_LoadASCIIFile
import task_myXCLASSPlot

# call myXCLASS , LoadASCIIFile , and myXCLASSPlot functions
FreqMin = 580102.0
FreqMax = 580546.5
FreqStep = 5.0000000000E-01
TelescopeSize = 3.5
Inter_Flag = False
t_back_flag = True
tBack = 1.1
tslope = 0.0000000000E+00
nH_flag = True
N_H = 3.0000000000E+24
beta_dust = 2.0
kappa_1300 = 0.02
MolfitsFileName = "/Volumes/SD-Mac/XCLASS-Interface/demo/myXCLASS/CH3OH__pure.molfit"
iso_flag = True
IsoTableFileName = "/Volumes/SD-Mac/XCLASS-Interface/demo/myXCLASS/iso_names.txt"
RestFreq = 0.0
vLSR = 0.0
modeldata, log, TransEnergies, IntOpt, jobDir = task_myXCLASS.myXCLASS(FreqMin , FreqMax , FreqStep , TelescopeSize , Inter_Flag , t_back_flag , tBack ,
                                                                       tslope , nH_flag , N_H , beta_dust , kappa_1300 , MolfitsFileName ,
                                                                       iso_flag , IsoTableFileName , RestFreq , vLSR)

# plot
# load expdata
FileName = "/Volumes/SD-Mac/XCLASS-Interface/demo/myXCLASS/band1b.dat"
NumHeaderLines = 1
expdata = task_LoadASCIIFile.LoadASCIIFile(FileName, NumHeaderLines, 0.0, 0.0)

MinIntensity = 0.0
xLowerLimit = expdata[:,0].min()
xUpperLimit = expdata[:,0].max()
yLowerLimit = expdata[:,1].min()
yUpperLimit = expdata[:,1].max()
PlotTitle = "Example for myXCLASSPlot function"
LegendFlag = True
SaveFigureFile = jobDir+'xclass_spectrum_output.pdf'
task_myXCLASSPlot.myXCLASSPlot(expdata, modeldata, TransEnergies, RestFreq, vLSR,
                               MinIntensity, xLowerLimit, xUpperLimit, yLowerLimit, yUpperLimit,
                               PlotTitle, LegendFlag, SaveFigureFile)