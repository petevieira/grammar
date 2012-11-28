import nltk.corpus
import random
import spell
import distance
from nlputils import *


def getScore(n):
    text = nltk.corpus.brown.sents()
    ss = []
    wss = []
    for i in xrange(n):
        s = []
        while len(s) <= 2 or s[0][0] > 'a' or s[-1] != ".":
            s = text[int(random.uniform(0,len(text)))]
        ss.append(s)

        ws = list(s)
        w = []
        while len(w) <= 1 or "." in w:
            j = int(random.uniform(0,len(ws)-1))
            w = list(ws[j])
        k = int(random.uniform(0,len(w)))
        c = chr(int(random.uniform(ord('a'), ord('z')+1)))
        w[k] = c
        ws[j] = "".join(w)
        #print c, s[j], ws[j]
        assert(len(s[j]) == len(ws[j]))
        wss.append(ws)

    ss = unsentences(ss)
    wss = unsentences(wss)
    css = spell.correct(wss)
    ss = splitSentence(ss)
    wss = splitSentence(wss)
    css = splitSentence(css)
    dd = 0
    for (s,ws,cs) in map(None, ss, wss, css):
        print unwords(s)
        print unwords(ws)
        print unwords(cs)
        d = distance.distance(s,cs)
        print d
        print
        if d > 0:
            dd += 1
    return float(dd) / n

if __name__ == '__main__':
    print getScore(100)


