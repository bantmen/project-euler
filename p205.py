# https://projecteuler.net/problem=205
#
# Peter sum 9 x Uniform(1, 4)
# Colin sum 6 x Uniform(1, 6)
# Find probability[Peter > Colin]
#
# See https://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/Chapter7.pdf
# for convolution interpretation of the random variable summation.
#

import time

start = time.time()


def sum_uniform(low, high, num_sum):
    base_prob = {x: 1 / (high - low + 1) for x in range(low, high + 1)}
    prob = base_prob.copy()
    for _ in range(num_sum - 1):
        new_prob = {}
        for x, prob_x in prob.items():
            for y, prob_y in base_prob.items():
                new_prob[x + y] = new_prob.get(x + y, 0) + prob_x * prob_y
        prob = new_prob
    return prob


peter_prob = sum_uniform(1, 4, 9)
colin_prob = sum_uniform(1, 6, 6)

ans = 0
for x, prob_x in peter_prob.items():
    for y, prob_y in colin_prob.items():
        if x > y:
            ans += prob_x * prob_y

print("Answer:", round(ans, 7)) # 0.5731441
print("Took:", round((time.time() - start) * 1000, 3), "ms")
