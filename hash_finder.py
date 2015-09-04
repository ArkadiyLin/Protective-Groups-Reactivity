from collections import Counter

f=open ('output.err.rdf', 'r')
hashes=f.readlines ()
f.close()

out=open('out.txt', 'w')

a=[]
b=[]

for i in range(len(hashes)):
    if '$DTYPE !reaction_center_hash_' in hashes[i-1] and int(hashes[i-1][29])%3==0:
        a.append(hashes[i][12:])

for i in a:
    r=i.split('+')[0].rstrip(' ')
    b.append(r)

d = Counter(b)
c = set(b)

for i in c:
    if d[i]>=1:
        out.write(str(d[i]))
        out.write('\n'+i+'\n')

out.close()
