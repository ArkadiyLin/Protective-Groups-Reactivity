__author__ = 'arkadii'



def parser_fingerprint(folder):
    f = open(folder + 'ID_1.txt', 'r')
    nitro = f.readlines()
    f.close()

    f = open(folder + 'ID_2.txt', 'r')
    not_nitro = f.readlines()
    f.close()

    g = open(folder + 'ID_3.txt', 'r')
    trash = g.readlines()
    g.close()

    nitro_id = []
    not_nitro_id = []
    trash_id = {}

    for i in range(len(nitro)):
        nitro_id.append(nitro[i].rstrip('\n'))

    for i in range(len(not_nitro)):
        not_nitro_id.append(not_nitro[i].rstrip('\n'))

    for i in range(len(trash)):
        trash_id[trash[i].rstrip('\n')] = 'No classes for this ID;'

    class_1 = []#Nitro
    class_2 = []#Not nitro

    for id in nitro_id:
        class_1.append(id)#Nitro

    for id in not_nitro_id:
        class_2.append(id)#Not nitro

    CLASS = [class_1, class_2]

    for i in range(len(CLASS)-1):
        for j in range(i + 1, len(CLASS)):
            list = set(CLASS[i]).intersection(set(CLASS[j]))
            if len(list) != 0:
                for id in list:
                    if id.rstrip('\n') not in trash_id.keys():
                        trash_id[id.rstrip('\n')] = str('This ID was in the classes ' + str(i+1) + ' and ' + str(j+1) + ';')
                    for number in range(len(CLASS)):
                        try:
                            CLASS[number].remove(id)
                        except:
                            continue



    out1 = open(folder + '1.txt', 'w')#Nitro
    out2 = open(folder + '2.txt', 'w')#Not nitro
    out3 = open(folder + '3.txt', 'w')#Trash ID

    out1.write(','.join(class_1))
    out2.write(','.join(class_2))
    for i, key in enumerate(trash_id.keys()):
        out3.write(key + ':' + trash_id[key])
        if i != len(trash_id)-1:
            out3.write('\n')

    out1.close()
    out2.close()
    out3.close()