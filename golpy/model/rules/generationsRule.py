# Another type of rule

from golpy.model.rules.baserule import BaseRule


class GenerationsRule(BaseRule):

    def __init__(self, rule_str="", neighborhood='M', mode=None, num_states=None):
        super().__init__(rule_str, neighborhood, mode, num_states)

    def apply(self, curr_state: int, num_neighbors: int) -> int:
        return 1
