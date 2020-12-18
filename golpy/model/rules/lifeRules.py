# Rules for Conway's Game of Life and similar Life-like CA
# Supported format is "B/S"

from golpy.model.rules.baserule import BaseRule


class LifeRule(BaseRule):

    def __init__(self, rule_str="", neighborhood='M', mode=None, num_states=0):

        super().__init__(rule_str, neighborhood, mode, num_states)

        self.mode = "Life-like"
        self.num_states = 2

        rule_list = self.rule_str.split("/")
        if len(rule_list) > 1:
            self.birth = rule_list[0].replace('B','')
            self.survive = rule_list[1].replace('S','')
        else:
            self.birth = ""
            self.survive = ""

    def apply(self, curr_state: int, num_neighbors: int) -> int:
        str_neighbors = str(num_neighbors)
        if curr_state == 1:
            if str_neighbors in self.survive:
                return 1  # Living cells that fulfill survival-condition stay alive
        else:
            if str_neighbors in self.birth:
                return 1  # Dead cells that fulfill birthing-condition come to live

        return 0  # Otherwise the cell will be dead
