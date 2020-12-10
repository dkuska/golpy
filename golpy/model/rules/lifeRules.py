#Rules for Conway's Game of Life and simular Life-like CA
#Supported format is "B/S"

from golpy.model.rules.baserule import BaseRule

class LifeRule(BaseRule):

    def __init__(self, rule_str = "", mode = None, num_states = None):

        super().__init__(rule_str,mode,num_states)

        self.mode = "Life-like"
        self.num_states = 2
        self.rule_str = rule_str

        #TODO - Add check for right format in rule_str
        list = self.rule_str.split("/")
        if len(list) > 1:
            self.birth = list[0]
            self.survive = list[1]
        else:
            self.birth = ""
            self.survive = ""

    def apply(self, curr_state:int, num_neighbors: int) -> int:
        str_neighbors = str(num_neighbors)
        if curr_state == 1:
            if  str_neighbors in  self.survive:
                return 1                    #Living cells that fulfill survival-condition stay alive
        else:
            if str_neighbors in self.birth:
                return 1                    #Dead cells that fulfill birthing-condition come to live

        return 0                            #Otherwise the cell will be dead
