import copy
import math
from itertools import chain

class kmap:
    # List of 4x4 kmaps
    kmap = []
    # Number of bits required to represent kmap
    nbit = 0
    # Letters to represent output
    letters = []
    # Numbers which should output 1
    ones = set()
    # Edge list representation of graph of all 1's
    graph = []
    # Check if already visited. Used for flood_and_graph
    memo = set()
    res = []

    def __init__(self, kmap):
        self.kmap = kmap
        self.nbit = 4+math.floor(math.log(len(kmap))/math.log(2))
        self.letters = [chr(x) for x in range(64+self.nbit,64, -1)]

    def binary_to_gray(self, n):
        return n^(n>>1)

    def gray_to_binary(self, n):
        res = n
        while n > 0:
            n >>= 1
            res ^= n
        return res

    def coor_to_num(self, base, x, y):
        base *= 16
        if x%2==0:
            return base+self.binary_to_gray((x*4+y))
        else:
            return base+self.binary_to_gray(x*4+(3-y))

    def num_to_coor(self, n):
        base = 0
        if n>15:
            base = n//16
            n -= 16*base
        y = self.gray_to_binary(n)%4
        x = (self.gray_to_binary(n)-y)//4

        if x%2!=0:
            y = 3-y
        return (base,x,y)


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

    def check_and_append_edge(self, b, x, y, dx, dy):
        new_x = (x + dx) % 4
        new_y = (y + dy) % 4
        # Check if it's a 1 or a don't care
        if self.kmap[b][new_y][new_x] in [1, 2]:
            self.graph.append([self.coor_to_num(b, x, y), self.coor_to_num(b, new_x, new_y)])

    def flood_in_direction(self, b, x, y, dx, dy):
        new_x = (x + dx) % 4
        new_y = (y + dy) % 4
        self.flood_and_graph(b, new_x, new_y)

    def flood_and_graph(self, b, x, y):
        bxy_num = self.coor_to_num(b, x, y)

        if self.kmap[b][y][x]==0 or bxy_num in self.memo:
            return

        self.memo.add(bxy_num)

        if self.kmap[b][y][x]==1:
            self.ones.add(bxy_num)

        # Add adjacent nodes from other 4x4 kmaps
        for base in range(len(self.kmap)):
            if self.kmap[base][y][x] in [1,2]:
                self.graph.append([bxy_num, self.coor_to_num(base, x, y)])

        # Check if we find an adjacent 1 or a don't care in the same 4x4 kmap
        # If yes then append it to the graph
        self.check_and_append_edge(b, x, y, 1, 0)  # Right
        self.check_and_append_edge(b, x, y, 0, 1)  # Down
        self.check_and_append_edge(b, x, y, -1, 0) # Left
        self.check_and_append_edge(b, x, y, 0, -1) # Up

        # Recursively flood
        self.flood_in_direction(b, x, y, 1, 0)  # Right
        self.flood_in_direction(b, x, y, 0, 1)  # Down
        self.flood_in_direction(b, x, y, -1, 0) # Left
        self.flood_in_direction(b, x, y, 0, -1) # Up

    def check_all_ones(self, subset):
        return self.ones.issubset(set(chain.from_iterable(subset)))

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

    def get_all_floods(self):
        for b in range(len(self.kmap)):
            for x in range(4):
                for y in range(4):
                    if self.coor_to_num(b,x, y) not in self.memo:
                        self.flood_and_graph(b, x, y)
                    if self.kmap[b][y][x] in [1, 2]:
                        self.graph.append([self.coor_to_num(b,x,y)]*2)


    def make_pairs(self):
        self.get_all_floods();
        # for g in self.graph:
            # self.graph.remove([g[1],g[0]])
        # for g in self.graph:
            # if g[0]!=g[1]:
                # print(f"{g[0]}-{g[1]}")
        m = []
        ones = []
        adj_list = {}
        for g in self.graph:
            adj_list[g[0]]=set()
            adj_list[g[1]]=set()
        for g in self.graph:
            if g[0]!=g[1]:
                adj_list[g[0]].add(g[1])
        for g in self.graph:
            adj_list[g[0]]=sorted(adj_list[g[0]])

        for k,v in adj_list.items():
            # print(k,v)
            ones.append((k,))
            for n in v:
                if (n,k) not in m:
                    m.append((k, n))

        r = []
        allg = ones+m
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
                        if [t[f], t[f+h]] not in self.graph:
                            fl = False
                            break
                    h = len(t)//4
                    for f in range(h):
                        if [t[f], t[f+h]] not in self.graph:
                            fl = False
                            break
                    h = len(t)//8
                    for f in range(h):
                        # print(t[f],t[f+h], [t[f],t[f+h]] in self.graph)
                        if [t[f], t[f+h]] not in self.graph:
                            fl = False
                            break

                    h = len(t)//16
                    for f in range(h):
                        # print(t[f],t[f+h], [t[f],t[f+h]] in self.graph)
                        if [t[f], t[f+h]] not in self.graph:
                            fl = False
                            break

                    if fl:
                        r.append(tuple((lg+tuple(t))))
            prev = r
            for x in r:
                allg.append(x)
                
        self.graph = list(set(map(tuple, map(sorted, allg))))

        me = []
        for k in range(len(self.graph)):
            for gk in range(len(self.graph)):
                if gk!=k:
                    if set(self.graph[k]).issubset(set(self.graph[gk])):
                        me.append(self.graph[k])
        for m in me:
            if m in self.graph:
                self.graph.remove(m)
        print("Length of all possible groups:", len(self.graph))

        # print(len(self.graph))
        l = [0 for _ in range(len(self.graph))]
        self.check_all_combinations(copy.deepcopy(self.graph), l, 0, 0)


        minl = 100000000
        mini = 0
        for xi,x in enumerate(self.res):
            if len(x)<minl:
                mini=xi
                minl = len(x)

        for g in self.res[mini]:
            r = []
            for num in g:
                b,x,y = self.num_to_coor(num)
                r.append(self.kmap[b][y][x])
            if all(x==2 for x in r):
                self.res[mini].remove(g)

        return self.res[mini]

if __name__=="__main__":
    k = kmap([[[1,0,0,0],
               [1,2,1,0],
               [2,2,2,0],
               [2,2,0,0]],
              [[1,0,0,1],
               [1,1,2,1],
               [1,1,2,1],
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
    # When values entered default remaining to don't care
    sol = k.make_pairs()
    print(sol)
    print(k.sol_to_letter(sol))
