def splatalogueReader(csvdata):
    import numpy as np
    foo = open(csvdata).readlines()
    header = foo[0].strip().split(':')
    moldata = {'nu0':[], 'Eu':[], 'El':[], 'Einstein-A':[], 'gu':[]}
    for line in foo[1:]:
        nu0 = float(line.strip().split(':')[header.index('Freq-MHz')])*1e6
        Eu = float(line.strip().split(':')[header.index('E_U (K)')])
        El = float(line.strip().split(':')[header.index('E_L (K)')])
        EA = 10**float(line.strip().split(':')[header.index('Log<sub>10</sub> (A<sub>ij</sub>)')])
        gu = float(line.strip().split(':')[header.index('Upper State Degeneracy')])
        moldata['nu0'].append(nu0)
        moldata['Eu'].append(Eu)
        moldata['El'].append(El)
        moldata['Einstein-A'].append(EA)
        moldata['gu'].append(gu)

    for k in moldata.keys():
        moldata[k] = np.array(moldata[k])

    return moldata
