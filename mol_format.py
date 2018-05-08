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
