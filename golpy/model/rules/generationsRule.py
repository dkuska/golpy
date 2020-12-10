# A nother

from golpy.model.rules.baserule import BaseRule

class GenerationsRule(BaseRule):

    def __init__(self, rule_str = "", mode = None, num_states = None):
        super().__init__(rule_str,mode,num_states)

    def apply(self, curr_state: int, num_neighbors: int) -> int:
        return 1
