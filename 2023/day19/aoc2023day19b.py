#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/19#part2
- what is the key insight that enabled the solution?
  + return optional acc, rej tuples (cats dict + destination)
  + no need to visit the same destination twice: already restricted all the ranges
  + ranges do not intersect for different paths (by construction)
    so we can just sum the products
- what is the longest bug to fix?
- what would have made it less likely?
"""
import re
from functools import reduce
from operator import mul


def getanswer(data):
    # 1..4000
    # distinct combinations
    # in: s<1351 -> px; s>=1351 -> qqz
    #
    cats = dict(zip("xmas", (range(1, 4001),) * 4))
    workflows_text, _ = data.split("\n\n")
    workflows = dict(map(parse_workflow, workflows_text.splitlines()))
    q = [(cats, "in")]
    seen = set()
    accepted = []
    while q:
        cats, dest = q.pop()
        match dest:
            case "A":
                accepted.append(cats)
                continue
            case "R":
                continue
        if dest in seen:
            continue
        seen.add(dest)

        rules = workflows[dest]
        for rule in rules:
            acc, rej = rule(cats)
            if acc:
                q.append(acc)
            if rej:
                cats, _ = rej
                assert _ is None
            else:
                assert acc
                break
        else:  # no break
            assert 0
    answer = sum(reduce(mul, map(len, cats.values())) for cats in accepted)
    print(answer)
    return answer


def parse_workflow(text):
    # workflow = name {(rule ,)* workflow_name}
    assert text.endswith("}")
    text = text[:-1]
    name, paren, rules_text = text.partition("{")
    assert paren == "{"
    return (name, list(map(parse_rule, rules_text.split(","))))


def parse_rule(text):
    # rule = pred:destination | destination
    pred_text, colon, destination = text.rpartition(":")
    if not colon:
        dest = lambda cats: ((dict(cats), destination), None)
    else:
        varname, opsymbol, n = re.split("([<>])", pred_text)
        n = int(n)

        def dest(cats):
            r = cats[varname]
            assert r.start < r.stop
            match opsymbol:
                case "<":
                    # varname < n
                    # ...[..)...n
                    if r.stop <= n:
                        return (dict(cats), destination), None
                    # ++++n--[--)
                    if r.start >= n:
                        return None, (dict(cats), None)
                    # +++[++n--)
                    assert r.start < n
                    assert r.stop > n
                    return (
                        dict(cats, **{varname: range(r.start, n)}),
                        destination,
                    ), (dict(cats, **{varname: range(n, r.stop)}), None)
                case ">":
                    # varname > n
                    # ----[---)---n
                    if r.stop <= (n + 1):
                        #      ...   # varname <= n
                        return None, (dict(cats), None)
                    # ---n ++[+++)
                    if r.start > n:
                        return (dict(cats), destination), None
                    # --[--n ++)
                    assert r.start <= n
                    assert r.stop > (n + 1)
                    return (
                        dict(cats, **{varname: range(n + 1, r.stop)}),
                        destination,
                    ), (dict(cats, **{varname: range(r.start, n + 1)}), None)
                case _:
                    assert 0, "unexpected operator"
            assert 0

    return dest


def main():
    test_getanswer()


def test_getanswer():
    for data, expected_answer in [
        (
            """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""",
            167409079868000,
        ),
        (open("input.txt").read().strip(), 123972546935551),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()
