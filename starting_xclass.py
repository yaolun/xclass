
# coding: utf-8

# In[1]:

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


# #### Update XCLASS database

# In[5]:

import task_UpdateDatabase
DBUpdateNew = 'new'
task_UpdateDatabase.UpdateDatabase(DBUpdateNew)


# In[6]:

from datetime import datetime
print('Last time for databse update: ', str(datetime.now()))


# #### GUI for get transition

# In[13]:

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
ElowMax = 3000.0
freqMin = expdata[0].min()
freqMax = expdata[0].max()
task_GetTransitions.GetTransitions(expdata, freqMin, freqMax, selectMolecule, freqWidth, ElowMin, ElowMax, [[0],[0]])


# In[ ]:



