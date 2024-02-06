import math
from itertools import chain
import networkx as nx

kmap = [[1,0,0,1],
        [0,1,0,0],
        [0,0,1,1],
        [0,0,1,1]]
# Take all the floods, then each subset of the flood
def binary_to_gray(n):
    n ^= (n >> 1)
    return n

def coor_to_num(x, y):
    if x%2==0:
        return binary_to_gray((x*4+y))
    else:
        return binary_to_gray(x*4+(3-y))

groups = []
memo = []
def make_groups(kmap, x, y):
    if kmap[y][x]==0 or coor_to_num(x,y) in memo:
        return
    # print(x,y)
    xy = coor_to_num(x, y)

    if x+1==len(kmap[0]):
        if kmap[y][0]==1:
            groups.append([xy ,coor_to_num(0,y)])
    else:
        if kmap[y][x+1]==1:
            groups.append([xy ,coor_to_num(x+1,y)])
    if y+1==len(kmap):
        if kmap[0][x]==1:
            groups.append([xy ,coor_to_num(x,0)])
    else:
        if kmap[y+1][x]==1:
            groups.append([xy ,coor_to_num(x,y+1)])

    if x==0:
        if kmap[y][len(kmap[0])-1]==1:
            groups.append([xy ,coor_to_num(len(kmap[0])-1,y)])
    else:
        if kmap[y][x-1]==1:
            groups.append([xy ,coor_to_num(x-1, y)])

    if y==0:
        if kmap[len(kmap)-1][x]==1:
            groups.append([xy ,coor_to_num(x, len(kmap)-1)])
    else:
        if kmap[y-1][x]==1:
            groups.append([xy ,coor_to_num(x, y-1)])

    # groups.append((x,y))
    memo.append(coor_to_num(x,y))

    if x+1==len(kmap[0]):
        make_groups(kmap, 0, y)
    else:
        make_groups(kmap, x+1, y)

    if y+1==len(kmap):
        make_groups(kmap, x, 0)
    else:
        make_groups(kmap, x, y+1)

    if x==0:
        make_groups(kmap, len(kmap[0])-1, y)
    else:
        make_groups(kmap, x-1, y)

    if y==0:
        make_groups(kmap, x, len(kmap)-1)
    else:
        make_groups(kmap, x, y-1)

make_groups(kmap, 0, 0)
for g in groups:
    print(f"{g[0]}-{g[1]}")

G=nx.DiGraph()
G.add_edges_from([(g[0], g[1]) for g in groups])

pgroups = [list(i) for i in set([tuple(sorted(x)) for x in list(nx.simple_cycles(G))])]
# for x in pgroups:
    # print(x)
def checkAllOnes(memo, b):
    smemo = list(set(sorted(memo)))
    sb = sorted(list(set(chain.from_iterable(b))))
    return sb==smemo

def isPowerOfTwo (x):
    return (x and (not(x & (x - 1))) )

res = []
def solve(a, b, ai, bi):
    if ai==len(a):
        so = []
        for x in range(bi):
            if isPowerOfTwo(len(b[x])):
                so.append(b[x])
        if checkAllOnes(memo, so):
            res.append(so)
        return

    b[bi]=a[ai]
    solve(a, b, ai+1, bi+1)
    solve(a, b, ai+1, bi)

l = [0 for _ in range(len(pgroups))]
solve(pgroups, l, 0, 0)

minl = 1000000
mini = 0
for xi,x in enumerate(res):
    if len(x)<minl:
        mini=xi
        minl = len(x)

print(res[mini])
