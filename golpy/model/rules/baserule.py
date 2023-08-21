# A base Class for the various kinds of 2d-rules used to update the playing field

class BaseRule:

    def __init__(self, rule_str="",  mode=None, num_states=0):
        self.rule_str = rule_str
        self.mode = mode
        self.num_states = num_states

        self.birth = []
        self.survive = []
