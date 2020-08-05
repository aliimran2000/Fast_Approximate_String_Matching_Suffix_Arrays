import operator
import numpy as np
import struct
from collections import defaultdict as DD


class INDEX:
    def __init__(self, char, ind):
        self.char = char
        self.ind = int(ind)
    
    def set(self, char, ind):
        self.char = char
        self.ind = ind
    
    def __repr__(self):
        string = "(" + self.char + "),(" + str(self.ind) + ")"
        return string
    
    def __str__(self):
        string = "(" + self.char + "),(" + str(self.ind) + ")"
        return string

    def Print(self):
        print(self.char," ",self.ind)

class Match:
    val = 0
    start = 0
    end = 0
    remain = 0
    leftmin = 0
    leftmax = 0
    rightmin = 0
    rightmax = 0
    pstart = 0
    pend = 0
    length = 0
    segment_id = -1

    def __repr__(self):
        string = '\n'+"start = " + str(self.start) + '\n'
        string += "end = " + str(self.end) + '\n'
        string += "length = " + str(self.length) + '\n'
        string += "remain = " + str(self.remain) + '\n'
        string += "pstart = " + str(self.pstart) + '\n'
        string += "pend = " + str(self.pend) + '\n'
        string += "leftmin = " + str(self.leftmin) + '\n'
        string += "leftmax = " + str(self.leftmax) + '\n'
        string += "rightmin = " + str(self.rightmin) + '\n'
        string += "rightmax = " + str(self.rightmax) + '\n'
        string += "segment_ID = " + str(self.segment_id) + '\n'
        string += "val = " + str(self.val) + '\n'
        
        
        
        return string

class Agenda_Item:
    M = Match
    sumlength = 0
    priority = 0

class Segment:
    id = 0
    length = 0
     

def ReadTxt(filename):
    f = open(filename,'r')
    str = f.read()
    return str

def Distance(A, B,error): 
    m = len(A)
    n = len(B)
    MEMO = np.zeros([m+1,n+1],dtype=int)
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0: 
                MEMO[i][j] = j     
            elif j == 0: 
                MEMO[i][j] = i    
            elif A[i-1] == B[j-1]: 
                MEMO[i][j] = MEMO[i-1][j-1]
            else: 
                MEMO[i][j] = 1 + min(MEMO[i][j-1],MEMO[i-1][j],MEMO[i-1][j-1])    

            
    if(MEMO[m][n] > error):
        return False

    return  True

def SortAlpha(LS,Words):
    LSI = []
    for j in LS:
        LSI.append(INDEX(' '.join(Words[j:j+12]),j))            

    LSI = sorted(LSI,key = operator.attrgetter('char'))
    
    LRET = []

    for i in LSI:
        LRET.append(i.ind)

    return LRET

def CreateSuffixArrayDD(text):
    Suffix = DD(list)
    Words = text.split(sep=' ')
    Suff_Arr = []
    
    count = 0

    for i in Words:
        if i != '':
            Suffix[i[0]].append(count)
            count+=1

    SuffA = []
    for i in sorted(Suffix):
        SuffA.extend(SortAlpha(Suffix[i],Words))

    return (SuffA,Words)


def FIND_IN_SUFFIX_no_bin_approx(SA,Words,Query,errorval = 30): 

    Q = Query.split()
    TotalError = len(Q)
    
    Results = []
    for i in SA[Query[0]]:
        value = ""
        appd = False
        itr = 0
        for j in Q:
            err = round((len(Words[i+itr])*(errorval)/(100)))
            if Distance(Words[i+itr],j,err):
                appd = True
                value += str(Words[i+itr])
                value += " "
                itr+=1
            else:
                appd = False
                break        

        if appd:
            Results.append(value+' '+str(i))

    return Results


    Q = Query.split()
    Results = []
    for i in SA[Query[0]]:
        value = ""
        #err = round((len(Words[i+itr])*(errorval)/(100)))
        if Distance(Words[i+len(Query)],Query,len(Query)*0.7):
            appd = True
            value += str(Words[i+len(Query)])
            value += " "
            Results.append(value+' '+str(i))

    return Results

def FIND_IN_SUFFIX_ARRAY(suffix_arr, words, query):
    
    lenQ = len(query.split())
        
    def BS_F(hi,bot):
        while bot < hi:
            mid = (bot + hi)//2
            
            suffix = suffix_arr[mid]
           
            if (' '.join(words[suffix:suffix+lenQ])<query):
                bot = mid + 1
            else:
                hi = mid

        return bot
    
    def BS_SEC(hi,bot):
        while bot < hi:
           
            mid = (bot + hi)//2
           
            suffix = suffix_arr[mid]
           
            if (' '.join(words[suffix:suffix+lenQ])==query):
                bot = mid + 1
            else:
                hi = mid

        return bot


    n = len(suffix_arr)
    R1 = BS_F(n,0)
    R2 = BS_SEC(n,R1)
    
    Matches = [Match]
    for i in suffix_arr[R1:R2] :
        m = Match()
        m.val = i
        m.segment_id = abs(i // 12)


        startseg = 12 * m.segment_id
        segmentS = ' '.join(words[startseg:startseg+12])
        
        m.start = len(' '.join(words[startseg:i]))       
        m.end = m.start+ len(query)
        m.start+=1
        m.end+=1
        m.length = len(query)
        
        m.remain = len(segmentS)-m.end
        
          
        if m.remain > 0 and m.segment_id != -1:
            Matches.append(m)


    return Matches

def FIND_IN_SUFFIX_ARRAY_MY_METHOD(suffix_arr, words, query):
    
    lenQ = len(query.split())
        
    def BS_F(hi,bot):
        while bot < hi:
            mid = (bot + hi)//2
            
            suffix = suffix_arr[mid]
           
            if (' '.join(words[suffix:suffix+lenQ])<query):
                bot = mid + 1
            else:
                hi = mid

        return bot
    
    def BS_SEC(hi,bot):
        while bot < hi:
           
            mid = (bot + hi)//2
           
            suffix = suffix_arr[mid]
           
            if (' '.join(words[suffix:suffix+lenQ])==query):
                bot = mid + 1
            else:
                hi = mid

        return bot


    n = len(suffix_arr)
    R1 = BS_F(n,0)
    R2 = BS_SEC(n,R1)
    
    Matches = [Match]
    for i in suffix_arr[R1:R2] :
        m = Match()
        m.val = i
        m.segment_id = abs(i // 12)
        Matches.append(m)


    return Matches


