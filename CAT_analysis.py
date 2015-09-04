__author__ = 'arkadii'

import glob

def cat_analysis(folder_in):
    f = open('DICTIONARY_FINAL_VERSION.txt', 'r')
    dict = f.readlines()
    f.close()

    dictionary = {}

    for i in dict:
        dictionary[i.split(':')[0]] = i.split(':')[1].rstrip('\n')

    files = glob.glob(folder_in + '*.csv')

    files.sort()

    for filename in files:
        g = open(filename, 'r')
        descr = g.readlines()
        g.close()

        out = open(filename[:-4] + '_AFTER_CAT_ANALYSIS.csv', 'w')

        line1 = descr[0].split(';')

        out.write(line1[0] + ';' + line1[1] + ';' + line1[4] + ';' + line1[5] + ';' + line1[6] + ';' + line1[7] + ';')
        out.write(line1[9] + ';' + line1[10] +';' + line1[11] + ';' + line1[12] + ';' + line1[-1].rstrip('\n') + '\n')


        for i in xrange(1, len(descr)):
            line = descr[i].split(';')
            out.write(line[0] + ';' + line[1] + ';' + line[4] + ';' + line[5] + ';' + line[6] + ';' + line[7] + ';')
            rgt = line[8].lstrip('"').rstrip('"').split('|')
            cat = line[9].lstrip('"').rstrip('"').split('|')
            CAT = []
            for j in rgt:
                if j in dictionary.keys():
                    CAT.append(dictionary[j])
            for j in cat:
                if j in dictionary.keys():
                    CAT.append(dictionary[j])
            CAT = set(CAT)
            out.write('"' + ','.join(CAT) + '|' + '|'.join(rgt) + '|' + '|'.join(cat) + '"' + ';')
            out.write(line[10] + ';' + line[11] + ';' + line[12] + ';' + line[-1].rstrip('\n') + '\n')

        out.close()