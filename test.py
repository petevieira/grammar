import distance
import spell
from nlputils import *

def readparagraph(f):
    line = "\n"
    while line in ["\n", ""]:
        line = f.readline()
        if line == "":
            return []
    paragraph = []
    while not line in ["\n", ""]:
        paragraph.append(line.strip())
        line = f.readline()
    return splitSentence(" ".join(paragraph))

def compare(fn1, fn2):
    f1 = open(fn1, "r")
    f2 = open(fn2, "r")

    
    p1 = [1]
    p2 = [1]
    d = 0
    l1 = 0
    l2 = 0
    ns = 0
    while p1 != [] and p2 != []:
        p1 = readparagraph(f1)
        p2 = readparagraph(f2)

        for (s1, s2) in map(None, p1, p2):
            ns += 1
            #print s1
            #print s2
            dd = 0
            di = 0
            if s1 == None:
                dd = 1.0
                l2 += len(s2)
            elif s2 == None:
                dd = 1.0
                l1 += len(s1)
            else:
                l1 += len(s1)
                l2 += len(s2)
                dd = float(distance.distance(s1,s2))/len(s1)
                di = float(abs(len(s1) - len(s2))) / (len(s1) + len(s2))
            d += dd
            #print dd, di, l1, l2
            #print
            #if di > 0.5:
            #    return d
    return (float(d)/ns, l1, l2)

if __name__ == '__main__':
    print compare('test/gpl-3.0.txt', 'test/gplchi.txt')
    print compare('test/gpl-3.0.txt', 'test/gpl-corrected.txt')


