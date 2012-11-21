def getGram(g):
    (t0, t1, t2, id) = g
    return " ".join([t0,t1,t2])

def getScore(grams):
    f = open('ngrams/3-grams')
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
            print "%s is not in file" % str(grams[gi])
            gi += 1
            if gi == glen:
                return output

        while fgram == getGram(grams[gi]):
            print "%s is in file" % str(grams[gi])
            (t0, t1, t2, id) = grams[gi]
            output.append( (id, t1, score) )
            gi += 1
            if gi == glen:
                return output

    return output

def getScore(grams):
    f = open('ngrams/3-grams')
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
            print "%s is not in file" % str(grams[gi])
            gi += 1
            if gi == glen:
                return output

        while fgram == getGram(grams[gi]):
            print "%s is in file" % str(grams[gi])
            (t0, t1, t2, id) = grams[gi]
            output.append( (id, t1, score) )
            gi += 1
            if gi == glen:
                return output

    return output

if __name__ == "__main__":
    scores = getScore(
            [("!", "!", "!", 0)
            ,("!", "!", "(", 1)
            ,("City", ",", "Mo.", 3)
            ,("City", ",", "New", 2)
            ,("{0,T}", ",", "and", 4)
            ,("{1,T}", ",", "and", 5)
            ])
    print scores


