__author__ = 'arkadii'

def bond_filter(file_in, file_out, max_numb_dyn_bonds):
    f = open(file_in)
    CGR = f.read().split('$$$$\n')[:-1]
    f.close()

    g = open(file_out, 'w')

    for sdf in CGR:
        natoms=int(str(sdf.split('\n')[3][0:3]).strip())
        nbonds=int(str(sdf.split('\n')[3][3:6]).strip())
        n=1
        ndynbonds=0
        lines=sdf.split('\n')
        while n<=nbonds:
            if lines[(3+natoms+n)][8].strip()=='8':
                ndynbonds+=1
            n+=1
        if ndynbonds<=max_numb_dyn_bonds:
            g.write(sdf + '$$$$\n')

    g.close()