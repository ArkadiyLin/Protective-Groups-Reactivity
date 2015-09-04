__author__ = 'arkadii'


def ID_finder(way1, way2, out):
    f=open(way1, 'r')
    first=f.readlines()
    f.close()

    g=open(way2, 'r')
    second=g.readlines()
    g.close()

    t=open(out, 'w')

    for i in range(len(second)):
        for j in range(len(first)):
            if first[j]==second[i]:
                t.write(first[j])
                break

    t.close()