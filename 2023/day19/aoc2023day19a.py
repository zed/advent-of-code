#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/19#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import re
import operator as OP


def getanswer(data):
    total = 0  # sum accepted
    workflows_text, parts_text = data.split("\n\n")
    workflows = dict(map(parse_workflow, workflows_text.splitlines()))
    for part in map(parse_part, parts_text.splitlines()):
        dest = "in"  # All parts begin in the workflow named in
        while dest not in ("A", "R"):
            rules = workflows[dest]
            # The first rule that matches the part being considered is
            # applied immediately, and the part moves on to the
            # destination described by the rule. (The last rule in
            # each workflow has no condition and always applies if
            # reached.)
            dest = next(dest for rule in rules if (dest := rule(part)))
        match dest:
            case "A":
                total += sum(part.values())
            case "R":
                pass
            case _:
                assert 0, "unexpected destination"
    print(total)
    return total


def parse_part(text):
    # {x=1,m=2,a=3,s=4}
    assert text.startswith("{")
    assert text.endswith("}")
    text = text[1:-1]
    cats = {}  # categories -> value
    for ass in text.split(","):
        cat, eq, value = ass.partition("=")
        assert eq == "="
        assert cat in list("xmas")
        value = int(value)
        cats[cat] = value
    return cats


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
        dest = lambda cats: destination
    else:
        varname, opsymbol, n = re.split("([<>])", pred_text)
        n = int(n)
        match opsymbol:
            case "<":
                op = OP.lt
            case ">":
                op = OP.gt
            case _:
                assert 0, "unexpected operator"

        def dest(cats):
            return destination if op(cats[varname], n) else None

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
            19114,
        ),
        (open("input.txt").read().strip(), 330820),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()
