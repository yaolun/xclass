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


# import task_myXCLASS , task_LoadASCIIFile , and task_myXCLASSPlot packages
import task_LoadASCIIFile
import task_myXCLASSPlot
import task_myXCLASS

# load spw0 spectrum
data = 'spw0.imcontsub.scriptExtraction.forXCLASS.txt'
# NumHeaderLines = 0
# restfreq = 0
# vlsr = 0
# expdata = task_LoadASCIIFile.LoadASCIIFile(data, NumHeaderLines, restfreq, vlsr)


# import task_myXCLASSFit package
import task_myXCLASSFit
# call myXCLASSFit function
MolfitsFileName = os.path.expanduser('~')+'/programs/xclass/coms.molfit'
experimentalData = data
AlgorithmXMLFile = os.path.expanduser('~')+'/programs/xclass/algorithm-settings.xml'
NumberIteration = 50
TelescopeSize = 0.27
Inter_Flag = True
t_back_flag = False
tBack = 0.0
tslope = 0.0
nH_flag = False
N_H = 1e24
beta_dust = 0.1
kappa_1300 = 0.01
iso_flag = False
IsoTableFileName = ''
RestFreq = 0.0
vLSR = 0.0
newmolfit, modeldata, JobDir = task_myXCLASSFit.myXCLASSFit(NumberIteration, AlgorithmXMLFile, MolfitsFileName,
                                                            experimentalData,  TelescopeSize, Inter_Flag, t_back_flag,
                                                            tBack, tslope, nH_flag, N_H, beta_dust, kappa_1300, iso_flag,
                                                            IsoTableFileName, RestFreq, vLSR)
