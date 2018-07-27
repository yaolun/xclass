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
    if 'bettyjo' in os.path.expanduser('~'):
        NewModulesPath = "/home/bettyjo/yaolun/XCLASS-Interface/build_tasks/"
    else:
        NewModulesPath = '/Volumes/SD-Mac/XCLASS-Interface/build_tasks/'

# extend sys.path variable
if NewModulesPath not in sys.path:
    sys.path.append(NewModulesPath)

# function to create molfit for each spw from a grand list of molecules
def molfitGen(molfit, FreqMin, FreqMax, spw):
    import task_ListDatabase
    ElowMin = 0.0
    ElowMax = 3000.0
    OutputDevice = 'quiet'

    molfit_data = open(molfit, 'r').readlines()
    molfit_out = open(os.path.dirname(molfit)+'/coms_spw'+spw+'.molfit', 'w')
    mol_list = []
    for i, line in enumerate(molfit_data):
        if line.startswith('%'):
            continue
        if len(line.strip().split()) == 2:
            mol_list.append(' '.join(line.strip().split()[0].split(';')[:-1]))
            SelectMolecule = [line.strip().split()[0]]

            Contents = task_ListDatabase.ListDatabase(FreqMin, FreqMax, ElowMin, ElowMax,
                                                      SelectMolecule, OutputDevice)
            if len(Contents) > 0:
                molfit_out.write(molfit_data[i]+molfit_data[i+1])

    molfit_out.close()

    return mol_list, os.path.dirname(molfit)+'/coms_spw'+spw+'.molfit'


import task_LoadASCIIFile
import task_myXCLASS
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.lines as mlines
from astropy.io import ascii
import glob
import numpy as np
from mol_format import mol_format

# fixed parameters for myXCLASS
MolfitsFileName = os.path.expanduser('~')+'/programs/xclass/coms.molfit'
# the directory contains the observed spectra
if 'bettyjo' in os.path.expanduser('~'):
    datadir = '/home/bettyjo/yaolun/alma_workign_data/'
else:
    datadir = '/Users/yaolun/GoogleDrive/research/bhr71_infall/analysis/imcontsub/spectra_mean/'

# parameters of myXCLASS
FreqStep = 0.5  # MHz
TelescopeSize = 0.27  # beam size
Inter_Flag = True
t_back_flag = False

# default values
tBack = 0.0
tslope = 0.0
nH_flag = False
N_H = 1e24
beta_dust = 0.1
kappa_1300 = 0.01
iso_flag = False
IsoTableFileName = ''
RestFreq = 0
vLSR = 0

# iterate through all spws
spws = ['0', '1', '2', '3']
path_info = {'spw': [], 'filepath': [], 'mol_name': []}
syn_spec = []

for spw in spws:
    # read in the data
    data = datadir+'spw'+spw+'.imcontsub.scriptExtraction.forXCLASS.txt'
    NumHeaderLines = 0
    restfreq = 0
    vlsr = 0
    expdata = task_LoadASCIIFile.LoadASCIIFile(data, NumHeaderLines, restfreq, vlsr)

    # get min/max freq
    FreqMin = expdata[:,0].min()
    FreqMax = expdata[:,0].max()

    mol_list, molfit_spw = molfitGen(MolfitsFileName, FreqMin, FreqMax, spw)

    # run myXCLASS
    modeldata, log, TransEnergies, IntOpt, jobDir = task_myXCLASS.myXCLASS(FreqMin , FreqMax , FreqStep , TelescopeSize , Inter_Flag ,
                                                                           t_back_flag , tBack , tslope , nH_flag , N_H , beta_dust ,
                                                                           kappa_1300 , molfit_spw , iso_flag , IsoTableFileName , RestFreq , vLSR)
    syn_spec.append(jobDir+'xclass_spectrum_output.dat')
    # plot the synthetic spectrum against the observation color-coded by species
    # get the intensities of each species from myXCLASS results
    intensity_files = glob.glob(jobDir+'intensity*.dat')
    for i, species in enumerate(intensity_files):
        # use the molecule name in the file
        with open(species, 'r') as f:
            mol_name = ' '.join(f.readlines()[0].strip()[27:].split(';')[:-1])

        path_info['spw'].append(spw)
        path_info['filepath'].append(species)
        path_info['mol_name'].append(mol_name)

for k in path_info.keys():
    path_info[k] = np.array(path_info[k])

# get the colors and linestyles for all species.
plot_params = {'mol_name': [], 'color': [], 'linestyle': []}
legend = []
for i, mol in enumerate(mol_list):
    if i > 9:
        linestyle = '--'
    else:
        linestyle = '-'
    p, = plt.plot([], [], linestyle=linestyle, linewidth=1.5, label=mol_format(mol, format='formula'))
    legend.append(p)
    plot_params['mol_name'].append(mol)
    plot_params['color'].append(p.get_color())
    plot_params['linestyle'].append(p.get_linestyle())
for k in plot_params.keys():
    plot_params[k] = np.array(plot_params[k])

fig = plt.figure(figsize=(12, 15))
# grid = ImageGrid(fig, 111, nrows_ncols=(4,1), axes_pad=0.1, aspect=False)

for i in range(4):
    ax = fig.add_subplot(411+int(i))
    obs = ascii.read(datadir+'spw'+str(i)+'.imcontsub.scriptExtraction.forXCLASS.txt', names=['freq(MHz)', 'temp(K)'])
    ax.plot(obs['freq(MHz)'], obs['temp(K)'], label='observation', color='thistle', linewidth=0.7)

    # integrated Spectrum
    all_spec = ascii.read(syn_spec[i], header_start=None, data_start=4, names=['Frequency[MHz]', 'Tmb[K]'])
    ax.plot(all_spec['Frequency[MHz]'], all_spec['Tmb[K]'], label='all', color='k', linestyle='--', alpha=0.7)

    for s in path_info['filepath'][path_info['spw'] == str(i)]:
        mol_spec = ascii.read(s, header_start=None, data_start=4, names=['Frequnecy[MHz]', 'Tmb[K]'])
        mol_name = path_info['mol_name'][path_info['filepath'] == s]

        ax.plot(mol_spec['Frequnecy[MHz]'], mol_spec['Tmb[K]'],
                color=plot_params['color'][plot_params['mol_name'] == mol_name][0],
                linestyle=plot_params['linestyle'][plot_params['mol_name'] == mol_name][0], linewidth=1.5)

    ax.set_xlim([obs['freq(MHz)'].min(), obs['freq(MHz)'].max()])
    ax.set_ylim([-2,4])
    ax.minorticks_on()
    [ax.spines[axis].set_linewidth(1.5) for axis in ['top','bottom','left','right']]
    ax.tick_params('both',labelsize=16,width=1.5,which='major',pad=5,length=5)
    ax.tick_params('both',labelsize=16,width=1.5,which='minor',pad=5,length=2.5)
    ax.grid(True)

    if i == 0:
        ax.legend(handles=legend, loc='upper center', fontsize=12, ncol=5, bbox_to_anchor=(0.5, 1.4))
    if i == 3:
        ax.set_xlabel('Frequency [MHz]', fontsize=18)
        ax.set_ylabel(r'$T_{\rm mb}$ [K]', fontsize=18)

SaveFigureFile = 'xclass_spectrum_output_'+os.path.dirname(syn_spec[-1]).split('/')[-1]+'.pdf'
fig.tight_layout()
fig.savefig(SaveFigureFile, format='pdf', dpi=300, bbox_inches='tight')
