import random

X = 0  # initialize X variable
weighs = 0  # initialize the # of weighings variable
S = []  # initialize S, the set of all coins
for i in range(2023):
    S.append(1)
    S.append(2)


def atLeastXGrams(k):  # weigh a set of coins and increment the # of weighings
    global weighs
    weighs += 1
    return k >= X


def runAlgo():  # algorithm
    global S
    global X

    l = 0
    r = 4046

    while (l < r):  # STEP 1: binary search
        m = (l+r)//2
        sum = 0
        for i in range(0, m+1):
            sum += S[i]
        if atLeastXGrams(sum):
            r = m
        else:
            l = m+1

    sum = 0
    for i in range(0, l+1):  # obtain the sum
        sum += S[i]

    for i in range(0, min(l+1, 2024)):  # STEP 2: combing
        if atLeastXGrams(sum - S[i]):
            return sum - S[i]

    if l+1 > 2023:  # if the size is more than 2023, we are done
        return sum

    sum -= S[0]
    for i in range(l+1, l+2024):  # STEP 3: removing the first element and testing
        if not atLeastXGrams(sum+S[i]):
            return sum + S[0]
    sum += S[0]

    if l == 0:  # if l = 0, then we necessarily must have X = sum = 2
        return sum

    sum -= S[1]
    for i in range(l+1, l+2023):  # STEP 4: removing the second element and testing
        if not atLeastXGrams(sum+S[i]):
            return sum + S[1]

    sum -= S[0]  # remove both the first and second element
    for i in range(l+1, l+2023):  # STEP 5: distinguishing between the remaining two cases
        sum += S[i]
        if atLeastXGrams(sum):
            return sum
        sum -= S[i]
    sum += S[0] + S[1]

    minimumsize = l+1
    subsetsfound = 0

    if minimumsize > 1011:  # Case 1.a
        # disregard coins at the beginning of S
        l = minimumsize - (minimumsize - (2023-minimumsize) - 1) + 1
        r = 4046
        while (l < r):  # binary search
            m = (l+r+1)//2
            sum = 0
            for i in range(m, 4046):
                sum += S[i]
            if atLeastXGrams(sum):
                l = m
            else:
                r = m-1
        sum = 0
        for i in range(l, 4046):  # obtain sum
            sum += S[i]
        for i in range(max(l, minimumsize), min(max(l, minimumsize)+2023-minimumsize, 4046)):  # combing
            if atLeastXGrams(sum - S[i]):
                return sum-S[i]
        return sum  # done

    elif minimumsize > 12:  # Case 1.b
        cursum = 0
        prevl = l  # keeps track of where we have binary searched to so far
        curl = l+minimumsize
        while True:  # begin binary searching
            l = curl
            r = 4046

            while (l < r):  # binary search forward
                m = (l+r)//2
                sum = 0
                for i in range(prevl+1, m+1):
                    sum += S[i]
                if atLeastXGrams(sum):
                    r = m
                else:
                    l = m+1
            curl = l  # update tracker

            cursum = 0
            for i in range(prevl+1, l+1):  # obtain sum
                cursum += S[i]

            if curl - prevl > minimumsize:
                for i in range(prevl+1, curl+1):  # combing
                    if atLeastXGrams(cursum - S[i]):
                        return cursum - S[i]

            subsetsfound += 1

            if curl+1-subsetsfound > 2023:  # if all two-weight coins are already searched
                l = 0  # one last binary search
                r = 4046
                while (l < r):
                    m = (l+r+1)//2
                    sum = 0
                    for i in range(m, 4046):
                        sum += S[i]
                    if atLeastXGrams(sum):
                        l = m
                    else:
                        r = m-1
                sum = 0
                for i in range(l, 4046):
                    sum += S[i]
                if atLeastXGrams(sum - S[4045]):  # test the last coin
                    return sum - S[4045]
                return sum
            prevl = curl
            curl += minimumsize

    else:  # Case 1.c
        cursum = 0
        prevl = l  # keeps track of where we iterated to so far
        curl = l+minimumsize
        r = 4046
        while True:
            cursum = 0
            for i in range(prevl+1, curl+1):  # obtain sum
                cursum += S[i]
            while not atLeastXGrams(cursum):  # iterate forward
                curl += 1
                cursum += S[curl]
            if curl - prevl > minimumsize:
                for i in range(prevl+1, curl+1):  # combing
                    if atLeastXGrams(cursum - S[i]):
                        return cursum - S[i]
                if minimumsize == 2:  # if size is 2, necessarily X = 3 and we have a set of three one-weight coins
                    return cursum

            subsetsfound += 1
            if curl+1-subsetsfound > 2023:  # if all two-weight coins are already iterated
                l = 0  # one last binary search
                r = 4046
                while (l < r):
                    m = (l+r+1)//2
                    sum = 0
                    for i in range(m, 4046):
                        sum += S[i]
                    if atLeastXGrams(sum):
                        l = m
                    else:
                        r = m-1
                sum = 0
                for i in range(l, 4046):
                    sum += S[i]
                if atLeastXGrams(sum - S[4045]):  # test the last coin
                    return sum - S[4045]
                return sum
            prevl = curl
            curl += minimumsize

while True:
    random.shuffle(S)  # randomize order of S
    for i in range(2, 6070):  # test all possible values of X
        weighs = 0
        X = i
        sum = runAlgo()  # run algorithm
        if sum != X or weighs > 10000:  # if failed, print error message
            print("TEST FAILED")
            print("X =", X)
            print("sum =", sum)
            print("S =", S)
            print("weighs =", weighs)
            exit(0)
