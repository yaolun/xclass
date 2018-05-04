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


def mol_format(mol_name, name=True, formula=False):
    mol_info = [
    ('Methyl Formate',      'CH3OCHO v=0',          'CH$_{3}$OCHO $v=0$'),
    ('Acetaldehyde',        'CH3CHO v15=1',         'CH$_{3}$CHO $v_{t}=1$'),
    ('Methanol',            'C-13-H3OH v=0',        '$^{13}$CH$_{3}$OH $v_{t}=0$'),
    ('Methanol',            'CH2DOH v=0',           'CH$_{2}$DOH $v_{t}=0$'),
    ('Methanol',            'CH3OH v=0',            'CH$_{3}$OH $v_{t}=0$'),
    ('Sulfur Dioxide',      'SO2 v=0',              'SO$_{2}$ $v=0$'),
    ('Dimethyl Ether',      'CH3OCH3 v=0',          'CH$_{3}$OCH$_{3}$ $v=0$'),
    ('Ethanol',             'C2H5OH v=0',           'C$_{2}$H$_{5}$OH $v=0$'),
    ('Ethyl Cyanide',       'C2H5CN v=0',           'C$_{2}$H$_{5}$CN $v=0$'),
    ('Methylamine',         'CH3NH2 v=0',           'CH$_{3}$NH$_{2}$ $v=0$'),
    ('Thioformaldehyde',    'H2CS v=0',             'H$_{2}$CS $v=0$'),
    ('Formyl radical',      'HCO v=0',              'HCO $v=0$'),
    ('Acetone',             'CH3COCH3 v=0',         'CH$_{3}$COCH$_{3}$ $v=0$'),
    ('Methyl Cyanide',      'CH2DCN v=0',           'CH$_{2}$DCN $v=0$'),
    ('Aminoethanol',        'NH2CH2CH2OH v25=1',    'NH$_{2}$CH$_{2}$CH$_{2}$OH $v_{25}=1$'),
    ('Nitric acid',         'HNO3 v=0',             'HNO$_{3}$ $v=0$'),
    ('Ethylene Glycol',     "aGg'-(CH2OH)2 v=0 ",   r'g\prime Ga-(CH$_{2}$OH)$_{2}$ $v=0$'),
    ('n-Propanol',          'Ga-n-C3H7OH v=0',      'Ga-n-C$_{3}$H$_{7}$OH $v=0$'),
    ('Vinyl Cyanide',       'H2CCCHCN v=0',         'H$_{2}$CCCHCN $v=0$'),
    ('Glycolaldehyde',      'HCOCH2OH v18=1',       'HCOCH$_{2}$OH $v_{18}=1$'),
    ('Thiozone',            'S3 v=0',               'S$_{3}$ $v=0$'),
    ('Bromine dioxide',     'OBr-81-O v=0',         'O$^{81}$BrO $v=0$'),
    ('Formamide',           'NH2CHO v=0',           'NH$_{2}$CHO $v=0$'),
    ('Hydroxyacetone',      'C3H6O2 v=0',           'C$_{3}$H$_{6}$O$_{2}$ $v=0$'),
    ('Propane',             'C3H8 v=0',             'C$_{3}$H$_{8}$ $v=0$'),
    ('Disulfurmonoxide',    'S2O v=0',              'S$_{2}$O $v=0$'),
    ('Dihydroxyacetone',    'C3O3H6 v=0',           'C$_{3}$O$_{3}$H$_{6}$ $v=0$'),
    ('Acetaldehyde',        'CH3CHO v15=2',         'CH$_{3}$CHO $v_{15}=2$')]

    for i, m in enumerate(mol_info):
        if m[1] == mol_name:
            if name:
                return m[0]
            elif formula:
                return m[2]


import task_LoadASCIIFile
import task_myXCLASS
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.lines as mlines
from astropy.io import ascii
import glob
import numpy as np

# fixed parameters for myXCLASS
MolfitsFileName = os.path.expanduser('~')+'/programs/xclass/coms.molfit'

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
iso_flag = False
IsoTableFileName = ''
RestFreq = 0
vLSR = 0

# iterate through all spws
spws = ['0', '1', '2', '3']
path_info = {'spw': [], 'filepath': [], 'mol_name': []}
syn_spec = []

for spw in spws:
    data = 'spw'+spw+'.imcontsub.scriptExtraction.forXCLASS.txt'
    NumHeaderLines = 0
    restfreq = 0
    vlsr = 0
    expdata = task_LoadASCIIFile.LoadASCIIFile(data, NumHeaderLines, restfreq, vlsr)

    FreqMin = expdata[:,0].min()
    FreqMax = expdata[:,0].max()

    mol_list, molfit_spw = molfitGen(MolfitsFileName, FreqMin, FreqMax, spw)


    modeldata, log, TransEnergies, IntOpt, jobDir = task_myXCLASS.myXCLASS(FreqMin , FreqMax , FreqStep , TelescopeSize , Inter_Flag ,
                                                                           t_back_flag , tBack , tslope , nH_flag , N_H , beta_dust ,
                                                                           kappa_1300 , molfit_spw , iso_flag , IsoTableFileName , RestFreq , vLSR)
    syn_spec.append(jobDir+'xclass_spectrum_output.dat')
    # plot the synthetic spectrum against the observation color-coded by species
    # get the intensities of each species from myXCLASS results
    intensity_files = glob.glob(jobDir+'intensity*.dat')
    for i, species in enumerate(intensity_files):
        mol_name = ' '.join(species.split('intensity')[1].split('comp')[0][2:-3].split('_'))

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
    p, = plt.plot([], [], linestyle=linestyle, label=mol_format(mol, formula=True, name=False))
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
    obs = ascii.read('spw'+str(i)+'.imcontsub.scriptExtraction.forXCLASS.txt', names=['freq(MHz)', 'temp(K)'])
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
    ax.set_ylim([-5,10])
    ax.minorticks_on()
    [ax.spines[axis].set_linewidth(1.5) for axis in ['top','bottom','left','right']]
    ax.tick_params('both',labelsize=16,width=1.5,which='major',pad=5,length=5)
    ax.tick_params('both',labelsize=16,width=1.5,which='minor',pad=5,length=2.5)
    ax.grid(True)

    if i == 0:
        ax.legend(handles=legend, loc='upper center', fontsize=12, ncol=5, bbox_to_anchor=(0.5, 1.4))
    if i == 3:
        ax.set_xlabel('Frequency [MHz]', fontsize=18)
        ax.set_ylabel(r'T$_{\rm mb}$ [K]', fontsize=18)

SaveFigureFile = 'xclass_spectrum_output_'+os.path.dirname(syn_spec[-1]).split('/')[-1]+'.pdf'
fig.tight_layout()
fig.savefig(SaveFigureFile, format='pdf', dpi=300, bbox_inches='tight')
