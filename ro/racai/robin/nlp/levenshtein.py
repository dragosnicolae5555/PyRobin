class Levenshtein:
    """
    Taken from:<br/>
    <a href="https://rosettacode.org/wiki/Levenshtein_distance#Iterative_space_optimized_.28even_bounded.29">
    https://rosettacode.org/wiki/Levenshtein_distance#Iterative_space_optimized_.28even_bounded.29</a>.</br>
    Added cache for better performance.
    """

    def __init__(self):
        self.__levenshtein_cache = {}

    def ld(self, a, b, max_n=-1):
        distance_result = self.distance(a, b, max_n)
        if max_n == -1:
            return distance_result
        else:
            return distance_result <= max_n

    def distance(self, a, b, max_n):
        keyab = a + "#" + b
        keyba = b + "#" + a

        if keyab in self.__levenshtein_cache:
            return self.__levenshtein_cache[keyab]

        if keyba in self.__levenshtein_cache:
            return self.__levenshtein_cache[keyba]

        if a == b:
            self.__levenshtein_cache[keyab] = 0
            return 0

        la = len(a)
        lb = len(b)

        if 0 <= max_n < abs(la - lb):
            self.__levenshtein_cache[keyab] = max_n + 1
            self.__levenshtein_cache[keyba] = max_n + 1
            return max_n + 1
        if la == 0:
            self.__levenshtein_cache[keyab] = lb
            self.__levenshtein_cache[keyba] = lb
            return lb
        if lb == 0:
            self.__levenshtein_cache[keyab] = la
            self.__levenshtein_cache[keyba] = la
            return la
        if la < lb:
            tl = la
            la = lb
            lb = tl
            ts = a
            a = b
            b = ts

        cost = [None] * (lb + 1)
        i = 1
        while i <= la:
            cost[0] = i
            prv = i - 1
            mindle = prv
            j = 1
            while j <= lb:
                act = prv + (0 if a[i - 1] == b[j - 1] else 1)
                prv = cost[j]
                cost[j] = min(1 + prv, 1 + cost[j - 1], act)
                if prv < mindle:
                    mindle = prv
                j += 1
            if 0 <= max_n < mindle:
                self.__levenshtein_cache[keyab] = max_n + 1
                self.__levenshtein_cache[keyba] = max_n + 1
                return max_n + 1
            i += 1

        if 0 <= max_n < cost[lb]:
            self.__levenshtein_cache[keyab] = max_n + 1
            self.__levenshtein_cache[keyba] = max_n + 1
            return max_n + 1

        self.__levenshtein_cache[keyab] = cost[lb]
        self.__levenshtein_cache[keyba] = cost[lb]
        return cost[lb]
