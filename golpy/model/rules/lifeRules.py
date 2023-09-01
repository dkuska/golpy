# Rules for Conway's Game of Life and similar Life-like CA
# Supported format is "B/S"

import numpy as np
from model.rules.baserule import BaseRule


class LifeRule(BaseRule):

    def __init__(self, rule_str="", mode=None, num_states=0):

        super().__init__(rule_str, mode, num_states)

        self.mode = "Life-like"
        self.num_states = 2

        rule_list = self.rule_str.split("/")
        if len(rule_list) > 1:
            self.birth = np.array([int(x) for x in rule_list[0].replace('B', '')])
            self.survive = np.array([int(x) for x in rule_list[1].replace('S', '')])
