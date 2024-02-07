import math
import copy
from itertools import chain
import networkx as nx

class kmap:
    kmap = []
    groups = []
    memo = set()
    res = []

    def __init__(self, kmap):
        self.kmap = kmap

    def binary_to_gray(self, n):
        n ^= (n >> 1)
        return n

    def isPowerOfTwo(self, x):
        return (x and (not(x & (x - 1))) )

    def coor_to_num(self, x, y):
        if x%2==0:
            return self.binary_to_gray((x*4+y))
        else:
            return self.binary_to_gray(x*4+(3-y))

    def make_groups(self, x, y):
        if self.kmap[y][x]==0 or self.coor_to_num(x,y) in self.memo:
            return
        xy = self.coor_to_num(x, y)

        if x+1==len(self.kmap[0]):
            if self.kmap[y][0]==1:
                self.groups.append([xy ,self.coor_to_num(0,y)])
        else:
            if self.kmap[y][x+1]==1:
                self.groups.append([xy ,self.coor_to_num(x+1,y)])
        if y+1==len(self.kmap):
            if self.kmap[0][x]==1:
                self.groups.append([xy ,self.coor_to_num(x,0)])
        else:
            if self.kmap[y+1][x]==1:
                self.groups.append([xy ,self.coor_to_num(x,y+1)])

        if x==0:
            if self.kmap[y][len(self.kmap[0])-1]==1:
                self.groups.append([xy ,self.coor_to_num(len(self.kmap[0])-1,y)])
        else:
            if self.kmap[y][x-1]==1:
                self.groups.append([xy ,self.coor_to_num(x-1, y)])

        if y==0:
            if self.kmap[len(self.kmap)-1][x]==1:
                self.groups.append([xy ,self.coor_to_num(x, len(self.kmap)-1)])
        else:
            if self.kmap[y-1][x]==1:
                self.groups.append([xy ,self.coor_to_num(x, y-1)])

        self.memo.add(self.coor_to_num(x,y))

        if x+1==len(self.kmap[0]):
            self.make_groups(0, y)
        else:
            self.make_groups(x+1, y)

        if y+1==len(self.kmap):
            self.make_groups(x, 0)
        else:
            self.make_groups(x, y+1)

        if x==0:
            self.make_groups(len(self.kmap[0])-1, y)
        else:
            self.make_groups(x-1, y)

        if y==0:
            self.make_groups(x, len(self.kmap)-1)
        else:
            self.make_groups(x, y-1)

    def check_all_ones(self, subset):
        smemo = self.memo
        sb = set(chain.from_iterable(subset))
        return sb==smemo

    def check_all_combinations(self, c, i, j):
        if j>len(self.memo):
            return
        if i==len(self.groups):
            subset = []
            for x in range(j):
                subset.append(c[x])
            if self.check_all_ones(subset):
                self.res.append(subset)
            return

        for k in range(len(self.groups)):
            for g in self.groups:
                if k>=len(self.groups):
                    k=0
                if g!=self.groups[k]:
                    if set(self.groups[k]).issubset(set(g)):
                        self.groups.remove(self.groups[k])

        c[j]=self.groups[i]
        self.check_all_combinations(c, i+1, j+1)
        self.check_all_combinations(c, i+1, j)

    def make_all_groups(self):
        for x in range(4):
            for y in range(4):
                if self.coor_to_num(x, y) not in self.memo:
                    self.make_groups(x, y)
                self.groups.append([self.coor_to_num(x,y)]*2)

    def get_minimal_groups(self):
        self.make_all_groups();

        G=nx.DiGraph()
        G.add_edges_from([(g[0], g[1]) for g in self.groups])

        m = copy.deepcopy(self.groups)

        # for g in self.groups:
            # print(f"{g[0]}-{g[1]}")
        self.groups = [list(i) for i in set([tuple(sorted(x)) for x in list(nx.simple_cycles(G)) if self.isPowerOfTwo(len(x))])]

        id = 0
        while True:
            if id==len(self.groups):
                break
            g = self.groups[id]
            if len(g)==8:
                o = []
                for i in g:
                    c = 0
                    for j in g:
                        if i!=j:
                            if [i,j] in m or [j, i] in m:
                                c+=1
                    o.append(c)
                for x in o:
                    if x<3:
                        self.groups.remove(g)
                        id-=1
                        break
            id+=1


        l = [0 for _ in range(len(self.groups))]
        self.check_all_combinations(l, 0, 0)


        # print(self.res)
        minl = 1000000
        mini = 0
        for xi,x in enumerate(self.res):
            if len(x)<minl:
                mini=xi
                minl = len(x)

        return self.res[mini]


if __name__=="__main__":
    k = kmap([[1,0,0,1],
              [1,1,0,1],
              [0,1,0,1],
              [1,1,0,1]])
    print(k.get_minimal_groups())
    # k.make_all_groups()
    # # In each flood do the following
    # for g in k.groups:
        # k.groups.remove([g[1],g[0]])
        # print(f"{g[0]}-{g[1]}")
