__author__ = 'arkadii'


def fingerprint_extractor(way_in, way_out):
    f = open(way_in)
    FILE = f.readlines()
    f.close()

    header = FILE[0].rstrip('\n').split(',')
    fingerprints = FILE[1:]

    out = open(way_out, 'w')

    RX_ID = 0
    fingers = 0

    for index_position, index in enumerate(header):
        if index=='@ROOT:RX_ID':
            RX_ID=index_position
        if index=='@fingerprint':
            fingers = index_position

    for line_number, line in enumerate(fingerprints):
        out.write(line.split(',')[RX_ID].rstrip('\n').lstrip(' ') + '\t' + line.split(',')[fingers].rstrip('\n').lstrip(' '))
        if line_number!=len(fingerprints)-1:
            out.write('\n')

    out.close()