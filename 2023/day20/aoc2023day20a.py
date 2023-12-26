#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/20#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Literal

LOW_PULSE, HIGH_PULSE = 0, 1


@dataclass
class Broadcaster:
    def receive(self, source_name, pulse):
        assert source_name == "button"
        return pulse


@dataclass
class FlipFlop:
    state = False

    def receive(self, source_name, pulse):
        if pulse == LOW_PULSE:
            # % flip-flop off/on by low pulse
            self.state = not self.state  # flip-flop
            # sends High on "off-> on",
            #        Low on "on -> off"
            return HIGH_PULSE if self.state else LOW_PULSE


@dataclass
class Conjunction:
    states: dict[str, Literal[LOW_PULSE] | Literal[HIGH_PULSE]] = field(
        default_factory=dict
    )

    def receive(self, source_name, pulse):
        # then  first updates
        self.states[source_name] = pulse
        # send Low if all input high,
        # and High otherwise
        return (
            LOW_PULSE
            if all(p == HIGH_PULSE for p in self.states.values())
            else HIGH_PULSE
        )


def getanswer(data):
    # populate modules, receivers
    receivers = defaultdict(list)  # name -> [*module_names]
    modules = {}  # name -> Module
    for line in data.splitlines():
        module, sep, modules_text = line.partition(" -> ")
        assert sep
        type_, name = module[0], module[1:]
        assert type_ in list("b%&")
        assert name
        match type_:
            case "b":
                receivers["button"].append(name)
                Module = Broadcaster
            case "%":
                Module = FlipFlop
            case "&":
                Module = Conjunction
            case _:
                assert 0, f"unexpected {type_=}"
        downstream = modules_text.split(", ")
        assert downstream
        receivers[name] += downstream
        modules[name] = Module()

    # populate input states for conjunctions
    for target_name, conj in modules.items():
        if isinstance(conj, Conjunction):
            for source_name, targets in receivers.items():
                if target_name in targets:
                    # they initially default to remembering a low
                    # pulse for each input
                    conj.states[source_name] = LOW_PULSE
    # send
    pulse_count = [0, 0]
    for _ in range(1000):  # button presses When you push the button,
        # a single low pulse is sent directly to the broadcaster
        # module.
        pulses_queue = deque([("button", LOW_PULSE)])
        while pulses_queue:
            source_name, pulse = pulses_queue.popleft()
            for target_name in receivers[source_name]:
                pulse_count[pulse] += 1
                if (
                    target := modules.get(target_name)
                    and (next_pulse := target.receive(source_name, pulse))
                    is not None
                ):
                    pulses_queue.append((target_name, next_pulse))

    answer = pulse_count[0] * pulse_count[1]
    print(answer)
    return answer


def main():
    test_getanswer()


def test_getanswer():
    for data, expected_answer in [
        (
            """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""",
            32000000,
        ),
        (
            """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""",
            11687500,
        ),
        (open("input.txt").read().strip(), 819397964),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()
