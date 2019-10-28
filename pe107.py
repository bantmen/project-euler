# https://projecteuler.net/problem=107
#
# Kruskal's algorithm
# https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
#

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import math
import time

start_time = time.time()

d = {}
for i in range(40):
    d[i] = lambda x: x if x.isdigit() else np.inf
graph = np.loadtxt('p107_network.txt', delimiter=',', converters=d)

class DisjointSet:
    """
    Disjoint-set forests - CLRS page 571.
    """

    def __init__(self):
        self.d = {}

    def make_set(self, x):
        self.d[x] = {'p': x, 'rank': 0}

    def find_set(self, x):
        if x != self.d[x]['p']:
            # Path compression heuristic
            self.d[x]['p'] = self.find_set(self.d[x]['p'])
        return self.d[x]['p']

    def union(self, x, y):
        self._link(self.find_set(x), self.find_set(y))

    def _link(self, x, y):
        # Union by rank heuristic
        if self.d[x]['rank'] > self.d[y]['rank']:
            self.d[y]['p'] = x
        else:
            self.d[x]['p'] = y
            if self.d[x]['rank'] == self.d[y]['rank']:
                self.d[y]['rank'] += 1

assert graph.shape[0] == graph.shape[1]
num_vertex = graph.shape[0]

ds = DisjointSet()

for v in range(num_vertex):
    ds.make_set(int(v))

mst = []

# TODO: Set upper triangular to zero so we don't get the same edges twice
# Why doesn't this work?
# graph[np.triu_indices(num_vertex, k=1)] = np.inf

for edge_idx in graph.flatten().argsort():
    v = int(math.floor(edge_idx / num_vertex))
    u = int(edge_idx % num_vertex)
    if graph[u, v] == np.inf:
        # Rest of the edges are inf i.e. missing
        break
    if ds.find_set(u) != ds.find_set(v):
        mst.append(graph[u, v])
        # mst_idx.append((u, v))
        ds.union(u, v)

# A = np.zeros((num_vertex, num_vertex))
# for (u, v), w in zip(mst_idx, mst):
#     A[u, v] = w
# G = nx.from_numpy_matrix(np.array(A))
# nx.draw(G, with_labels=True)
# plt.show()

graph[graph == np.inf] = 0 # so .sum() works
print('Answer: ', int(graph.sum() / 2 - sum(mst))) # 259679
print('Took:', round((time.time() - start_time) * 1000, 3), 'ms') # 4.5-5ms
