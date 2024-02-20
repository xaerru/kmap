from ckmap import kmap

if __name__=="__main__":
    k = kmap.from_arr([[[1,0,0,0],
                        [1,2,1,0],
                        [2,2,2,0],
                        [2,2,0,0]],
                       [[1,0,0,1],
                        [1,1,2,1],
                        [1,1,2,1],
                        [1,0,0,1]],
                   ])
    sol = k.get_minimal_grouping()
    print(sol)
    k2 = kmap.from_minterm_and_dont_care([2,3,4], [5, 16]);
    sol = k2.get_minimal_grouping()
    print(sol)
