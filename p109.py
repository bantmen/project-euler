# https://projecteuler.net/problem=109
#
# Generates all combinations with mild pruning and then uses
# a set to deduplicate combinations - pretty inefficient.
# Faster approach: build the sums bottom up and then count
# number of moves adding up to numbers between 1-99.
#

import time

start = time.time()

all_scores = []
doubles = []
all_scores.append((0, ""))  # Miss
for i in range(1, 20 + 1):  # Singles
    all_scores.append((i, "s%s" % i))
for i in range(1, 20 + 1):  # Doubles
    all_scores.append((i * 2, "d%s" % i))
    doubles.append((i * 2, "d%s" % i))
for i in range(1, 20 + 1):  # Trebles
    all_scores.append((i * 3, "t%s" % i))
# Bulls-eye
all_scores.append((25, "s25"))
all_scores.append((50, "d25"))
doubles.append((50, "d25"))
# We need the ordering for early breaks to work.
# It is ~450ms slower without breaks.
all_scores.sort(key=lambda t: t[0])

# Used to eliminate the "same" moves
class Moves:
    def __init__(self, moves):
        self.moves = moves

    def __hash__(self):
        return hash(tuple(sorted(self.moves[:2])) + (self.moves[2],))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return str(self.moves)


ans = 0

for s in range(0, 100):
    l = []
    for n1, m1 in all_scores:
        if n1 > s:
            break
        for n2, m2 in all_scores:
            if n1 + n2 > s:
                break
            for n3, m3 in doubles:
                if n1 + n2 + n3 > s:
                    break
                if n1 + n2 + n3 == s:
                    l.append(Moves((m1, m2, m3)))
    ans += len(set(l))

print ("Answer:", ans)  # 38182
print ("Took:", round((time.time() - start) * 1000, 3), "ms")  # 1s
