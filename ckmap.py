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

    def coor_to_num(self, b, x, y):
        b *= 16
        if x%2==0:
            return b+self.binary_to_gray((x*4+y))
        else:
            return b+self.binary_to_gray(x*4+(3-y))

    def make_groups(self, b, x, y):
        if self.kmap[b][y][x]==0 or self.coor_to_num(b,x,y) in self.memo:
            return
        xy = self.coor_to_num(b,x, y)

        for i in range(len(self.kmap)):
            self.groups.append([xy, self.coor_to_num(i, x, y)])

        if x+1==4:
            if self.kmap[b][y][0]==1:
                self.groups.append([xy ,self.coor_to_num(b,0,y)])
        else:
            if self.kmap[b][y][x+1]==1:
                self.groups.append([xy ,self.coor_to_num(b,x+1,y)])
        if y+1==4:
            if self.kmap[b][0][x]==1:
                self.groups.append([xy ,self.coor_to_num(b,x,0)])
        else:
            if self.kmap[b][y+1][x]==1:
                self.groups.append([xy ,self.coor_to_num(b,x,y+1)])

        if x==0:
            if self.kmap[b][y][3]==1:
                self.groups.append([xy ,self.coor_to_num(b,3, y)])
        else:
            if self.kmap[b][y][x-1]==1:
                self.groups.append([xy ,self.coor_to_num(b,x-1, y)])

        if y==0:
            if self.kmap[b][3][x]==1:
                self.groups.append([xy ,self.coor_to_num(b,x,3)])
        else:
            if self.kmap[b][y-1][x]==1:
                self.groups.append([xy ,self.coor_to_num(b,x, y-1)])

        self.memo.add(self.coor_to_num(b,x,y))

        if x+1==4:
            self.make_groups(b, 0, y)
        else:
            self.make_groups(b, x+1, y)

        if y+1==4:
            self.make_groups(b, x, 0)
        else:
            self.make_groups(b, x, y+1)

        if x==0:
            self.make_groups(b, 3, y)
        else:
            self.make_groups(b, x-1, y)

        if y==0:
            self.make_groups(b, x, 3)
        else:
            self.make_groups(b, x, y-1)

    def check_all_ones(self, subset):
        smemo = self.memo
        sb = set(chain.from_iterable(subset))
        return sb==smemo

    def check_all_combinations(self, sg, c, i, j):
        if i==len(sg):
            subset = []
            for x in range(j):
                subset.append(c[x])
            if self.check_all_ones(subset):
                self.res.append(subset)
            return

        me = []
        for k in range(len(sg)):
            for gk in range(len(sg)):
                if gk!=k:
                    if set(sg[k]).issubset(set(sg[gk])):
                        me.append(sg[k])
        for m in me:
            if m in sg:
                sg.remove(m)
                        

        if i>=len(sg):
            i=0
        if j>=len(sg):
            j=0

        c[j]=sg[i]
        self.check_all_combinations(sg, c, i+1, j+1)
        self.check_all_combinations(sg, c, i+1, j)

    def make_all_groups(self):
        for b in range(len(self.kmap)):
            for x in range(4):
                for y in range(4):
                    if self.coor_to_num(b,x, y) not in self.memo:
                        self.make_groups(b, x, y)
                    if self.kmap[b][y][x]==1:
                        self.groups.append([self.coor_to_num(b,x,y)]*2)


    def make_pairs(self):
        self.make_all_groups();
        # for g in self.groups:
            # self.groups.remove([g[1],g[0]])
        for g in self.groups:
            print(f"{g[0]}-{g[1]}")
        m = []
        adj_list = {}
        for g in self.groups:
            adj_list[g[0]]=set()
        for g in self.groups:
            if g[0]!=g[1]:
                adj_list[g[0]].add(g[1])

        for k,v in adj_list.items():
            print(k,v)
            for n in v:
                m.append([k, n])

        m2 = []

        for k,v in adj_list.items():
            for n in v:
                # Chose the first item 8
                for i in v:
                    if i!=n:
                        l = [x for x in m if x[0]==i and k not in x and n not in x]
                        for c in l:
                            if [n, c[1]] in self.groups:
                                m2.append([k,n,c[0],c[1]])
                

        for _m in m2:
            print(_m)
        return

    def get_minimal_groups(self):
        self.make_all_groups();

        G=nx.DiGraph()
        G.add_edges_from([(g[0], g[1]) for g in self.groups])

        m = copy.deepcopy(self.groups)

        # print(self.groups)
        for g in self.groups:
            print(f"{g[0]}-{g[1]}")
        # Need to implement custom cycle finding without needing to remove stuff
        self.groups = [list(i) for i in set([tuple(sorted(x)) for x in list(nx.simple_cycles(G)) if self.isPowerOfTwo(len(x))])]

        id = 0
        while id!=len(self.groups):
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
            if len(g)==16:
                o = []
                for i in g:
                    c = 0
                    for j in g:
                        if i!=j:
                            if [i,j] in m or [j, i] in m:
                                c+=1
                    o.append(c)
                for x in o:
                    if x<4:
                        self.groups.remove(g)
                        id-=1
                        break
            if len(g)==32:
                o = []
                for i in g:
                    c = 0
                    for j in g:
                        if i!=j:
                            if [i,j] in m or [j, i] in m:
                                c+=1
                    o.append(c)
                for x in o:
                    if x<5:
                        self.groups.remove(g)
                        id-=1
                        break
            id+=1


        l = [0 for _ in range(len(self.groups))]
        # print(len(self.groups))
        self.check_all_combinations(copy.deepcopy(self.groups), l, 0, 0)


        minl = 100000000
        mini = 0
        for xi,x in enumerate(self.res):
            if len(x)<minl:
                mini=xi
                minl = len(x)

        return self.res[mini]


if __name__=="__main__":
    k = kmap([[[1,0,0,1],
               [1,1,0,1],
               [1,0,1,1],
               [1,0,0,1]],

              # [[1,1,0,1],
               # [1,1,1,1],
               # [1,0,1,1],
               # [1,0,1,1]],
              ])
    print(k.get_minimal_groups())
    # k.make_all_groups()
    # # In each flood do the following
    # for g in k.groups:
        # k.groups.remove([g[1],g[0]])
        # print(f"{g[0]}-{g[1]}")
