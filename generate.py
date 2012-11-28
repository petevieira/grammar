import random
import sys
import scorer
import math

def count(n):
    f = open('ngrams/%d-grams' % n)
    c = 0
    t = 0
    for line in f:
        fgram = line.split("\t")
        score = int(fgram[1])
        c += 1
        t += score
    return (c, t)

def generate(lastgrams, t):
    n = len(lastgrams) + 1
    f = open('ngrams/%d-grams' % n)

    target = t

    mscore = 0
    mword = ""
    found = 0
    for line in f:
        fgram = line.split("\t")
        score = int(fgram[1])
        fgram = fgram[0].split(" ")

        if fgram[0:-1] == lastgrams:
            if mscore/16 < score:
                if found == 0 or score > random.uniform(0,(mscore+score)*found):
                    mscore = score
                    mword = fgram[-1]
                found += 1

    if (mword == ""):
        print mword, mscore, lastgrams, found
        assert(0)
    #sys.stdout.flush()
    #print mword, mscore, lastgrams, found
    return mword

def perplexity(s, t):
    N = len(s)

    l = zip(map(lambda w: (w,),s), xrange(N-1))
    l.sort()
    l = scorer.getScore(l, 1)
    l.sort()

    l = map(lambda (id, g, score):
        math.log(float(score)/float(t)) * 1.0/N , l)
    return math.exp(-sum(l))


def make(l,n):
    if l == 0:
        return ""
    (c,t) = count(n)
    print "Number of %d-grams: %d with a total of %d occurences" % (n,c,t)
    s = ["^"]
    f = []
    while l > 0:
        if n > 1:
            word = generate(s[-n+1:], c)
        else:
            word = "$"
            while word == "$" or word == "^":
                word = generate([], c)

        print word,
        f.append(word)
        s.append(word)
        if word == "$":
            s = ["^"]
        else:
            l -= 1
    print
    print "Perpleixity: %s" % str(perplexity(f, t))
    return f

if __name__ == "__main__":
    make(100,1)
    make(100,2)
    make(100,3)
    make(100,4)
    make(100,5)

