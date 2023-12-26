"""
https://adventofcode.com/2023/day/3#part1
"""
import aocd

# print(aocd.data)

L = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".splitlines()
####L = aocd.data.splitlines()
H = len(L)
W = len(L[0])
assert all(len(row) == W for row in L)
a = schema = ["." * (W + 2)] + ["." + row + "." for row in L] + ["." * (W + 2)]
#####print(*schema, sep="\n")
# note: assume a digit is a symbol (only '.' is not a symbol)
S = 0
n = 0
for y in range(1, H + 1):
    x = 1
    while x <= W:
        c = a[y][x]
        assert not n  # not inside a number
        x0 = x
        while c.isdecimal():
            n = n * 10 + int(c)
            x += 1
            c = a[y][x]
        if n:  # found number
            # add  if there is a adjucent symbol
            if (
                any(a[y - 1][i] != "." for i in range(x0 - 1, x + 1))
                or a[y][x0 - 1] != "."
                or a[y][x] != "."
                or any(a[y + 1][i] != "." for i in range(x0 - 1, x + 1))
            ):
                S += n
            else:  # not adjucent
                pass  ### #print("not adjucent", n)
            n = 0  # reset
        x += 1
answer = S
print(S)
###aocd.submit(answer)
