import os, glob
from astropy.io import ascii
import matplotlib.pyplot as plt
from mol_format import mol_format
import numpy as np

# get the latest myXCLASS results
files = glob.glob('/Volumes/SD-Mac/XCLASS-Interface/run/myXCLASS/*')
files.sort(key=os.path.getmtime)
jobdirs = files[-4:]

syn_spec = [(jobDir+'/xclass_spectrum_output.dat') for jobDir in jobdirs]
path_info = {'spw': [], 'filepath': [], 'mol_name': []}
for jobDir in jobdirs:
    intensity_files = glob.glob(jobDir+'/intensity*.dat')
    spw = glob.glob(jobDir+'/coms_spw*.molfit')[0].split('spw')[1][0]
    for i, species in enumerate(intensity_files):
        mol_name = ' '.join(species.split('intensity')[1].split('comp')[0][2:-3].split('_'))

        path_info['spw'].append(spw)
        path_info['filepath'].append(species)
        path_info['mol_name'].append(mol_name)

for k in path_info.keys():
    path_info[k] = np.array(path_info[k])

# get the molecule list from the latest molfit
molfit = '/Users/yaolun/programs/xclass/coms.molfit'
molfit_data = open(molfit, 'r').readlines()
mol_list = []
for i, line in enumerate(molfit_data):
    if line.startswith('%'):
        continue
    if len(line.strip().split()) == 2:
        mol_list.append(' '.join(line.strip().split()[0].split(';')[:-1]))

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

# L483 files
filepaths = ['/Volumes/SD-Mac/Google Drive/research/bhr71_infall/L483/hcn-l483.dat',
             '/Volumes/SD-Mac/Google Drive/research/bhr71_infall/L483/hcop-l483.dat',
             '/Volumes/SD-Mac/Google Drive/research/bhr71_infall/L483/cs-l483.dat',
             '/Volumes/SD-Mac/Google Drive/research/bhr71_infall/L483/h13cn-l483.dat']
beams = [(0.36, 0.26), (0.30, 0.20), (0.36, 0.26), (0.28, 0.21)]
def jyperbeam2temp(freq, flux, beam):
    """
    freq: MHz
    flux: Jy/beam
    """
    t = flux*(13.6*(3e5/freq)**2/(beam[0]*beam[1]))
    return t

# make the plot
fig = plt.figure(figsize=(12, 15))

for i in range(4):
    ax = fig.add_subplot(411+int(i))

    # spectra of compared source
    obs_compared = ascii.read(filepaths[i], names=['freq(GHz)', 'flux(Jy/bm)'], data_start=1, header_start=None)
    ax.plot(obs_compared['freq(GHz)']*1e3, jyperbeam2temp(obs_compared['freq(GHz)']*1e3, obs_compared['flux(Jy/bm)'], beams[i]),
            label='L483', color='k', linewidth=0.7, alpha=0.7)

    # observed spectrum
    obs = ascii.read('spw'+str(i)+'.imcontsub.scriptExtraction.forXCLASS.txt', names=['freq(MHz)', 'temp(K)'])
    ax.plot(obs['freq(MHz)'], obs['temp(K)'], label='observation', color='thistle', linewidth=0.7)

    # integrated spectrum
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
        ax.legend(handles=legend, loc='upper center', fontsize=12, ncol=5, bbox_to_anchor=(0.5, 1.5))
    if i == 3:
        ax.set_xlabel('Frequency [MHz]', fontsize=18)
        ax.set_ylabel(r'T$_{\rm mb}$ [K]', fontsize=18)

SaveFigureFile = 'xclass_spectrum_output_'+os.path.dirname(syn_spec[-1]).split('/')[-1]+'.pdf'
fig.tight_layout()
fig.savefig(SaveFigureFile, format='pdf', dpi=300, bbox_inches='tight')
