#!/usr/bin/python
# -*- coding: utf-8 -*-

# to avoid matplotlib error in screen shell
import matplotlib
import matplotlib matplotlib.use(’Agg’)
#
import sys

# get environment variable for XCLASS root directory
XCLASSRootDir = str(os.environ.get('XCLASSRootDir', ''))
XCLASSRootDir = XCLASSRootDir.strip()
if (XCLASSRootDir != ""):
    NewModulesPaths = [XCLASSRootDir + "/build_tasks/"]
else:
    # use the following line to define XCLASS root directory manually
    NewModulesPath = "/Volumes/SD-Mac/XCLASS-Interface/build_tasks/"

# extend sys.path variable
already_included_flag = False
for entries in sys.path:
    if (entries == NewModulesPath):
        already_included_flag = True
        break
    if (not already_included_flag):
        sys.path.append(NewModulesPath)

# import MAGIX package
import task_MAGIX

# define parameters for MAGIX
MAGIXExpXML = "Reflectance_Data.xml"
MAGIXInstanceXML = "parameters.xml"
MAGIXFitXML = "algorithm-settings.xml"
MAGIXRegXML = "Generalized_Drude-Lorentz__sym__freq-damping+Rp.xml"
MAGIXOption = ""

# start MAGIX function
task_MAGIX.MAGIX(MAGIXExpXML, MAGIXInstanceXML, MAGIXFitXML, MAGIXRegXML, MAGIXOption)

# update database
import task_UpdateDatabase
DBUpdateNew = 'new'
task_UpdateDatabase.UpdateDatabase(DBUpdateNew)
