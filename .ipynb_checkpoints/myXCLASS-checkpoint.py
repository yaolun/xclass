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

# import task_myXCLASS , task_LoadASCIIFile , and task_myXCLASSPlot packages import task_myXCLASS
import task_LoadASCIIFile
import task_myXCLASSPlot
import task_myXCLASS

# load spw0 spectrum
data = 'spw0.imcontsub.scriptExtraction.forXCLASS.txt'
NumHeaderLines = 0
restfreq = 0
vlsr = 0
expdata = task_LoadASCIIFile.LoadASCIIFile(data, NumHeaderLines, restfreq, vlsr)

# call myXCLASS , LoadASCIIFile , and myXCLASSPlot functions 

FreqMin = expdata[:,0].min()
FreqMax = expdata[:,0].max()
print(FreqMin, FreqMax)

FreqStep = 0.5  # MHz
TelescopeSize = 0.27
Inter_Flag = True
t_back_flag = False
# default values
tBack = 0.0
tslope = 0.0
nH_flag = False
N_H = 1e24
beta_dust = 0.1
kappa_1300 = 0.01
MolfitsFileName = '/Users/yaolun/programs/xclass/coms.molfit'
iso_flag = False
IsoTableFileName = ''
RestFreq = restfreq
vLSR = vlsr
modeldata, log, TransEnergies, IntOpt, jobDir = task_myXCLASS.myXCLASS(FreqMin , FreqMax , FreqStep , TelescopeSize , Inter_Flag ,
                                                                       t_back_flag , tBack , tslope , nH_flag , N_H , beta_dust , 
                                                                       kappa_1300 , MolfitsFileName , iso_flag , IsoTableFileName , RestFreq , vLSR)

# plot

MinIntensity = 0.0
xLowerLimit = None
xUpperLimit = None
yLowerLimit = None
yUpperLimit = None

PlotTitle = "BHR 71 HCN J=4-3 (spw0)"
LegendFlag = True
SaveFigureFile = jobDir+'xclass_spectrum_output_spw0.pdf'
task_myXCLASSPlot.myXCLASSPlot(expdata, modeldata, TransEnergies, RestFreq, vLSR,
                               MinIntensity, xLowerLimit, xUpperLimit, yLowerLimit, yUpperLimit,
                               PlotTitle, LegendFlag, SaveFigureFile)

