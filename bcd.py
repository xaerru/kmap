from ckmap import kmap

class bcd_circuit:
    def __init__(self):
        pass

    @classmethod
    def from_int(cls, lhs_arr, rhs_arr):
        cls.lhs = list(map(lambda x:bin(x)[2:], lhs_arr))
        cls.longest_lhs = max(map(len, cls.lhs))
        cls.lhs = list(map(lambda x:x.zfill(cls.longest_lhs), cls.lhs))

        cls.rhs = list(map(lambda x:bin(x)[2:], rhs_arr))
        cls.longest_rhs = max(map(len, cls.rhs))
        cls.rhs = list(map(lambda x:x.zfill(cls.longest_rhs), cls.rhs))
        return cls()

    @classmethod
    def from_string(cls, lhs_string, rhs_string):
        cls.lhs = lhs_string
        cls.rhs = rhs_string
        return cls()


    def solve(self):
        for l,r in zip(self.lhs, self.rhs):
            print(f"{l} -> {r}")
        print()
        for id in range(len(self.rhs[0])):
            ones = []
            for numi, num in enumerate(self.rhs):
                kmap_num = int(self.lhs[numi], 2)
                if num[id]=="1":
                    ones.append(kmap_num)
            dont_cares = [x for x in range(2**self.longest_lhs) if bin(x)[2:].zfill(self.longest_lhs) not in self.lhs]
            k = kmap.from_minterm_and_dont_care(ones, dont_cares)
            print(f"Y{len(self.rhs[0])-id-1}: ", end="")
            print(k.grouping_to_letter(k.get_minimal_grouping()))


if __name__ == "__main__":
    print("A is LSB, Y0 is output LSB.")
    # 8421
    eft1 = list(range(10))
    # 2421
    tft1 = [0, 1, 2, 3, 4, 11, 12, 13, 14, 15]
    # 4221
    ftt1 = [0, 1, 2, 3, 6, 9, 10, 11, 14, 15]
    # Excess 3
    excess3 = [x+3 for x in range(10)]
    # Excess 6
    excess6 = [x+6 for x in range(10)]
    # 53211
    ftht11_string = [
        "00000",
        "00001",
        "00011",
        "00110",
        "00111",
        "01100",
        "01101",
        "10100",
        "11000",
        "11001",
    ]
    ftht11 = list(map(lambda x:int(x,2), ftht11_string))
    # Johnson's code
    johnson_string = [
        "00000",
        "00001",
        "00011",
        "00111",
        "01111",
        "11111",
        "11110",
        "11100",
        "11000",
        "10000",
    ]
    johnson = list(map(lambda x:int(x,2), johnson_string))

    print("8421 to excess6:")
    bc = bcd_circuit.from_int(eft1, excess6)
    bc.solve()
    print()

    print("excess3 to excess6:")
    bc = bcd_circuit.from_int(excess3, excess6)
    bc.solve()
    print()

    print("8421 to 2421:")
    bc = bcd_circuit.from_int(eft1, tft1)
    bc.solve()
    print()

    print("8421 to 53211:")
    bc = bcd_circuit.from_int(eft1, ftht11)
    bc.solve()
    print()

    print("53211 to 8421:")
    bc = bcd_circuit.from_int(ftht11, eft1)
    bc.solve()
    print()

    print("8421 to Johnson's code:")
    bc = bcd_circuit.from_int(eft1, johnson)
    bc.solve()
    print()

    print("Johnson's code to 8421")
    bc = bcd_circuit.from_int(johnson, eft1)
    bc.solve()
