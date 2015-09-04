__author__ = 'arkadii'

def mols_finder(ID_input, rdf_input, out):
    f=open(ID_input, 'r')
    ID=f.readlines()
    f.close()

    g=open(rdf_input, 'r')
    lines=g.read()
    mols=lines.split('$RFMT')[1:]
    g.close()

    dict = {}

    for j in mols:
        dict['$RFMT'+j.split('\n')[0]] = j

    out1=open(out, 'w')
    out1.write('$RDFILE 1\n$DATM 2012-10-16 06:03:34\n')

    for i in range(len(ID)):
        out1.write('$RFMT' + dict[ID[i].rstrip('\n')])
        if i%1000 == 0:
            print (str(i) + ' reactions...')

    out1.close()