# file: Goldbach.py 
#  G is a dictionary of numbers with a list of their prime sums
#    G[7] =>  7:[7,[5,2],[3,2,2]]
#
# we also have a list of the first hundred prime numbers fhp
#      fhp = [ 2, 3, 5, 7, 11, 13, ...
#
# pseudo-code
#    to get G[12]
#    extract sub-list from fhp  [2,3,5,7,11]   where max(sub_list) <= 12
#    vlist = []
#    in a loop:
#    for each prime in the sub-list:
#    subtract each prime from 12
#    12-2 = 10  -- look at G[10]   pull(10,2)
#                          extract lists, add 2
#                          5+5+2, 5+3+2+2, 3+2+3+2+2, 7+3+2, 2+2+2+2+2+2
#                          sort the lists for ease of comparison
#                          add to vlist 
#    12-3 =  9  -- look at G[ 9]   pull[3,3,3] and append 3, to get [3,3,3,3]
#    12-5 =  7  -- prime  add [5,7]
#    12-7 =  5  -- prime  duplicate of [5,7] don't add
#    12-11=  1  -- pass 
#-------------------------------------------------------------------------
#   the table we are going to create .... Ref: https://pastebin.com/6bNQRQVt
#-------------------------------------------------------------------------
#
#   N	G(N)       
#   2     1   :: 2 
#   3     1   :: 3
#   4     1   :: 2+2
#   5     2   :: 5, 3+2
#   6     2   :: 3+3,  2+2+2
#   7     3   :: 7, 5+2, 3+2+2 
#   8     3   :: 5+3, 3+3+2, 2+2+2+2
#   9     4   :: 7+2, 5+2+2, 3+3+3, 3+2+2+2
#  10     5   :: 5+5, 5+3+2, 3+2+3+2, 7+3, 2+2+2+2+2
#  11     6   :: 11,  7+2+2, 2+2+2+2+3, 5+3+3,  5+2+2+2
#  12     7   :: 5+5+2, 5+3+2+2,  3+2+3+2+2, 7+5, 7+3+2,  3+3+3+3,  2+2+2+2+2+2
#  13     9   :: 13, 11+2, 7+3+3, 5+2+2+2,  ... 
#  14    10   :: [7,7],[3,3,3,5],[3,11],[2,5,7],[2,3,3,3,3],[2,2,5,5],[2,2,3,7],[2,2,2,3,5],[2,2,2,2,2,2,2],[2,2,2,2,3,3]
#  15    12   :: 5+5+5  13+2, 11+2+2, 7+5+3,  5+2+2+2+2  ....
#  16    14   ::  ...
#  17    17   :: 17, 7+3+2+5 ...
#  18    19   ::  ...
#  19    23   ::  ...
#  20    26   ::  ...
#  21    30   :: 11+3+7
#  22    35   :: 
#  23    40   :: 23, 11+7+5 ...
#  24    46   :: 
#  25    52   :: 17+5+3
#-------------------------------------------------------------------------
#  Approach : Goldbachs conjecture .... any even integer can be expressed as sum of two prime numbers.
#   three cases:
#      1) When N is a prime number, print the number.
#      2) When (N-2) is a prime number, print 2 and N-2.
#      3) Express N as 3 + (N-3). Obviously, N-3 will be an even number 
#         (subtraction of an odd from another odd results in even). 
#         So, according to Goldbach’s conjecture, that even number can be expressed
#         as the sum of two prime numbers. So, print 3 and other two prime numbers.
#-------------------------------------------------------------------------
DIAG=True
DIAG=False

def dprint(v_s):
    if DIAG:
        print(v_s)

def isPrime(x): 
    if(x == 0 or x == 1) : 
        return False
    i = 2
    while i * i <= x :  
        if (x % i == 0) : 
            return False
        i = i + 1
    return True

def stuff(alist):
    """ sort alist, if list not already in vlist, then append alist """
    global vlist
    alist.sort()
    if alist not in vlist:
        vlist.append( alist )


def getsums(k):
    global vlist

    def getsublist(k, nbelow):
        """  k is the number we have to get below 
             nbelow is 1 or 2 below
             returns sublist of prime numbers
        """

        global fhp 
        sublist = []
        maxp = 2
        for p in fhp:
            if p < (k-nbelow):
                maxp = p
        return list(filter(lambda x: x <= maxp, fhp))

    def extractG(k, nextprime):
        """ get lists from G[k]  add  nextprime  to each list
            stuff into vlist    """
        global G
        dprint('    extractG({}, {})'.format(k,nextprime))
        n = k-nextprime
        dprint('    G[{}]={}'.format(n,G[n]))
        for item in G[n]:
            # look for items of type list
            floo   = str(type(item)).split()
            weebit = floo[1].replace("'","").replace(">","")
            if weebit == 'list':
                thing = item.copy()
                dprint('    G[{}] add {}  {}'.format(n, nextprime, item))
                thing.append(nextprime) 
                if sum(thing) == k:
                    thing.sort()
                    stuff( thing )

    #--------------------------------------------------------------------
    #   main body of getsums
    #--------------------------------------------------------------------
    maxkey = max(G.keys())
    dprint(' k={}  maxkey={}'.format(k, maxkey))
    #  Every even integer greater than 2 can be expressed as the sum of two primes.
    if k%2 == 0:
        sublist = getsublist(k,2)        # even number
    else:
        sublist = getsublist(k,1)        # odd  number

    dprint('    sublist={}'.format(sublist))
    for next_prime  in sublist:
        kn = k - next_prime
        if isPrime(kn):
            dprint('      {} = {} - {} Prime'.format(kn, k, next_prime))
            stuff( [kn, next_prime] )

        extractG(k, next_prime)


#---------------------- main ----------------------------------
global G, vlist, fhp

# first one hundred prime numbers 
fhp=[ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97 ]

G={ 2:[2], 3:[3], 4:[[2,2]], 5:[5,[2,3]], 6:[[3,3],[2,2,2]] 
,7:[7,[2,5],[2,2,3]] 
,8:[[2,3,3],[2,2,2,2],[3,5]]
,9:[[2,7],[3,3,3],[2,2,2,3],[2,2,5]]
,10:[[2,2,3,3],[2,2,2,2,2],[2,3,5],[3,7],[5,5]]
,11:[[11],[2,2,7],[2,3,3,3],[2,2,2,2,3],[2,2,2,5],[3,3,5]]
,12:[[2,2,2,3,3],[2,2,2,2,2,2],[2,2,3,5],[2,3,7],[2,5,5],[3,3,3,3],[5,7]]
,13:[[13],[2,11],[2,2,3,3,3],[2,2,2,2,2,3],[2,3,3,5],[3,3,7],[3,5,5],[2,2,2,2,5],[2,2,2,7]]
,14:[[2,2,2,2,3,3],[2,2,2,2,2,2,2],[2,2,2,3,5],[2,2,3,7],[2,2,5,5],[2,3,3,3,3],[2,5,7],[3,11],[3,3,3,5],[7,7]]
,15:[[2,13],[2,2,2,3,3,3],[2,2,2,2,2,2,3],[2,2,3,3,5],[2,3,3,7],[2,3,5,5],[3,3,3,3,3],[3,5,7],[2,2,2,2,2,5],[5,5,5],[2,2,2,2,7],[2,2,11]]
}

maxval = 50
for k in range (16,maxval+1):
    vlist=[]
    if isPrime(k):
        stuff([k])
    getsums(k)
    G[k] = vlist
    print(' {}    {} '.format(k, len(vlist) ))

#-------------  bottom of Goldbach.py -------------------------------
