__author__ = 'arkadii'

import subprocess as sp
import fingerprint_extractor
import ensure_dir
import glob
from threading import Thread
import threading
import time
import dynamic_bond_filter
import hashlib

def sdf_parse(sdf_way, PATH):
    f = open(sdf_way)
    sdf = f.read().split('$$$$\n')[:-1]
    f.close()

    ensure_dir.ensure_dir(PATH+'/temp/')
    n=0

    for i in range(1,(len(sdf)/1000)+2):
        out = open(PATH+'/temp/' + str(i) + '.sdf', 'w')
        while n<i*1000 and n<=len(sdf)-1:
            out.write(sdf[n] + '$$$$\n')
            n+=1
        out.close()

def fingerprint_preparing(file, key):
    g = open(file + '.hdr')
    header = g.readlines()
    g.close()
    hashes = {}
    for line in header:
        p1 = int(hashlib.md5(line.rstrip('\n').strip().split(' ')[-1].strip().encode('utf8')).hexdigest(), 16) % 2048
        p2 = int(hashlib.sha1(line.rstrip('\n').strip().split(' ')[-1].strip().encode('utf8')).hexdigest(), 16) % 2048
        p_frag = line.rstrip('\n').split('.')[0].strip()
        hashes[p_frag] = [p1, p2]
    g = open(file + '.svm')
    svm = g.readlines()
    g.close()
    fingerprints = {}
    for line_position, line in enumerate(svm):
        if key=='base':
            id = line.rstrip('\n').split(' ')[0].strip()
        if key=='query':
            id = line_position+1
        fragments = [i.split(':')[0] for i in line.rstrip('\n').split()[1:] if int(i.split(':')[1])>0]
        fingerprints[id] = [str(0) for i in range(2048)]
        for frag in fragments:
            fingerprints[id][hashes[frag][0]] = str(1)
            fingerprints[id][hashes[frag][1]] = str(1)
    out = open(file + ".csv", "w")
    out.write('@ROOT:RX_ID,@fingerprint\n')
    for key_position, key in enumerate(sorted(fingerprints.keys())):
        out.write(str(key) + ',' + ''.join(fingerprints[key]))
        if key_position<len(sorted(fingerprints.keys()))-1:
            out.write('\n')
    out.close()


def script(file_name, key, PATH):
    print(file_name)
    sp.call([PATH+"/Fragmentor2015/Fragmentor", "-i", file_name, "-o", file_name[:-4], "-s", "ROOT:RX_ID","-t", "0", "-t", "3", "-l", "2", "-u", "6", "--DoAllWays"])
    fingerprint_preparing(file_name[:-4], key)
    fingerprint_extractor.fingerprint_extractor(file_name[:-4] + ".csv", file_name[:-4] + ".txt")



def ramil_scripts(output_name, key, bonds_number, PATH):#key- query or database
    '''if key=='query':
        sp.call([PATH+"/condenser", "-i", PATH+"/Query/query.mapped.rdf", "-o", PATH+"/CGR/CGR_query.sdf"])
    if key=='base':
        sp.call([PATH+"/condenser", "-i", PATH+"/MAPPED_REACTIONS/MOLS_" + output_name[7:] + ".rdf", "-o", PATH+"/CGR/CGR_temp_" + output_name + ".sdf"])
        dynamic_bond_filter.bond_filter(PATH+"/CGR/CGR_temp_" + output_name + ".sdf", PATH+"/CGR/CGR_" + output_name + ".sdf", bonds_number)
    print ("CGR has been made...")
	'''
    sdf_parse(PATH+'/CGR/CGR_' + output_name + '.sdf', PATH)
    print ('Fragger is launched...')
    files = glob.glob(PATH+'/temp/*.sdf')
    files.sort()
    tasks = []

    while files:
        if threading.active_count()<5:
            tasks.append(Thread(target=script, args=(files.pop(), key, PATH)))
            tasks[-1].start()
        else:
            time.sleep(1)

    while threading.active_count()>1:
        time.sleep(1)

    fing_files = glob.glob(PATH+'/temp/*.txt')
    fing_files.sort()
    out = open(PATH+"/FINGERPRINTS/fingerprint_" + output_name + ".txt", 'w')
    for file_position, file_name in enumerate(fing_files):
        f = open(file_name)
        fingers = f.read()
        f.close()
        out.write(fingers)
        if file_position!=len(fing_files)-1:
            out.write('\n')

    out.close()
    sp.call(["rm", "-r", PATH+"/temp/"])