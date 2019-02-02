import numpy as np
import string

def check(s1,s2):
    if(checksame(s1,s2)):
        return checksame(s1,s2)
    else:
        value_som=np.zeros(len(s1))
        for i in range(0, len(s1)):
            e_d=EditDistance(s1[i],s2)
            value_som[i] = e_d
        if(np.min(value_som)<=5):
            return s1[value_som.argmin()]
        else:
            return 'invalid syntax'

def checksame(s1,s2):
    for i in range(0,len(s1)):
        wordsS1=str.split(s1[i])
        wordsS2=str.split(s2)
        if(len(wordsS2)==1 and (wordsS1[0]==wordsS2[0])):
            return s2
        elif(len(wordsS2)>=2 and len(wordsS1)>=2 and (wordsS1[0]==wordsS2[0])):
            if((wordsS1[1]==wordsS2[1])):
                return s1[i]
            else:
                return s2

def EditDistance(s1,s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def replace_type(s1,s2):
    cmd=check(s1,s2)
    cmd_comp=cmd
    words_cmd=str.split(s2)
    if(len(cmd)>4):
        b = words_cmd[4:]
        for i in b:
            cmd_comp = cmd_comp + ' ' + i
    else:
        for i in b:
            cmd_comp= cmd_comp + ' ' +i
    return cmd,cmd_comp


#correct_commands=['start','stop','next track','previous track','shuffle','volume','play','play album','play playlist']
#a,b=replace_type(correct_commands,'play ultimo')
#print(a,b)


