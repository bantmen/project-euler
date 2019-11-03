# https://projecteuler.net/problem=59

import itertools

with open("p059_cipher.txt") as f:
    enc_msg = list(map(int, f.read().split(",")))

assert len(enc_msg) % 3 == 0

# Checking for "all" English words is overkill for this problem.
# Counting number of characters that are in the alphabet or looking for most
# common words (e.g. "the", "and", etc.) both work.
words = set()
with open("/usr/share/dict/words") as f:
    for line in f:
        words.add(line.rstrip())

max_word_count = float("-inf")
correct_dec_str = None
for key in itertools.product(range(97, 122 + 1), repeat=3):
    dec_msg = []
    for i in range(0, len(enc_msg), 3):
        for j in range(0, 3):
            x = enc_msg[i + j] ^ key[j]
            dec_msg.append(chr(x))

    word_count = 0
    dec_str = "".join(dec_msg)
    for word in dec_str.split(" "):
        if word in words:
            word_count += 1
    if word_count > max_word_count:
        max_word_count = word_count
        correct_dec_str = dec_str

# Roughly takes 12.5s total
print (sum(map(ord, correct_dec_str)))
