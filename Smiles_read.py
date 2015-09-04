__author__ = 'arkadii'

import subprocess as sp

def smiles_read(folder, way_smiles_reaction):
    f = open(folder + way_smiles_reaction)
    SMR = f.readlines()
    f.close()
    SMILES = []
    SMILES_reaction = []
    for i in range(len(SMR)):
        SMILES.append(SMR[i].split('>>')[0].strip())
    out = open(folder + 'query.smarts', 'w')
    for i in range(len(SMR)):
        SMILES_reaction.append(SMR[i].rstrip('\n'))
        SMILES_reaction.append(SMR[i].rstrip('\n').split('>>')[0] + '>>' + SMR[i].rstrip('\n').split('>>')[0])
    out.write('\n'.join(SMILES_reaction))
    out.close()
    sp.call(['molconvert', 'rdf', folder + 'query.smarts', '-o', folder + 'query.mapped.rdf'])
    print ('Smiles has been read...')
    return SMILES, SMILES_reaction