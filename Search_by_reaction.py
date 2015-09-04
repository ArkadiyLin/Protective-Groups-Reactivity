__author__ = 'arkadii'

import glob
import subprocess as sp
import sys
import ensure_dir


def search_by_reaction(number,folder,SMILES_reaction, PATH):
    files_mrv = glob.glob(folder + 'search_' + str(number+1) + '/' + '*.mrv')
    ensure_dir.ensure_dir(folder + 'temporary/')
    fn=0
    for file in files_mrv:
        g = open(file)
        ggg = g.readlines()
        g.close()
        fn+=1
        if len(ggg)>2:
            print(file)
            print ('Standardizing...')
            try:
                sp.call(['standardize', file, '-c', PATH+'/standardizer2.xml', '-f', 'rdf', '-o', file[:-3] + 'rdf'])
            except:
                print ('Not enough memory for Standardizer!!!')
                sys.exit()
            print ('Searching by reaction...')
            try:
                sp.call(['jcsearch', '-q', SMILES_reaction[number*2], '-f', 'MRV', '-o', folder + 'temporary/' + file.split('/')[-1], file[:-3] + 'rdf'])
            except:
                print ('Not enough memory for jcsearch!!!')
                sys.exit()
            print (file.split('/')[-1] + ' is done..')
            print (str(fn*100//len(files_mrv)) + '%')
    sp.call([PATH+'/molconvert_calling.sh', folder.rstrip('/'), str(number+1)])
    sp.call(["rm", "-r", folder + 'temporary/'])
    print ('Substructure search in jcsearch by reaction is done...')