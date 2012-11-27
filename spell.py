import operator
import itertools
import distance
import random
import scorer
from nlputils import *

def printf(x):
    print x

def correct(text, between=True):
    sents = splitSentence(text)
    if between:
        sents = map(lambda s: list(intersperse(s, "")), sents)
    candSents = confusionSets(sents)

    trigrams = []
    cid = 0
    for (cs, sid) in candSents:
        trigrams += trigramify(cs, (sid, cid))
        cid += 1

    #run score function
    scoredgrams = map(lambda (t0, t1, t2, ((sid, cid), wid)):
            (sid, cid, wid, t1, 1), trigrams)
    #trigrams.sort()
    #getScore(trigrams)

    scoredgrams.sort()
    #print scoredgrams

    nsentences = []
    bsid = 0
    bcid = 0
    bwid = 0
    cand = []
    candS = []
    candidates = []
    for (sid, cid, wid, t1, score) in scoredgrams + [(None,None,None,None,None)]:
        if (bcid != cid or bsid != sid) and cand != []:
            #print cand
            candidates.append( calcScore(cand) )
            cand = []
        if bsid != sid:
            candidates.sort(reverse=True)
            map(printf,candidates)
            print
            nsentences.append(candidates[0][1])
            candidates = []
        cand.append( (t1, score, wid) )
        #print sid,cid,wid, cand
        bsid = sid
        bcid = cid
        bwid = wid
    #print
    #print scoredgrams
    #print
    #print nsentences
    return " ".join(map(lambda s: " ".join(filter(lambda x: x!=""
                                                 ,s))
                       ,nsentences))

def calcScore(s):
    #print s
    assert( len(s) != 0 )
    rs = []
    score=0
    for (((d, s1), w), s2, wid) in s:
        rs.append(w)
        score += s1 + s2 + d
    return (score, rs)

def confusionSets(sentences):

    tcgrams = taggedConfusionTrigrams(sentences)
    #print tcgrams
    #print
    tcgrams.sort()

    #run candidate generator
    #tcgrams = map(lambda (t0, t1, t2, (sid, wid)):
    #        ((sid, wid), t1, random.random()), tcgrams)
    tcgrams = scorer.generate(tcgrams)
    tcgrams.sort()
    #print tcgrams
    #print

    candidates = nEmpty(len(sentences))
    for ((sid, wid), t1, score) in tcgrams:
        if len(candidates[sid]) == 0:
            candidates[sid] = nEmpty(len(sentences[sid]))
        candidates[sid][wid].append((t1, score))

    candSents = []
    sid = 0
    for (s,css) in zip(sentences, candidates):
        ncss = []
        for (word,cs) in zip(s,css):
            ncs = []
            for (candidate,score) in cs:
                dist = distance.distance(candidate, word)
                ncs.append( ((-dist*dist, score), candidate) )
            ncs.sort(reverse=True)
            #print word, ncs
            ncss.append(ncs[0:5])
            #ncss.append(ncs)
        
        candSents += map(lambda s: (s, sid), combinations2(ncss))
        sid += 1
    #print candidates
    print candSents
    candSents.sort()
    return candSents


def nEmpty(n):
    return [[] for i in xrange(n)]

def taggedConfusionTrigrams(sentences):
    o = []
    sid = 0
    for s in sentences:
        o += trigramify(s, sid)
        #o += betweens(s, sid)
        sid += 1
    return o

def combinations(ls):
    if len(ls) == 0:
        return []
    if len(ls) == 1:
        return ls[0]
    tail = combinations(ls[1:])
    return [l+" "+t for l in ls[0] for t in tail]

def combinations2(ls):
    if len(ls) == 0:
        return [[]]
    tail = combinations2(ls[1:])
    return [[l]+t for l in ls[0] for t in tail]

if __name__ == '__main__':
    #print combinations([["0","1"], ["2","3"], ["4","5"]])
    #print combinations([["0","1"], ["2","3","5"]])
    #print combinations([["0","1","3"], ["2","3","5"]])
    #print combinations([["0","1"], ["0","1"]])
    #print combinations([["0","1"], ["0","1"], ["0","1"]])
    #print combinations([[], ["0","1"]])
    #print combinations([[]])
    #print combinations([])
    #print combinations2([["0","1"], ["0","1"]])
    #print combinations2([[], ["0","1"]])
    #print combinations2([[]])
    #print combinations2([])

    ss = ["I am .", "This is a sentence .", "This is another sentence .", "Hello"]
    #print taggedConfusionTrigrams(map(words, ss))
    print correct(" ".join(ss))

