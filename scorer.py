import operator

def getGram(g):
    #print g
    (t, id) = g
    #return " ".join(map(operator.itemgetter(1), t))
    return " ".join(t)

def getScore(grams, n):
    f = open('ngrams/%d-grams' % n)
    glen = len(grams)
    if glen==0:
        return []
    gi = 0
    output = []
    lastgram = getGram(grams[gi])
    count = 0
    total = 0
    for line in f:
        fgram = line.split("\t")
        score = int(fgram[1])
        fgram = fgram[0]
        count += 1
        total += score

        #print "looking for fgram %s with score %d" % (fgram, score)

        while fgram > lastgram:
            #print "%s is not in file" % str(grams[gi])
            (t, id) = grams[gi]
            output.append( (id, t, -1) )
            gi += 1
            if gi == glen:
                lastgram = "~~~~~"
            else:
                lastgram = getGram(grams[gi])

        while fgram == lastgram:
            #print "%s is in file" % str(grams[gi])
            (t, id) = grams[gi]
            output.append( (id, t, score) )
            gi += 1
            if gi == glen:
                lastgram = "~~~~~"
            else:
                lastgram = getGram(grams[gi])

    while gi < glen:
        (t, id) = grams[gi]
        output.append( (id, t, -1) )
        gi += 1

    return (output, count, total)

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

# takes list of lists of trigrams for each sentence ('grams')
# and generates a list of confusion words for the middle word
# in each trigram 
def generate(grams):
    # open 3-grams file created by nGrams.py from the
    # Brown corpus 
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
        fgram = line.split("\t")	# split line at the tab
        score = int(fgram[1])		# get score for 3-gram
        fgram = fgram[0].split(" ") # get 3-gram words

        #print "looking for fgram %s with score %d" % (fgram, score)
        if lastfgram != fgram[0]:
            output += mix(l0, l1)
            l0 = []
            l1 = []
            lastfgram = fgram[0]
	
		# add (score, fgram) for current trigram from 3-gram
		# file being read to the list 'l1'
        l1.append( (score, fgram) )

		# while the first word in the currnet trigram in
		# 'grams' is lexigraphically smaller than the
		# first word in the trigram from the 3-gram file
		# being read line by line
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


