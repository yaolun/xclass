def mol_format(mol_name, format='name'):
    mol_info = [
    ('Methyl formate',      'CH3OCHO v=0',          'CH$_{3}$OCHO'),
    ('Acetaldehyde',        'CH3CHO v15=1',         'CH$_{3}$CHO $v_{t}=1$'),
    ('13C-Methanol',        'C-13-H3OH v=0',        '$^{13}$CH$_{3}$OH'),
    ('D-Methanol',          'CH2DOH v=0',           'CH$_{2}$DOH'),
    ('Methanol',            'CH3OH v=0',            'CH$_{3}$OH'),
    ('Sulfur dioxide',      'SO2 v=0',              'SO$_{2}$'),
    ('Dimethyl ether',      'CH3OCH3 v=0',          'CH$_{3}$OCH$_{3}$'),
    ('Ethanol',             'C2H5OH v=0',           'C$_{2}$H$_{5}$OH'),
    ('Ethyl cyanide',       'C2H5CN v=0',           'C$_{2}$H$_{5}$CN'),
    ('Methylamine',         'CH3NH2 v=0',           'CH$_{3}$NH$_{2}$'),
    ('Thioformaldehyde',    'H2CS v=0',             'H$_{2}$CS'),
    ('Formyl radical',      'HCO v=0',              'HCO'),
    ('Acetone',             'CH3COCH3 v=0',         'CH$_{3}$COCH$_{3}$'),
    ('Methyl cyanide',      'CH2DCN v=0',           'CH$_{2}$DCN'),
    ('Aminoethanol',        'NH2CH2CH2OH v25=1',    'NH$_{2}$CH$_{2}$CH$_{2}$OH $v_{25}=1$'),
    ('Nitric acid',         'HNO3 v=0',             'HNO$_{3}$'),
    ('Ethylene glycol',     "aGg'-(CH2OH)2 v=0",    r'g$\prime$Ga-(CH$_{2}$OH)$_{2}$'),
    ('n-Propanol',          'Ga-n-C3H7OH v=0',      'Ga-n-C$_{3}$H$_{7}$OH'),
    ('Vinyl cyanide',       'H2CCCHCN v=0',         'H$_{2}$CCCHCN'),
    ('Glycolaldehyde',      'HCOCH2OH v18=1',       'HCOCH$_{2}$OH $v_{18}=1$'),
    ('Thiozone',            'S3 v=0',               'S$_{3}$'),
    ('Bromine dioxide',     'OBr-81-O v=0',         'O$^{81}$BrO'),
    ('Formamide',           'NH2CHO v=0',           'NH$_{2}$CHO'),
    ('Hydroxyacetone',      'C3H6O2 v=0',           'C$_{3}$H$_{6}$O$_{2}$'),
    ('Propane',             'C3H8 v=0',             'C$_{3}$H$_{8}$'),
    ('Disulfurmonoxide',    'S2O v=0',              'S$_{2}$O'),
    ('Dihydroxyacetone',    'C3O3H6 v=0',           'C$_{3}$O$_{3}$H$_{6}$'),
    ('Acetaldehyde',        'CH3CHO v15=2',         'CH$_{3}$CHO $v_{15}=2$'),
    ('Propargyl alcohol',   'HCCCH2OH v=0',         'HCCCH$_{2}$OH'),
    ('Ketene',              'HDCCO v=0',            'HDCCO'),
    ('Hydrogen cyanide (v2=1)','HCN v2=1',          'HCN $v_{2}=1$'),
    ('Cyanamide',           'NH2CN v=0',            'NH$_{2}$CN')]

    for i, m in enumerate(mol_info):
        if m[1] == mol_name:
            if format == 'name':
                return m[0]
            elif format == 'formula':
                return m[2]

    # in case no match is found.
    return mol_name
