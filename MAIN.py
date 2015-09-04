__author__ = 'arkadii'

import glob
import rdf_parser
import subprocess as sp
import ensure_dir
import mols_finder
import fingerprint_comparing
import finder_descriptions_on_id
import parser_fingerprint
import CAT_separation
import Smiles_read
import substructure_search
import Search_by_reaction
import Ramil_scripts
import sys
from os import path

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#================================ARGUMENTS==========================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if len(sys.argv)>1:
    n1=int(sys.argv[1])
    n2=int(sys.argv[2])
    n5=int(sys.argv[3])
    n7=int(sys.argv[4])
    n6=int(sys.argv[5])
else:
    n1 = int(input('Parse?: '))
    n2 = int(input('Standardize?: '))
    n5 = int(input('Cross comparing?: '))
    n7 = int(input('Substructure searches?: '))
    n6 = int(input('Maximum number of dynamic bonds?: '))

PATH = path.dirname(__file__)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#=======================PARSING OF INITIAL DATABASE=================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

ensure_dir.ensure_dir(PATH  + '/RDFs_from_INITIAL/')
if n1 == 1:
    rdf_parser.rdf_parser(PATH + '/INITIAL/*.rdf', PATH + '/RDFs_from_INITIAL/', PATH+'/descriptions.csv')
    print('Database is parsed...')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#====================STANDARDIZING OF PARSED DATABASE===============================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

files_mols_rdf = glob.glob(PATH+'/RDFs_from_INITIAL/*.mols.rdf')
ensure_dir.ensure_dir(PATH+'/STANDARDIZED_RDFs/')
if n2 == 1:
    for file in files_mols_rdf:
        print ('Standardizing of ' + file[18:])
        sp.call(['standardize', file, '-c', PATH + '/standardizer.xml', '-f', 'rdf', '-o', PATH+'/STANDARDIZED_RDFs/' + file.split('/')[-1][0:-9] + '.stand.rdf'])
    print ('Files are standardized!')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#===========================SMILES READING=========================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

SMILES = []
SMILES_reaction = []
SMILES, SMILES_reaction = Smiles_read.smiles_read(PATH+'/Query/', 'SMILES_reaction.smarts')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#=======================ENDING OF SMILES READING===================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#==================SUBSTRUCTURE SEARCH BY MOLECULE SMILES==========================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if n7==1:
    substructure_search.substructure_search(PATH+'/SUBSTRUCTURE_SEARCH/', PATH+'/STANDARDIZED_RDFs/*.stand.rdf', SMILES)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#===============SUBSTRUCTURE SEARCH BY MOLECULE SMILES ENDED=======================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#===CONVERTION FROM MRV TO RDF, BASE MAPPING AND SUBSTRUCTURE SEARCH BY REACTION===
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if n7==1:
    for number in range(len(SMILES)):
        Search_by_reaction.search_by_reaction(number, PATH+'/SUBSTRUCTURE_SEARCH/', SMILES_reaction, PATH)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#=================SUBSTRUCTURE SEARCH BY REACTION IS DONE==========================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#ensure_dir.ensure_dir('REACTION_COMBINATIONS/')
ensure_dir.ensure_dir(PATH+'/MAPPED_REACTIONS/')
ensure_dir.ensure_dir(PATH+'/CGR/')
ensure_dir.ensure_dir(PATH+'/SEARCH_ON_FINGERPRINTS/')
ensure_dir.ensure_dir(PATH+'/DESCRIPTIONS/')
ensure_dir.ensure_dir(PATH+'/RESULTS/')
ensure_dir.ensure_dir(PATH+'/FINGERPRINTS/')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#============================QUERY TREATMENT=======================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

print ("Query's fingerprint preparing...")
Ramil_scripts.ramil_scripts('query', 'query', n6, PATH)
print ("Fingerprints query has been made and put into folder FINGERPRINTS...")

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#=======================QUERY TREATMENT IS FINISHED================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#=============================PAIRS TREATMENT======================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

for pair in range(1, len(SMILES)+1):
    if path.exists(PATH+'/SUBSTRUCTURE_SEARCH/output.search_' + str(pair) + '.rdf'):
        print ('mols_finder is running now..')
        mols_finder.mols_finder(PATH+'/SUBSTRUCTURE_SEARCH/ID_' + str(pair) + '.txt', PATH+'/SUBSTRUCTURE_SEARCH/output.search_' + str(pair) + '.rdf', PATH+'/MAPPED_REACTIONS/MOLS_' + str(pair) + '.rdf')
        print ('mols_finder is finished..')
        """
        f = open('REACTION_COMBINATIONS/MOLS_' + str(pair) + '.rdf', 'r')
        lines = f.read()
        f.close()
        u = open('MAPPED_REACTIONS/MOLS_' + str(pair) + '.rdf', 'w')
        u.write('$RDFILE 1\n$DATM 2012-10-16 06:03:34\n' + lines)
        u.close()
        """
        print ("Ramil's script run...")
        Ramil_scripts.ramil_scripts('output_' + str(pair), 'base', n6, PATH)
        print ("Fingerprints for pair " + str(pair) + " has been made and put into folder FINGERPRINTS...")
        ensure_dir.ensure_dir(PATH+'/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/')
        print ('Fingerprint comparing...')
        if pair<len(SMILES):
            fingerprint_comparing.fingerprint_comparing(PATH+"/FINGERPRINTS/fingerprint_output_" + str(pair) + ".txt", PATH+"/FINGERPRINTS/fingerprint_query.txt", PATH+'/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/', (pair-1)*2, pair*2)
        if pair==len(SMILES):
            fingerprint_comparing.fingerprint_comparing(PATH+"/FINGERPRINTS/fingerprint_output_" + str(pair) + ".txt", PATH+"/FINGERPRINTS/fingerprint_query.txt", PATH+'/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/', (pair-1)*2, 0)
        parser_fingerprint.parser_fingerprint(PATH+'/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/')
        ensure_dir.ensure_dir(PATH+'/DESCRIPTIONS/' + str(pair) + '/')
        finder_descriptions_on_id.finder_descriptions(PATH+'/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/', PATH+'/DESCRIPTIONS/' + str(pair) + '/', ['1.txt', '2.txt'], PATH)
        print ('Descriptions have been found...')
        ensure_dir.ensure_dir(PATH+'/RESULTS/' + str(pair) + '/')
        CAT_separation.cat_separation(PATH+'/DESCRIPTIONS/' + str(pair) + '/', PATH+'/RESULTS/' + str(pair) + '/', True, PATH+'/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/', False, PATH)
        print ('Result table was constructed...')
    else:
        print('No reactions have been found!!!')


if n5==1:
    pairs = []
    for i in range(1, len(SMILES)):
        for j in range(i+1, len(SMILES)+1):
            pairs.append(str(i) + "-" + str(j))

    for pair in pairs:
        print('Begining of pair comparing for pair' + pair + '...')
        ensure_dir.ensure_dir(PATH+'/RESULTS/' + pair + '/')
        dict1_1 = {}
        dict1_2 = {}
        dict2_1 = {}
        dict2_2 = {}
        DICT = {}
        f = open(PATH+'/RESULTS/' + pair.split('-')[0] + '/result_dictionary2.txt')
        dd = f.read()
        ID1_1 = dd.split("Class 1:\n")[1].split("Class 2:\n")[0].split('\n')[:-1]
        ID1_2 = dd.split("Class 2:\n")[1].split("\nID from the trash:\n")[0].split('\n')[:-1]
        f.close()
        g = open(PATH+'/RESULTS/' + pair.split('-')[-1] + '/result_dictionary2.txt')
        dd = g.read()
        ID2_1 = dd.split("Class 1:\n")[1].split("Class 2:\n")[0].split('\n')[:-1]
        ID2_2 = dd.split("Class 2:\n")[1].split("\nID from the trash:\n")[0].split('\n')[:-1]
        g.close()
        catalysts = []
        for i in range(len(ID1_1)//2):
            dict1_1['_'.join(ID1_1[i*2].split(' ')[3:-2])] = ID1_1[i*2+1].rstrip('\n').split(',')
            dict1_2['_'.join(ID1_2[i*2].split(' ')[3:-2])] = ID1_2[i*2+1].rstrip('\n').split(',')
            catalysts.append('_'.join(ID1_1[i*2].split(' ')[3:-2]))
        for i in range(len(ID2_1)//2):
            dict2_1['_'.join(ID2_1[i*2].split(' ')[3:-2])] = ID2_1[i*2+1].rstrip('\n').split(',')
            dict2_2['_'.join(ID2_2[i*2].split(' ')[3:-2])] = ID2_2[i*2+1].rstrip('\n').split(',')
            if '_'.join(ID2_1[i*2].split(' ')[3:-2]) not in catalysts:
                catalysts.append('_'.join(ID2_1[i*2].split(' ')[3:-2]))
        ID1 = []
        ID2 = []
        ID3 = []
        ID4 = []
        for cat in catalysts:
            try:
                if len(list(set(dict1_2[cat]) & set(dict2_1[cat])))>0:
                    ID1 += list(set(dict1_2[cat]) & set(dict2_1[cat]))
            except:
                pass
            try:
                if len(list(set(dict1_1[cat]) & set(dict2_1[cat])))>0:
                    ID2 += list(set(dict1_1[cat]) & set(dict2_1[cat]))
            except:
                pass
            try:
                if len(list(set(dict1_1[cat]) & set(dict2_2[cat])))>0:
                    ID3 += list(set(dict1_1[cat]) & set(dict2_2[cat]))
            except:
                pass
            try:
                if len(list(set(dict1_2[cat]) & set(dict2_2[cat])))>0:
                    ID4 += list(set(dict1_2[cat]) & set(dict2_2[cat]))
            except:
                pass
        id =[ID1, ID2, ID3, ID4]
        ensure_dir.ensure_dir(PATH + '/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/')
        for i in range(1,5):
            out = open(PATH+'/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/' + str(i) + '.txt', 'w')
            out.write(','.join([str(j) for j in id[i-1] if j!='']))
            out.close()
        ensure_dir.ensure_dir(PATH+'/DESCRIPTIONS/' + str(pair) + '/')
        finder_descriptions_on_id.finder_descriptions(PATH+'/SEARCH_ON_FINGERPRINTS/search_' + str(pair) + '/', PATH+'/DESCRIPTIONS/' + str(pair) + '/', ['1.txt', '2.txt', '3.txt', '4.txt'], PATH)
        ensure_dir.ensure_dir(PATH+'/RESULTS/' + str(pair) + '/')
        CAT_separation.cat_separation(PATH+'/DESCRIPTIONS/' + str(pair) + '/', PATH+'/RESULTS/' + str(pair) + '/', False, '', True, PATH)
        print('Ending of cross comparing for pair ' + pair + '...')


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#==============================PAIRS TREATMENT END==================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#===================================END OF CODE=====================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!