import numpy

def distance(a,b):
    return DamerauLevenshteinDistance(a,b)

def DamerauLevenshteinDistance(a, b):
    al = len(a)
    bl = len(b)

    if al == 0:
        if bl == 0:
            return 0
        else:
            return bl
    elif bl == 0:
            return al
 
    score = numpy.zeros((al+2,bl+2), dtype=numpy.int)
 
    inf = al+bl
    score[0,0] = inf
    for i in xrange(al+1):
        score[i+1,0] = inf
        score[i+1,1] = i
    for j in xrange(bl+1):
        score[0,j+1] = inf
        score[1,j+1] = j
 
    sd = {}
    for c in a+b:
        sd[c] = 0
 
    for i in xrange(1,al+1):
        db = 0
        for j in xrange(1,bl+1):
            i1 = sd[b[j - 1]]
            j1 = db
 
            if a[i-1] == b[j-1]:
                score[i+1,j+1] = score[i,j]
                db = j
            else:
                score[i+1,j+1] = 1 + min(min(
                    score[i,j],
                    score[i+1,j]),
                    score[i,j+1])
 
            score[i+1,j+1] = min(score[i+1, j+1], score[i1,j1] + (i-i1-1)+ 1 +(j-j1-1))
 
        sd[a[i - 1]] = i
 
    return score[al+1,bl+1]

if __name__ == '__main__':
    print DamerauLevenshteinDistance("a","b")
    print DamerauLevenshteinDistance("ab","ba")
    print DamerauLevenshteinDistance("ab","ab")
    print DamerauLevenshteinDistance("hello","hej")
    print

