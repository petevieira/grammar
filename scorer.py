def getGram(g):
    #print g
    (t, id) = g
    return " ".join(t)

def getScore(grams, n):
    f = open('ngrams/%d-grams' % n)
    glen = len(grams)
    if glen==0:
        return []
    gi = 0
    output = []
    for line in f:
        fgram = line.split("\t")
        score = int(fgram[1])
        fgram = fgram[0]

        #print "looking for fgram %s with score %d" % (fgram, score)

        while fgram > getGram(grams[gi]):
            #print "%s is not in file" % str(grams[gi])
            (t, id) = grams[gi]
            output.append( (id, t, -1) )
            gi += 1
            if gi == glen:
                return output

        while fgram == getGram(grams[gi]):
            #print "%s is in file" % str(grams[gi])
            (t, id) = grams[gi]
            output.append( (id, t, score) )
            gi += 1
            if gi == glen:
                return output

    while gi < glen:
        (t, id) = grams[gi]
        output.append( (id, t, -1) )
        gi += 1

    return output

def mix(gs, fs):
    if len(gs) == 0:
        return []

    output = []
    for (g0, g1, g2, id) in gs:
        gramFound = False
        for (score, (f0, f1, f2)) in fs:
            assert(f0 == g0)
            if g2 == f2:
                output.append( (id, f1, score) )
                if g1 == f1:
                    gramFound = True
        if not gramFound:
            output.append( (id, g1, -1) )
    return output

def generate(grams):
    f = open('ngrams/3-grams')
    glen = len(grams)
    if glen==0:
        return []
    gi = 0
    output = []
    l0 = []
    l1 = []
    lastfgram = ""
    for line in f:
        fgram = line.split("\t")
        score = int(fgram[1])
        fgram = fgram[0].split(" ")

        #print "looking for fgram %s with score %d" % (fgram, score)

        if lastfgram != fgram[0]:
            output += mix(l0, l1)
            l0 = []
            l1 = []
            lastfgram = fgram[0]

        l1.append( (score, fgram) )

        while fgram[0] > grams[gi][0]:
            output += mix(l0, l1)
            l0 = []
            l1 = []
            #print "%s is not in file" % str(grams[gi])
            (g0, g1, g2, id) = grams[gi]
            output.append( (id, g1, -1) )
            gi += 1
            if gi == glen:
                output += mix(l0, l1)
                return output

        while fgram[0] == grams[gi][0]:
            l0.append(grams[gi])
            #print "%s may have a candiate" % str(grams[gi])
            gi += 1
            if gi == glen:
                output += mix(l0, l1)
                return output

    while gi < glen:
        (g0, g1, g2, id) = grams[gi]
        output.append( (id, g1, -1) )
        gi += 1

    output += mix(l0, l1)
    return output

if __name__ == "__main__":
    ngrams =[("!", "!", "!", 0)
            ,("!", "!", "(", 1)
            ,("City", ",", "Mo.", 5)
            ,("City", ",", "!!!", 6)
            ,("City", ",", "New", 7)
            ,("Test", "Test", "Test!!!", 4)
            ,("{0,T}", ",", "and", 8)
            ,("{1,T}", ",", "and", 9)
            ]
    ngrams.sort()
    print sorted(getScore(ngrams))
    print sorted(generate(ngrams))


