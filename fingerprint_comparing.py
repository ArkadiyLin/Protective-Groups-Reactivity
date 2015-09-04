__author__ = 'arkadii'

import sys

def fingerprint_comparing(way_basa, way_query, folder_for_ID, etalon_begin, etalon_end):
    f = open(way_basa, 'r')
    basa = f.readlines()
    f.close()
    
    g = open(way_query, 'r')
    if etalon_end!=0:
        etalon = g.readlines()[etalon_begin:etalon_end]
    if etalon_end==0:
        etalon = g.readlines()[etalon_begin:]
    g.close()

    ID = []
    ID_used = []

    if len(etalon) % 2 != 0:
        print ('Error in query!!!')
        sys.exit()

    for eta_counter, eta in enumerate(etalon):
        out = open(folder_for_ID + 'ID_'+str(eta_counter+1)+'.txt', 'w')
        positions = [i for i, x in enumerate(eta.split('\t')[-1].rstrip('\n')) if x=='1']
        for line_counter, line in enumerate(basa):
            i=0
            id = line.split('\t')[0]
            ID.append(id)
            while (i<len(positions) and ord(line.split('\t')[-1].rstrip('\n')[positions[i]])-ord(eta.split('\t')[-1].rstrip('\n')[positions[i]])==0):
                i+=1
            if i==len(positions):
                out.write(id)
                ID_used.append(id)
                if line_counter<len(basa)-1:
                    out.write('\n')
        out.close()

    out = open(folder_for_ID + 'ID_'+str(len(etalon)+1)+'.txt', 'w')
    for id in ID:
        if id not in ID_used:
            out.write(id + '\n')

    out.close()