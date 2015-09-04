__author__ = 'arkadii'

import glob
import ensure_dir
import subprocess as sp


def substructure_search(folder_for_data, folder_for_standardized_data, SMILES):
    ensure_dir.ensure_dir(folder_for_data)
    files_stand_rdf = glob.glob(folder_for_standardized_data)
    for number, smiles in enumerate(SMILES):
        ensure_dir.ensure_dir(folder_for_data + 'search_' + str(number+1) + '/')
        for file in files_stand_rdf:
            print ('Searching of ' + smiles + ' in ' + file.split('/')[-1][0:-9] + 'mrv')
            sp.call(['jcsearch', '-q', smiles, '-f', 'MRV', '-o', folder_for_data + 'search_' + str(number+1) + '/' + file.split('/')[-1][0:-9] + 'mrv', file])
    print ('Searching ended...')