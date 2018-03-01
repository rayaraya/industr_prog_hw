BEGIN { print "Words counting:" }
{ A[$1] += $2 }
END { for (i in A) print i, A[i] }
