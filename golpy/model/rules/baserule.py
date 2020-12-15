# A base Class for the various kinds of 2d-rules used to update the playing field

class BaseRule():

    def __init__(self, rule_str = "", neighborhood = 'M', mode = None, num_states = None):
        self.rule_str = rule_str
        self.neighborhood = neighborhood
        self.mode = mode
        self.num_states = num_states

    def apply(self, curr_state: int, num_neighbors: int) -> int:
        pass
