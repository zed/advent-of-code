#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/20#part2
- what is the key insight that enabled the solution?
  there are cycles in pre-feeder conjunctions
  (and the answer is lcm of their cycles)
- what is the longest bug to fix?
- what would have made it less likely?
"""
import math
import itertools
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Literal

LOW_PULSE, HIGH_PULSE = 0, 1


@dataclass
class Broadcaster:
    type = "b"

    def receive(self, source_name, pulse):
        assert source_name == "button"
        return pulse


@dataclass
class FlipFlop:
    type = "%"
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
    type = "&"
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


def getanswer(data, final_target="rx"):
    # machine turns on when a single low pulse is sent to rx
    # Reset all modules to their default states.

    # Waiting for all pulses to be fully handled after each button press,

    # what is the fewest number of button presses required to deliver a single low pulse to the module named rx?

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
            case Broadcaster.type:
                receivers["button"].append(name)
                Module = Broadcaster
            case FlipFlop.type:
                Module = FlipFlop
            case Conjunction.type:
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

    """
    count("-low -> rx")
    count("&tg -low")
    """
    [feeder] = [name for name, r in receivers.items() if final_target in r]
    assert isinstance(modules[feeder], Conjunction)
    print(feeder)
    """
    count(
      &ln -high,
      &db -high,
      &vq -high,
      &tf -high
    )
    """
    # assumption: almost always high but occasionally it is low, then repeats
    cycle_length = {name: None for name, r in receivers.items() if feeder in r}
    print(cycle_length)
    assert all(isinstance(modules[name], Conjunction) for name in cycle_length)
    """
    count(
      &bk -low,
      &tp -low,
      &pt -low,
      &vd -low
    )
    count(
      # &bk -low
      %rg -high,
      %vp -high,
      %lp -high,
      %lm -high,
      %jt -high,
      %jh -high,
      %mn -high,
    %ql -high,
    %xh -high,
    %gr -high,
    # &tp -low
    %lv -high
    %jc -high
    %km -high
    %xf -high
    %ps -high
    %bd -high,
    %dk -high,
    %gg -high,
    # &pt -low,
    %cn -high
    %dj -high
    %fl -high
    %gc -high
    %rf -high
    %sk -high
    %sd -high
    %hq -high
    %mv -high
    # &vd -low
    %vg -high
    %sj -high
    %cg -high
    %lr -high
    %gp -high
    %st -high
    %sb -high
    %rm -high
    )
    count(
    %bd -high,
    %cg -high
    %cn -high
    %dj -high
    %dk -high,
    %fl -high
    %gc -high
    %gg -high,
    %gp -high
    %gr -high,
    %hq -high
    %jc -high
    %jh -high,
    %jt -high,
    %km -high
    %lm -high,
    %lp -high,
    %lr -high
    %lv -high
    %mn -high,
    %mv -high
    %ps -high
    %ql -high,
    %rf -high
    %rg -high,
    %rm -high
    %sb -high
    %sd -high
    %sj -high
    %sk -high
    %st -high
    %vg -high
    %vp -high,
    %xf -high
    %xh -high,
    )
    count(
    -low %bd off-on
    -low %cg off-on
    -low %cn off-on
    -low %dj off-on
    -low %dk off-on
    -low %fl off-on
    -low %gc off-on
    -low %gg off-on
    -low %gp off-on
    -low %gr off-on
    -low %hq off-on
    -low %jc off-on
    -low %jh off-on
    -low %jt off-on
    -low %km off-on
    -low %lm off-on
    -low %lp off-on
    -low %lr off-on
    -low %lv off-on
    -low %mn off-on
    -low %mv off-on
    -low %ps off-on
    -low %ql off-on
    -low %rf off-on
    -low %rg off-on
    -low %rm off-on
    -low %sb off-on
    -low %sd off-on
    -low %sj off-on
    -low %sk off-on
    -low %st off-on
    -low %vg off-on
    -low %vp off-on
    -low %xf off-on
    -low %xh off-on
    )
    """
    for count in itertools.count(
        1
    ):  # button presses When you push the button,
        # a single low pulse is sent directly to the broadcaster
        # module.
        pulses_queue = deque([("button", LOW_PULSE)])
        while pulses_queue:
            source_name, pulse = pulses_queue.popleft()
            for target_name in receivers[source_name]:
                if target_name == final_target and pulse == LOW_PULSE:
                    answer = count
                    print(answer)
                    return answer  # done
                elif target_name == feeder and pulse == HIGH_PULSE:
                    # seen pre-final target but wrong value
                    if cycle_length[source_name] is None:
                        cycle_length[source_name] = count
                    if all(ns := cycle_length.values()):
                        answer = math.lcm(*ns)
                        print(answer)
                        return answer  # done

                if (target := modules.get(target_name)) and (
                    next_pulse := target.receive(source_name, pulse)
                ) is not None:
                    pulses_queue.append((target_name, next_pulse))


def main():
    assert getanswer(open("input.txt").read().strip()) == 252667369442479


if __name__ == "__main__":
    main()
