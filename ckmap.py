import math
from itertools import chain

class kmap:
    def __init__(self, arr):
        # List of 4x4 kmaps
        self.kmap = arr
        # Letters to represent output
        self.letters = [chr(x) for x in range(64+self.nbit,64, -1)]
        # Numbers which should output 1
        self.ones = set()
        # Edge list representation of graph of all 1's
        self.graph = []
        # All possible groups of len 2,4,8,etc.
        self.all_groups = []
        # Check if already visited. Used for flood_and_graph
        self.memo = set()
        # All the groupings which cover all the ones
        self.valid_groupings = []
        # Grouping with minimum number of groups in valid_groupings
        self.minimal_group = []

    def next_pow_of_2(self, n):
        if not (n & (n - 1)):
            return n
        return  int("1" + (len(bin(n)) - 2) * "0", 2)

    @classmethod
    def from_arr(cls, arr):
        cls.nbit = 4+math.floor(math.log(len(arr))/math.log(2))
        c = cls(arr)
        return c

    @classmethod
    def from_minterm_and_dont_care(cls, minterms, dont_cares):
        max_num = max(max(minterms), max(dont_cares, default=0))
        cls.nbit = math.floor(math.log2(max_num))+1

        arr = [[[0,0,0,0],
               [0,0,0,0],
               [0,0,0,0],
               [0,0,0,0]] for x in range(math.ceil(2**(cls.nbit-4)))]

        for m in minterms:
            b,x,y = cls.num_to_coor(m)
            arr[b][y][x]=1
        for t in dont_cares:
            b,x,y = cls.num_to_coor(t)
            arr[b][y][x]=2
        return cls(arr)

    def binary_to_gray(self, n):
        return n^(n>>1)

    @classmethod
    def gray_to_binary(cls, n):
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

    @classmethod
    def num_to_coor(cls, n):
        base = 0
        if n>15:
            base = n//16
            n -= 16*base
        y = cls.gray_to_binary(n)%4
        x = (cls.gray_to_binary(n)-y)//4

        if x%2!=0:
            y = 3-y
        return (base,x,y)

    def node_to_letter(self, n):
        r = []
        for xi,x in enumerate(bin(n)[2:].zfill(self.nbit)):
            if x=="1":
                r.append(self.letters[xi])
            else:
                r.append(self.letters[xi]+"'")
        return r

    def group_to_letter(self, group):
        r = []
        for node in group:
            r.append(set(self.node_to_letter(node)))
        return ".".join(sorted(r[0].intersection(*r)))

    def grouping_to_letter(self, sol):
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

        # Add adjacent nodes from other 4x4 kmaps and the self node
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

    def check_all_combinations(self, sg, c, i, j):
        if i==len(sg):
            subset = [c[x] for x in range(j)]
            if self.check_all_ones(subset):
                self.valid_groupings.append(subset)
            return

        c[j]=sg[i]
        self.check_all_combinations(sg, c, i+1, j+1)
        self.check_all_combinations(sg, c, i+1, j)

    def graph_all_floods(self):
        for b in range(len(self.kmap)):
            for x in range(4):
                for y in range(4):
                    if self.coor_to_num(b, x, y) not in self.memo:
                        self.flood_and_graph(b, x, y)

    def edge_list_to_adj_list(self):
        adj_list = {}
        for g in self.graph:
            adj_list[g[0]]=set()
            adj_list[g[1]]=set()
        for g in self.graph:
            if g[0]!=g[1]:
                adj_list[g[0]].add(g[1])
        for g in self.graph:
            adj_list[g[0]]=sorted(adj_list[g[0]])
        return adj_list

    def check_valid_group(self, group):
        if len(set(group))!=len(group):
            return False

        m = 2
        h = len(group)//m
        while h>0:
            # # print(t[f],t[f+h], [t[f],t[f+h]] in self.graph)
            h = len(group)//m
            m*=2
            for f in range(h):
                if [group[f], group[f+h]] not in self.graph:
                    return False
        return True


    def remove_redundant_groups(self):
        me = []
        for k in range(len(self.all_groups)):
            for gk in range(len(self.all_groups)):
                if gk!=k:
                    if set(self.all_groups[k]).issubset(set(self.all_groups[gk])):
                        me.append(self.all_groups[k])
        for m in me:
            if m in self.all_groups:
                self.all_groups.remove(m)

        for g in self.all_groups:
            r = []
            for num in g:
                b,x,y = self.num_to_coor(num)
                r.append(self.kmap[b][y][x])
            if all(x==2 for x in r):
                self.all_groups.remove(g)

    def make_all_groups(self):
        # for g in self.graph:
            # self.graph.remove([g[1],g[0]])
        # for g in self.graph:
            # if g[0]!=g[1]:
                # print(f"{g[0]}-{g[1]}")
        adj_list = self.edge_list_to_adj_list()

        twos = []
        ones = []
        for node, adjs in adj_list.items():
            # print(k,v)
            ones.append((node,))
            for n in adjs:
                if (n, node) not in twos:
                    twos.append((node, n))

        cur_size_groups = []
        all_size_groups = ones+twos
        prev_size_groups = twos
        for _ in range(self.nbit):
            # r = []
            for group in prev_size_groups:
                all_adj_lists = []
                for el in group:
                    all_adj_lists.append([x for x in adj_list[el] if x not in group])

                for i in range(min(map(len, all_adj_lists))):
                    t = [all_adj_lists[j][i] for j in range(len(all_adj_lists))]
                    if self.check_valid_group(t):
                        cur_size_groups.append(group+tuple(t))

            prev_size_groups = cur_size_groups
            for group in cur_size_groups:
                all_size_groups.append(group)
                
        self.all_groups = list(set(map(tuple, map(sorted, all_size_groups))))

        self.remove_redundant_groups()

    def remove_dont_care_groups(self):
        for g in self.minimal_group:
            r = []
            for num in g:
                b,x,y = self.num_to_coor(num)
                r.append(self.kmap[b][y][x])
            if all(x==2 for x in r):
                self.minimal_group.remove(g)

    def get_minimal_grouping(self):
        self.graph_all_floods();
        self.make_all_groups()

        l = [0 for _ in range(len(self.all_groups))]
        self.check_all_combinations(self.all_groups, l, 0, 0)

        valid_groupings_len_list = list(map(len, self.valid_groupings))
        mini = valid_groupings_len_list.index(min(valid_groupings_len_list))

        self.minimal_group = self.valid_groupings[mini]

        self.remove_dont_care_groups()

        return self.minimal_group
