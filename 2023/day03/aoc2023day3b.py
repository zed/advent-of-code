"""
https://adventofcode.com/2023/day/3#part2
"""
from functools import reduce
import aocd

# print(aocd.data)

L = """\
467..114..
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
for y in range(1, H + 1):
    for x in range(1, W + 1):
        c = a[y][x]
        if c != "*":
            continue  # not gear
        numbers = []

        def handle_number(i, j):
            left = i
            if not a[j][left].isdecimal():
                return
            while a[j][left].isdecimal():
                left -= 1
            assert not a[j][left].isdecimal()
            left += 1

            right = i
            assert a[j][right].isdecimal()
            while a[j][right].isdecimal():
                right += 1
            assert not a[j][right].isdecimal()
            numbers.append(int(a[j][left:right]))

        # left
        handle_number(x - 1, y)
        # right
        handle_number(x + 1, y)

        def horizonal(i, j):
            # possible cases: 0, 1, 2 numbers
            # 0..3 digits
            ndigits = sum(a[j][ii].isdecimal() for ii in range(i - 1, i + 2))
            if ndigits == 0:
                return  # 0 numbers
            elif ndigits == 3:  # 1 number 3+ digit number
                assert a[j][i].isdecimal()
                handle_number(i, j)
            elif ndigits == 1:  # 1 number
                for ii in range(i - 1, i + 2):
                    if a[j][ii].isdecimal():
                        handle_number(ii, j)
                        break
                else:
                    assert 0, f"can't be: must find digit in {a[j][i-1:i+2]=}"
            elif ndigits == 2:  # 1,2 numbers
                if a[j][i].isdecimal():  # 1 number 2+ digit  number
                    handle_number(i, j)
                else:  # 2 numbers
                    assert not a[j][i].isdecimal()
                    assert a[j][i - 1].isdecimal()
                    handle_number(i - 1, j)
                    assert a[j][i + 1].isdecimal()
                    handle_number(i + 1, j)
            else:
                assert 0, f"can't be: {ndigits=}"

        # below
        horizonal(x, y + 1)
        # above
        horizonal(x, y - 1)

        if len(numbers) == 2:
            # gear
            S += numbers[0] * numbers[1]


answer = S
print(S)
###aocd.submit(answer)
