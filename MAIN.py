import operator
import numpy as np
import struct
import time
import collections as Col
from collections import defaultdict as DD
from Utility import *



def Find_Matches(pattern,Suffa,Words):
    PS = pattern.split()
    #length = len(PS)
    length = len(pattern)
    
    index = []
    Returner = DD(list)
    ceiling_cost = (0.3 * len(pattern))
    for i in range(0,length):
        for j in range(length,i,-1) :
            remain = length - j+1
            current = pattern[i:j+1]
            index = FIND_IN_SUFFIX_ARRAY(Suffa,Words,pattern[i:j+1])
            Matches = [Match]
            
            if(len(index) > 1):
                for m in index:
                    if m.segment_id != -1:
                        pbfor = i
                        m.leftmin = abs(m.start - pbfor)
                
                        if m.leftmin == 0 and i > 0 :
                            m.leftmin = 1

                        paftr = len(pattern[j+1:])
                        m.rightmin = abs(m.remain - paftr)
                        #m.rightmin = abs(abs(m.remain) - abs(paftr))
                        if m.rightmin == 0 and remain > 0:
                            m.rightmin = 1

                        min_cost = m.leftmin + m.rightmin
                        
                        m.pstart = i
                        m.pend = j+1
                        m.leftmax = max(m.start,pbfor)
                        m.rightmax = max (m.remain,paftr)
                        
                        if(min_cost <= ceiling_cost+1):
                            #index.remove(m)
                            Returner[pattern[i:j+1]].append(m)
                            break
                        
                #if(len(index) > 1):
                #    print(pattern[i:j+1],len(index)-1,file = filep )#,file = open("test.txt","a"))
                    
                    #for v in index:
                    #    Returner[pattern[i:j+1]].append(v)
                    #break

    return Returner            
                
def Find_Segments(pattern,Matches):
    for k in Matches.keys():
        LS = Matches[k]
        print(LS[0].pstart ,LS[0].pend,k,len(LS))
        #for all in LS:
        #    seg = all.segment_id
        #    print(' '.join(DivW[seg*12:seg*12+12]),file = filep)
        #print('--------END--------',file = filep)

def Filter_N_Gram(Matches):
    
    Copy = DD(list)
    Last = -1
    
    for all in Matches.keys():
        LS = Matches[all]
        LASTIN = LS[0].pstart
        if LASTIN != Last:
            
            for val in LS:
                Copy[all].append(val)
            
            Last = LASTIN

    return Copy

def SEGMENT_PRINT(Seg_id,F):
    S = Seg_id*12
    print(Seg_id,' : ',' '.join(DivW[S:S+12]),file = open(F,'a'))

def Find_Matches_NO_FILTER(pattern,Suffa,Words):
    PS = pattern.split()
    #length = len(PS)
    length = len(pattern)
    
    index = []
    Returner = DD(list)
    ceiling_cost = (0.3 * len(pattern))
    for i in range(0,length):
        for j in range(length,i,-1) :
            remain = length - j+1
            current = pattern[i:j+1]
            index = FIND_IN_SUFFIX_ARRAY_MY_METHOD(Suffa,Words,pattern[i:j+1])
            Matches = [Match]
            
            if(len(index) > 1):
                for m in index:
                    Returner[pattern[i:j+1]].append(m)
    return Returner            
    
def LengthFilter(Matches):

    class MYclass:
        Size = 0
        KeyValue = '-1'

        def __init__(self,K,S):
            KeyValue = (K)
            Size = S

    LSI = []
    for a in list(Matches):
        LSI.append((a))
    
    LSI = (sorted(LSI,key = len))
    
    return LSI

def Frequency_Match_Filter(Matches,selective):
    FREQ = []
    for all in selective:
        LS = Matches[all]
        for i in LS:
            a = i.segment_id
            if (a != -1):
                FREQ.append(i.segment_id)

    return FREQ

text = ReadTxt("SAMPLEMICUSP.txt")

#pattern = " if it is adequate such as quality of the weave and the display of male the manor in which birds select their nests can be identified as somewhat of a common sense approach as in placing it in an area that"

print("OUTPUT WILL BE WRITTEN TO FILE NAMED OUTPUT.txt")

filename = input("ENTER INPUT FILE")
text = ReadTxt(filename)
pattern = input("ENTER SEARCH QUERY")
#if it is adequate such as quality of the weave and the display of male the manor
tup = CreateSuffixArrayDD(text)
Suffa = tup[0]
DivW = tup[1]

filep = open("output2.txt","w")

start = time.time()

REMAINING_MATCHES = Find_Matches_NO_FILTER(pattern,Suffa,DivW)

Selected = LengthFilter(REMAINING_MATCHES)
counter=Col.Counter(Frequency_Match_Filter(REMAINING_MATCHES,Selected[len(Selected)-14:]))
L = (counter.most_common(12))

end = time.time()

print('Time :',end-start)

for i,j in L[0:]:
    SEGMENT_PRINT(i-1,"OUTPUT.txt")    
    SEGMENT_PRINT(i,"OUTPUT.txt")
    SEGMENT_PRINT(i+1,"OUTPUT.txt")
    print('---------',file = open('OUTPUT.txt','a'))


#for k in LengthFilter(REMAINING_MATCHES):
#    Frequency = DD(list)
#    for 

#Find_Segments(pattern,(REMAINING_MATCHES))




    
