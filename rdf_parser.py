__author__ = 'arkadii'

import glob


def rdf_parser(input_rdfs_way, output_rdfs_way, output_csv_way):
    files = glob.glob(input_rdfs_way)

    g = open(output_csv_way, 'w')
    g.write('RX_ID;'+'COND_ID;'+'CL;'+'LB;'+'T;'+'P;'+'TIM;'+'STP;'+'RGT;'+'CAT;'+'SOL;'+'YD;'+'NYD;'+'LCN;'+'YPRO;'+'CIT;'+'TXT\n')
    molnumber=0
    descrnumber=0

    for filename in files:
        print("Parsing file", filename)
        f = open(filename)
        lines=f.readlines()
        f.close()

        f = open(output_rdfs_way + filename.split('/')[-1][:-4] + '.mols.rdf', 'w')

        f.write(lines[0]+lines[1])

        q=0
        q1=0
        n=0
        molinit=0
        molinit2=0
        nvar1=1
        m1=0
        n1=0
        ID=0
        CL=''
        LB=''
        T=''
        P=''
        TIM=''
        STP=''
        RGT=''
        CAT=''
        SOL=''
        YD=''
        NYD=''
        LCN=''
        YPRO=''
        CIT=''
        TXT=''


        for r in range(len(lines)):#Here we take molecules to the .mols.rdf
            if q==1:
                m+=1
                if m==4:
                    molinit=int(lines[r][:4].lstrip(' '))
                    molinit2=int(lines[r][4:7].lstrip(' '))
                if 'M  END' in lines[r]:
                    n+=1
                if n<=(molinit+molinit2):
                    f.write(lines[r])
                    if n==(molinit+molinit2) and n!=0:
                        q=0
                        n=0
            if '$RFMT' in lines[r-1]:
                q=1
                m=0
                f.write(lines[r-1])
                f.write(lines[r])
                nvar1=1
                molnumber+=1

            stroka='$DTYPE ROOT:RXD('+str(nvar1)+'):'

            if '$DTYPE ROOT:RX_ID' in lines[r]:
                q=2
                n+=1

            if '$DTYPE ROOT:RX_ID' in lines[r-1]:
                ID=int(lines[r][7:])

            if '$DTYPE ROOT:RX_NVAR' in lines[r]:
                q=2
                n+=1

            if q==2:
                f.write(lines[r])
                if n==2:
                    q=0
                    n=0
                if n==1:
                    n+=1

            if q1==3 or q1==4:
                if '$DTYPE ROOT:' in lines[r] or '$RFMT' in lines[r]:
                    q1=0
                if '$DTYPE ROOT:' not in lines[r]:
                    if q1==3:
                        CIT=CIT.strip()+lines[r].strip()
                    if q1==4:
                        TXT=TXT.strip()+lines[r].strip()

            if stroka in lines[r-1]:
                if m1==0:
                    COND_ID=nvar1
                    descrnumber+=1
                    m1+=1
                if '):CL' in lines[r-1]:
                    CL='"'+lines[r][7:].strip().replace(';', ',')+'"'
                if '):LB' in lines[r-1]:
                    LB='"'+lines[r][7:].strip().replace(';', ',')+'"'
                if '):T\r' in lines[r-1]:
                    T=lines[r][7:].strip().replace(';', ',')
                if '):P\r' in lines[r-1]:
                    P=lines[r][7:].strip().replace(';', ',')
                if '):TIM' in lines[r-1]:
                    TIM=lines[r][7:].strip().replace(';', ',')
                if '):STP' in lines[r-1]:
                    STP=lines[r][7:].strip().replace(';', ',')
                if '):RGT' in lines[r-1]:
                    RGT='"'+lines[r][7:].strip().replace(';', ',')+'"'
                if '):CAT' in lines[r-1]:
                    CAT='"'+lines[r][7:].strip().replace(';', ',')+'"'
                if '):SOL' in lines[r-1]:
                    SOL='"'+lines[r][7:].strip().replace(';', ',')+'"'
                if '):YD' in lines[r-1]:
                    YD='"'+lines[r].split(' ')[-1].strip().replace(';', ',')+'"'
                if '):NYD' in lines[r-1]:
                    NYD=lines[r][7:].strip()
                if '):LCN' in lines[r-1]:
                    LCN='"'+lines[r][7:].strip().replace(';', ',')+'"'
                if '):YPRO' in lines[r-1]:
                    YPRO='"'+lines[r][7:].strip().replace(';', ',')+'"'
                if '):citation' in lines[r-1]:
                    CIT=lines[r][7:].strip()
                    q1=3
                if '):TXT' in lines[r-1]:
                    TXT=lines[r][7:].strip()
                    q1=4

            if ('$DTYPE ROOT:RXD(' in lines[r] and stroka not in lines[r]) or r==(len(lines)-1) or ('$RFMT $RIREG' in lines[r] and r>3):
                TXT = TXT.replace('"', '')
                CIT = CIT.replace('"', '')
                CIT='"'+CIT.strip()+'"'
                TXT='"'+TXT.strip()+'"'
                TXT = TXT.replace(';', ',')
                CIT = CIT.replace(';', ',')
                g.write(str(ID)+';'+str(COND_ID)+';'+CL.strip()+';'+LB.strip()+';'+T.strip()+';'+P.strip()+';'+TIM.strip()+';'+STP.strip()+';'+RGT.strip()+';'+CAT.strip()+';'+SOL.strip()+';'+YD.strip()+';'+NYD.strip()+';'+LCN.strip()+';'+YPRO.strip()+';'+CIT.strip()+';'+TXT.strip()+'\n')
                CL=''
                LB=''
                T=''
                P=''
                TIM=''
                STP=''
                RGT=''
                CAT=''
                SOL=''
                YD=''
                NYD=''
                LCN=''
                YPRO=''
                CIT=''
                TXT=''
                nvar1+=1
                m1=0

        f.close()

    g.close()
    print (str(molnumber) + ' transformations are in files\n')
    print (str(descrnumber) + ' reactions are in files\n')