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

# iterate through all spws
spws = ['0', '1', '2', '3']
jobdirs = []
for spw in spws:
    data = 'spw'+spw+'.imcontsub.scriptExtraction.forXCLASS.txt'
    NumHeaderLines = 0
    restfreq = 0
    vlsr = 0
    expdata = task_LoadASCIIFile.LoadASCIIFile(data, NumHeaderLines, restfreq, vlsr)

    # call myXCLASS , LoadASCIIFile , and myXCLASSPlot functions

    FreqMin = expdata[:,0].min()
    FreqMax = expdata[:,0].max()

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
    MolfitsFileName = os.path.expanduser('~')+'/programs/xclass/coms.molfit'
    iso_flag = False
    IsoTableFileName = ''
    RestFreq = restfreq
    vLSR = vlsr
    modeldata, log, TransEnergies, IntOpt, jobDir = task_myXCLASS.myXCLASS(FreqMin , FreqMax , FreqStep , TelescopeSize , Inter_Flag ,
                                                                           t_back_flag , tBack , tslope , nH_flag , N_H , beta_dust ,
                                                                           kappa_1300 , MolfitsFileName , iso_flag , IsoTableFileName , RestFreq , vLSR)

    # save the jobdir
    jobdirs.append(jobDir)
    # plot the synthetic spectrum against the observation color-coded by species
    # get the intensities of each species from myXCLASS results
    import glob
    intensity_files = glob.glob(jobDir+'intensity*.dat')
    import matplotlib.pyplot as plt
    from astropy.io import ascii

    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(111)

    ax.plot(expdata[:,0], expdata[:,1], label='observation', color='k')

    # integrated Spectrum
    all_spec = ascii.read(jobDir+'xclass_spectrum_output.dat',
                          header_start=None, data_start=4, names=['Frequency[MHz]', 'Tmb[K]'])
    ax.plot(all_spec['Frequency[MHz]'], all_spec['Tmb[K]'], label='all', color='Gray')

    # individual species
    for species in intensity_files:
        mol_spec = ascii.read(species, header_start=None, data_start=4, names=['Frequnecy[MHz]', 'Tmb[K]'])
        mol_name = species.split('intensity')[1].split('comp')[0][2:-3]
        ax.plot(mol_spec['Frequnecy[MHz]'], mol_spec['Tmb[K]'], label=mol_name)

    ax.legend(loc='best', fontsize=12, ncol=2)
    ax.set_xlabel('Frequency [MHz]', fontsize=18)
    ax.set_ylabel(r'T$_{\rm mb}$ [K]', fontsize=18)
    ax.set_ylim([-20,20])
    ax.minorticks_on()
    [ax.spines[axis].set_linewidth(1.5) for axis in ['top','bottom','left','right']]
    ax.tick_params('both',labelsize=16,width=1.5,which='major',pad=5,length=5)
    ax.tick_params('both',labelsize=16,width=1.5,which='minor',pad=5,length=2.5)
    plt.grid(True)

    SaveFigureFile = jobDir+'xclass_spectrum_output_spw'+spw+'.pdf'
    fig.savefig(SaveFigureFile, format='pdf', dpi=300, bbox_inches='tight')
