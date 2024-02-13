import copy
import math
from itertools import chain

class kmap:
    kmap = []
    groups = []
    memo = set()
    res = []
    nbit = 0
    letters = []

    def __init__(self, kmap):
        self.kmap = kmap
        self.nbit = 4+math.floor(math.log(len(kmap))/math.log(2))
        self.letters = [chr(x) for x in range(64+self.nbit,64, -1)]

    def binary_to_gray(self, n):
        n ^= (n >> 1)
        return n

    def coor_to_num(self, b, x, y):
        b *= 16
        if x%2==0:
            return b+self.binary_to_gray((x*4+y))
        else:
            return b+self.binary_to_gray(x*4+(3-y))

    def to_letter(self, n):
        r = []
        for xi,x in enumerate(bin(n)[2:].zfill(self.nbit)):
            if x=="1":
                r.append(self.letters[xi])
            else:
                r.append(self.letters[xi]+"'")
        return r

    def group_to_letter(self, group):
        r = []
        for el in group:
            r.append(set(self.to_letter(el)))
        return ".".join(sorted(r[0].intersection(*r)))

    def sol_to_letter(self, sol):
        r = []
        for g in sol:
            r.append(self.group_to_letter(g))
        return " + ".join(r)

    def make_groups(self, b, x, y):
        if self.kmap[b][y][x]==0 or self.coor_to_num(b,x,y) in self.memo:
            return
        xy = self.coor_to_num(b,x, y)

        for i in range(len(self.kmap)):
            if self.kmap[i][y][x]==1:
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
        return self.memo==set(chain.from_iterable(subset))

    def check_all_combinations(self, sg, c, i, j, f=False):
        if i==len(sg):
            if f:
                return
            subset = [c[x] for x in range(j)]
            if self.check_all_ones(subset):
                self.res.append(subset)
            return

        c[j]=sg[i]
        self.check_all_combinations(sg, c, i+1, j+1, False)
        self.check_all_combinations(sg, c, i+1, j, True)

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
        # for g in self.groups:
            # if g[0]!=g[1]:
                # print(f"{g[0]}-{g[1]}")
        m = []
        ones = []
        adj_list = {}
        for g in self.groups:
            adj_list[g[0]]=set()
            adj_list[g[1]]=set()
        for g in self.groups:
            if g[0]!=g[1]:
                adj_list[g[0]].add(g[1])
        for g in self.groups:
            adj_list[g[0]]=sorted(adj_list[g[0]])

        for k,v in adj_list.items():
            # print(k,v)
            ones.append((k,))
            for n in v:
                if (n,k) not in m:
                    m.append((k, n))

        r = []
        all = ones+m
        prev = m
        for _ in range(5):
            # r = []
            for lg in prev:
                all_adj_lists = []
                for g in lg:
                    all_adj_lists.append([x for x in adj_list[g] if x not in lg])
                p = min((map(len, all_adj_lists)))
                for i in range(p):
                    t = []
                    for j in range(len(all_adj_lists)):
                        t.append(all_adj_lists[j][i])

                    fl = True
                    if len(set(t))!=len(t):
                        fl = False
                        break
                    # print(lg,t)
                    # Generalize
                    h = len(t)//2
                    for f in range(h):
                        if [t[f], t[f+h]] not in self.groups:
                            fl = False
                            break
                    h = len(t)//4
                    for f in range(h):
                        if [t[f], t[f+h]] not in self.groups:
                            fl = False
                            break
                    h = len(t)//8
                    for f in range(h):
                        # print(t[f],t[f+h], [t[f],t[f+h]] in self.groups)
                        if [t[f], t[f+h]] not in self.groups:
                            fl = False
                            break

                    h = len(t)//16
                    for f in range(h):
                        # print(t[f],t[f+h], [t[f],t[f+h]] in self.groups)
                        if [t[f], t[f+h]] not in self.groups:
                            fl = False
                            break

                    if fl:
                        r.append(tuple((lg+tuple(t))))
            prev = r
            for x in r:
                all.append(x)
                
        self.groups = list(set(map(tuple, map(sorted, all))))

        me = []
        for k in range(len(self.groups)):
            for gk in range(len(self.groups)):
                if gk!=k:
                    if set(self.groups[k]).issubset(set(self.groups[gk])):
                        me.append(self.groups[k])
        for m in me:
            if m in self.groups:
                self.groups.remove(m)
        print(len(self.groups))

        # print(len(self.groups))
        l = [0 for _ in range(len(self.groups))]
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
               [1,0,0,1],
               [1,0,0,1],
               [1,0,0,1]],
              [[1,0,0,1],
               [1,1,0,1],
               [1,1,0,1],
               [1,0,0,1]],
              [[0,1,0,1],
               [0,1,1,1],
               [0,0,0,1],
               [0,1,1,1]],
              [[1,1,0,1],
               [0,1,1,1],
               [1,0,0,1],
               [1,0,0,1]],
              # [[0,1,1,1],
               # [0,1,1,1],
               # [0,0,0,1],
               # [0,1,1,1]],
              # [[1,1,0,1],
               # [0,1,1,1],
               # [1,0,0,1],
               # [1,0,0,1]],
              # [[1,1,0,1],
               # [0,1,0,1],
               # [1,1,1,1],
               # [1,0,1,1]],
              # [[0,1,0,1],
               # [0,0,1,1],
               # [0,0,1,1],
               # [1,0,1,1]],
              ])
    sol = k.make_pairs()
    print(k.sol_to_letter(sol))
