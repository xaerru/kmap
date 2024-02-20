from ckmap import kmap

if __name__ == "__main__":
    print("Enter minterms: ", end="")
    m = list(map(int, input().split()))
    print("Enter don't care: ", end="")
    d = list(map(int, input().split()))

    k = kmap.from_minterm_and_dont_care(m, d)
    
    print("\nKarnaugh map:")
    for t in k.kmap:
        for tt in t:
            for ttt in tt:
                if ttt==2:
                    print('X', end=" ")
                else:
                    print(ttt, end=" ")
            print()
        print()

    sol = k.get_minimal_grouping()
    print("Minimal groups:",*sol)
    print("Minimal letter sol:", k.grouping_to_letter(sol))
