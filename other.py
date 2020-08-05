from Utility import *
import operator
import time
import string
import numpy as np
from collections import defaultdict as DD



text = ReadTxt("test.txt")
tup = CreateSuffixArrayDD(text)

def Find_in_Suffix_Approximate(SA,Words,Query):
    Q = Query.split()

    m = len(Q)
    if(m > 2):
        m+=1


    err = round((len(Query)*(30)/(100)))

    Lisp =[]
    for i in SA[Query[0]]:
        errc = round((len(Words[i+m])*(30)/(100)))    
        if Distance(' '.join(Words[i:i+m]),Query,err+errc):
            Lisp.append(' '.join(Words[i:i+m]) + ' '+str(i))

    return Lisp    

Query = "peeple" 
print(Find_in_Suffix_Approximate(tup[0],tup[1],Query))


def Find_All_Matches(Suffa,Words,pattern):
    length = len(pattern)
    Matches = DD(list)
    ceiling_cost = (0.3 * len(pattern))
    for i in range(0,length):
            for j in range(length,i,-1) :
                search = pattern[i:j+1]
                ind = FIND_IN_SUFFIX_ARRAY(Suffa,Words,search)
                start = i
                end = j+1
                remain = len(pattern[j+1:])
                
                for M in ind:
                    if M.segment_id == -1:
                        break
                      
                    #min_cost = MatchFiltering(start,end,remain,MS)
                    M.leftmin = abs(M.start - start)
                    if M.leftmin == 0 and start > 0:
                        M.leftmin = 1
                    
                    M.rightmin = abs(M.remain - remain)
                    
                    if M.rightmin == 0 and remain > 0:
                        M.rightmin = 1
                    
                    min_cost = M.leftmin + M.rightmin
    
                    if min_cost <= ceiling_cost:                    
                        M.leftmax = max(M.start,start)
                        M.rightmax = max(M.remain,remain)
                        M.pstart = start
                        M.pend = end
                        Matches[(pattern[i:j+1])].append(M)



    return Matches
