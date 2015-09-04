__author__ = 'arkadii'

import pickle

f = open('descriptions.csv', 'r')
descr = f.readlines()[1:]
f.close()

dict = {}
ID = [line.split(';')[0] for line in descr]

ID_unique = set(ID)
print(len(ID_unique))

for position, id in enumerate(ID):
    if id not in dict.keys():
        dict[id] = [descr[position]]
    else:
        dict[id].append(descr[position])
    if position%100==0:
        print(position)


out = open('descriptions_bin', 'wb')
pickle.dump(dict, out)
out.close()