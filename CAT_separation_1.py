__author__ = 'arkadii'

import glob
import string

files = glob.glob('DESCRIPTIONS/1/*_AFTER_CAT_ANALYSIS.csv')

nfiles = len(files) #Number of files

metals = ['Pd', 'Pt', 'Lindlar', 'Ni', 'Rh', 'Au', 'Fe', 'Ir', 'Ru']

results = [[0 for j in range(nfiles*4+1)] for i in range(len(metals) + 2)]

results[0][0] = ''
results[1][0] = ''
for i in range(len(metals)):
    results[i+2][0] = metals[i]

reaction_number = 0.0
number_of_empty_reactions = 0
i = 1
s = 0

ID = []

files.sort()

for filename in files:#Go to the file
    f = open(filename)
    DESCR = f.readlines()[1:]
    f.close()

    ID.append([])
    for catalysts in xrange(len(metals)):
        ID[s].append([])

    results[0][i] = 'Class ' + str(s+1)#filename[19:-23] #Write names of files
    results[0][i+1] = len(DESCR)# - 1 #Write total number of reactions in this file
    results[0][i+2] = ''
    results[0][i+3] = ''
    reaction_number += len(DESCR)# - 1
    results[1][i] = 'N'
    results[1][i+1] = 'N, %'
    results[1][i+2] = 'NYD'
    results[1][i+3] = 's'

    for descr in DESCR:#Go to the line
        cat = descr.split(';')[6].lstrip('"').rstrip('"').split('|')[0].split(',')
        try:
            yields = float(descr.split(';')[9])

            for v in cat:#We analyze catalysts
                for r in range(len(metals)):
                    if v == metals[r]:
                        results[r+2][i] = int(results[r+2][i]) + 1
                        results[r+2][i+2] = round((float(results[r+2][i+2]) * (results[r+2][i]-1) + yields) / results[r+2][i], 2)
                        ID[s][r].append(descr.split(';')[0])

                if v == '':
                    number_of_empty_reactions += 1
        except:
            number_of_empty_reactions += 1
            continue

    for descr in DESCR:#Go to the line
        cat = descr.split(';')[6].lstrip('"').rstrip('"').split('|')[0].split(',')
        try:
            yields = float(descr.split(';')[9])

            for v in cat:#We analyze catalysts
                for r in range(len(metals)):
                    if v == metals[r]:
                        results[r+2][i+3] += (yields - results[r+2][i+2]) ** 2
        except:
            continue
    i+=4
    s +=1


for j in range(2, len(metals)+2):
    i = 1
    number_reactions_on_this_cat = 0
    k=1
    for filename1 in files:
        number_reactions_on_this_cat += results[j][k]
        k+=4
    for filename1 in files:
        if number_reactions_on_this_cat != 0:
            results[j][i+1] = round(results[j][i] * 100.0 / number_reactions_on_this_cat, 2)
        if results[j][i] > 1:
            results[j][i+3] = round((float(results[j][i+3]) / (results[j][i]-1)) ** (1.0/2), 2)
        i+=4


out = open('RESULTS/1/result.txt', 'w')

for a in range(len(metals)+4):
    k = 1
    if a!=2 and a!=len(metals)+3:
        if a==0 or a==1:
            i=a
        if a > 2:
            i = a-1
        out.write('%s %s' % (string.ljust(str(results[i][0]), 7), string.center('|', 1)))
        for j in files:
            out.write(' %s  %s  %s  %s %s' % (string.rjust(str(results[i][k]), 12), string.rjust(str(results[i][k+1]), 5), string.rjust(str(results[i][k+2]), 5), string.rjust(str(results[i][k+3]), 5), string.center('|', 1)))
            k+=4
        out.write('\n')
    if a==2 or a==len(metals)+3:
        for r in range(13):
            out.write('%s' % (string.center('-', 1)))
        for j in files:
            for r in range(35):
                out.write('%s' % (string.center('-', 1)))
        out.write('\n')

out.write('\n' + str(number_of_empty_reactions) + ' did not have catalyst or yield.\n\n')

f = open('SEARCH_ON_FINGERPRINTS/search_1/3.txt')
ID_5 = f.readlines()
f.close()
length = len(ID_5)

out.write(str(length) + ' elements are in the trash.\n\n')
out.write('N - number of reactions\n')
out.write('N, % - number of reactions in percent, %\n')
out.write('NYD - mean yield of reactions in this type of transformation, %\n')
out.write('s - dispersion of NYD, %\n\n')
i=1
for filename in files:
    out.write('Class ' + str(i) + ' represent file ' + filename + '\n')
    i += 1

out.write('\n')

s=0

for filename in files:
    out.write(results[0][s*4+1] + ' means the file' + filename[19:-23] + ':\n')
    m=0
    for metal in range(len(metals)):
        if int(results[metal+2][s*4+1]) != 0:
            out.write("Reaction's ID for " + metals[metal] + ' as catalyst:\n')
            out.write(','.join(ID[s][metal]) + '\n')
            m = m + results[metal+2][s*4+1]
    s += 1

out.write('\n')

out.write('ID from the trash:\n')
out.write(''.join(ID_5))

out.close()