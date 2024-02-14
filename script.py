from ckmap import kmap

def gray_to_binary(n):
    res = n
    while n > 0:
        n >>= 1
        res ^= n
     
    return res
def num_to_coor(n):
    b = 0
    if n>15:
        b = n//16
        n -= 16*b
    y = gray_to_binary(n)%4
    x = (gray_to_binary(n)-y)//4

    if x%2!=0:
        y = 3-y

    return (b,x,y)
def next_pow_of_2(n):
    if not (n & (n - 1)):
        return n
    return  int("1" + (len(bin(n)) - 2) * "0", 2)
if __name__ == "__main__":
    print("Enter minterms: ", end="")
    m = list(map(int, input().split()))
    print("Enter don't care: ", end="")
    d = list(map(int, input().split()))

    d = d or [-1]

    maxx = max(max(m),max(d))

    km = [[[0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0]] for x in range(next_pow_of_2(maxx//16+1))]

    for t in m:
        b,x,y = num_to_coor(t)
        km[b][y][x]=1
    for t in d:
        if t==-1:
            break
        b,x,y = num_to_coor(t)
        km[b][y][x]=2

    k = kmap(km)
    
    print("\nKarnaugh map:")
    for t in km:
        for tt in t:
            for ttt in tt:
                if ttt==2:
                    print('X', end=" ")
                else:
                    print(ttt, end=" ")
            print()
        print()

    sol = k.make_pairs()
    print("Minimal groups:",*sol)
    print("Minimal letter sol:", k.sol_to_letter(sol))
