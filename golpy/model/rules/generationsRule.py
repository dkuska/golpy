# Another type of rule

import numpy as np
from model.rules.baserule import BaseRule


class GenerationsRule(BaseRule):
    def __init__(self, rule_str="", mode=None, num_states=0):

        super().__init__(rule_str, mode, num_states)

        self.mode = "Generations"
        self.num_states = 2

        rule_list = self.rule_str.split("/")
        if len(rule_list) == 3:
            self.birth = np.array([int(x) for x in rule_list[0].replace('B', '')])
            self.survive = np.array([int(x) for x in rule_list[1].replace('S', '')])
            self.num_states = int(rule_list[2].replace('C', ''))
        elif len(rule_list) == 2:
            self.birth = np.array([int(x) for x in rule_list[0].replace('B', '')])
            self.survive = np.array([int(x) for x in rule_list[1].replace('S', '')])
