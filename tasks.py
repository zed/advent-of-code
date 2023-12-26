import datetime as DT
import os
from pathlib import Path

import rich
from invoke import task, Context

solution_template = r'''#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/{day}#part{part}
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
- what utilities might have speed up similar solutions?
"""
import datetime as DT
from collections import namedtuple

import aocd
from icecream import ic
ic.configureOutput(prefix=lambda: f"{DT.datetime.now():%T}| ")

from rich.traceback import install

install(show_locals=True)

def getanswer(data):
    print(answer)
    return answer


def main():
    test_getanswer()
    aocd.submit(getanswer(aocd.data))


def test_getanswer():
    for data, expected_answer in [
        (
            """\
""",
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()
'''


def log(*args):
    rich.print(*args)


@task(positional="year")
def generate_stubs(c: Context):
    year = DT.date.today().year
    for day in range(1, 26):
        day_path = Path(f"{year}/day{day:02d}")
        if day_path.exists():
            log(day_path, "exists. Skipping")
            continue
        day_path.mkdir()
        for part, letter in zip(range(1, 3), "ab"):
            path = day_path / f"aoc{year}day{day}{letter}.py"
            path.write_text(solution_template.format_map(locals()))
            os.chmod(path, 0o755)
