__author__ = 'arkadii'

import pickle

def finder_descriptions(folder_in, folder_out, files, PATH):

    for filename in files:
        f=open(folder_in + filename, 'r')
        ID=f.read().split(',')
        f.close()

        g=open(PATH+'/descriptions_bin', 'rb')
        DESCR=pickle.load(g)
        g.close()

        r=open(folder_out + 'descr_' + filename[:-4] + '.csv', 'w')

        r.write('RX_ID;COND_ID;CL;LB;T;P;TIM;STP;RGT;CAT;SOL;YD;NYD;LCN;YPRO;CIT;TXT\n')

        if len(ID)==0:
            continue

        for id in ID:
            if id=='':
                continue
            for line in DESCR[id]:
                r.write(line.rstrip('\n')+'\n')

        r.close()