__author__ = 'arkadii'

import glob
import string



def cat_separation(folder_in, folder_result, garbage, folder_garbage, double_comparison, PATH):
    files = glob.glob(folder_in + '*.csv')

    nfiles = len(files) #Number of files

    g = open (PATH+'/DICTIONARY_1.txt')
    dict1 = g.readlines()
    g.close()

    dictionary1 = {}

    for line in dict1:
        dictionary1[line.split(':')[0].strip()] = line.split(':')[1].lstrip(' ').rstrip('\n')

    g = open(PATH+'/DICTIONARY_2.txt')
    dict2 = g.readlines()
    g.close()

    dictionary2 = {}
    dictionary3 = {}
    dictionary4 = {}

    dictionaries = [dictionary2, dictionary3, dictionary4]

    for line in dict2:
        dictionary2[line.split(';')[0].strip()] = line.split(';')[1].lstrip(' ').rstrip(' ')
        dictionary3[line.split(';')[0].strip()] = line.split(';')[2].lstrip(' ').rstrip(' ')
        dictionary4[line.split(';')[0].strip()] = line.split(';')[3].lstrip(' ').rstrip(' ').rstrip('\n')

    results1 = {}
    results2 = {}
    results3 = {}

    RESULTS = [results1, results2, results3]

    reaction_number = []
    number_of_empty_reactions = [0, 0, 0]

    ID1 = {}
    ID2 = {}
    ID3 = {}

    id = [ID1, ID2, ID3]

    files.sort()

    for file_number, filename in enumerate(files):#Go to the file
        f = open(filename)
        DESCR = f.readlines()[1:]
        f.close()

        reaction_number.append(len(DESCR))


        for descr in DESCR:#Go to the line
            rgt = descr.split(';')[8].lstrip('"').rstrip('"').split('|')
            cat = descr.split(';')[9].lstrip('"').rstrip('"').split('|')

            for result_position, results in enumerate(RESULTS):
                try:
                    yields = float(descr.split(';')[12])
                    CAT = []
                    for r in rgt:
                        try:
                            if (dictionaries[result_position])[dictionary1[r]] != '':
                                CAT.append((dictionaries[result_position])[dictionary1[r]])
                        except:
                            continue
                    for c in cat:
                        try:
                            if (dictionaries[result_position])[dictionary1[c]] != '':
                                CAT.append((dictionaries[result_position])[dictionary1[c]])
                        except:
                            continue

                    CAT.sort()
                    key = '_&_'.join(CAT)

                    if len(CAT)>0:

                        if key not in results.keys():#If our catalyst is not in list it will add him into the list with nfiles number of [] and will put into each [] 3 zero
                            results[key] = [[0 for j in range(3)] for i in range(nfiles)]
                        if key not in id[result_position].keys():
                            id[result_position][key] = [[] for i in range(nfiles)]

                        results[key][file_number][0] += 1
                        results[key][file_number][1] += yields
                        results[key][file_number][2] += yields**2
                        id[result_position][key][file_number].append(descr.split(';')[0])
                    if len(CAT) == 0:
                        number_of_empty_reactions[result_position] += 1
                except:
                    number_of_empty_reactions[result_position] += 1
                    continue


    out1 = open(folder_result + 'result_dictionary1.txt', 'w')
    out2 = open(folder_result + 'result_dictionary2.txt', 'w')
    out3 = open(folder_result + 'result_dictionary3.txt', 'w')

    OUT = [out1, out2, out3]

    for out_position, out in enumerate(OUT):
        max = 0

        for key in RESULTS[out_position].keys():
            if len(key)>max:
                max = len(key)

        out.write('%s %s' % (string.ljust(str(''), max), string.center('|', 1)))
        for k in range(1, nfiles+1):
            out.write(' %s  %s  %s  %s %s' % (string.rjust('Class ' + str(k), 12), string.rjust(str(reaction_number[k-1]), 5), string.rjust(str(''), 5), string.rjust(str(''), 5), string.center('|', 1)))
        out.write('\n')
        out.write('%s %s' % (string.ljust(str(''), max), string.center('|', 1)))
        for k in range(1, nfiles+1):
            out.write(' %s  %s  %s  %s %s' % (string.rjust('N', 12), string.rjust('N, %', 5), string.rjust('NYD', 5), string.rjust('s', 5), string.center('|', 1)))
        out.write('\n')
        for i in range(max+2):
            out.write('-')
        for k in range(1, nfiles+1):
            for j in range(36):
                out.write('-')
        out.write('\n')
        for key in sorted(RESULTS[out_position].keys()):
            out.write('%s %s' % (string.ljust(key, max), string.center('|', 1)))
            N_all = 0
            for k in range(nfiles):
                N_all += RESULTS[out_position][key][k][0]#Sum of all reactions for this catalyst
            for k in range(nfiles):
                if RESULTS[out_position][key][k][0]!=0:
                    NYD = round(RESULTS[out_position][key][k][1]*1.0/RESULTS[out_position][key][k][0], 2)
                    s = round((RESULTS[out_position][key][k][2]*1.0/RESULTS[out_position][key][k][0] - (RESULTS[out_position][key][k][1]*1.0/RESULTS[out_position][key][k][0])**2)**(0.5), 2)
                else:
                    NYD=0
                    s=0
                N_proc = round(RESULTS[out_position][key][k][0]*100.0/N_all, 2)
                out.write(' %s  %s  %s  %s %s' % (string.rjust(str(RESULTS[out_position][key][k][0]), 12), string.rjust(str(N_proc), 5), string.rjust(str(NYD), 5), string.rjust(str(s), 5), string.center('|', 1)))
            out.write('\n')
        for i in range(max+2):
            out.write('-')
        for k in range(1, nfiles+1):
            for j in range(36):
                out.write('-')
        out.write('\n')

        out.write('\n' + str(number_of_empty_reactions[out_position]) + ' did not have catalyst or yield.\n\n')

        if garbage==True:
            f = open(folder_garbage + '3.txt')
            ID_5 = f.readlines()
            f.close()
            length = len(ID_5)
            out.write(str(length) + ' elements are in the trash.\n\n')

        out.write('N - number of reactions\n')
        out.write('N, % - number of reactions in percent, %\n')
        out.write('NYD - mean yield of reactions in this type of transformation, %\n')
        out.write('s - dispersion of NYD, %\n\n')

        if double_comparison==False:
            out.write('Class 1 represents reactions where transformation occurs;\n')
            out.write('Class 2 represents reactions where transformation does not occur.\n')

        if double_comparison==True:
            out.write('Class 1 represents reactions where transformation1 does not occur but transformation2 occurs;\n')
            out.write('Class 2 represents reactions where transformation1 occurs and transformation2 occurs;\n')
            out.write('Class 3 represents reactions where transformation1 occurs but transformation2 does not occur;\n')
            out.write('Class 4 represents reactions where transformation1 does not occur and transformation2 does not occur.\n')

        out.write('\n')

        for i in range(1, nfiles+1):
            out.write('Class ' + str(i) +':\n')
            for key in id[out_position].keys():
                out.write("Reaction's ID for " + key + ' as catalyst:\n')
                out.write(','.join(id[out_position][key][i-1]) + '\n')

        out.write('\n')
        if garbage==True:
            out.write('ID from the trash:\n')
            out.write(''.join(ID_5))

        out.close()