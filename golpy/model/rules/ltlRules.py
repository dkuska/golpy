"""
Rule type:
Rr,Cc,Mm,Ssmin..smax,Bbmin..bmax,Nn
Here:

Rr specifies the range (r is from 1 to 500 in Golly and LifeViewer; 1 to 10 in MCell).
Cc specifies the number of states (c is from 0 to 255 in Golly, LifeViewer and MCell[note 1])
Mm specifies if the middle cell is included in the neighborhood count (m is 0 or 1).
Ssmin..smax specifies the count limits for a state 1 cell to survive.
Bbmin..bmax specifies the count limits for a dead cell to become a birth.
Nn specifies the extended neighborhood type (n is M for Moore or N for von Neumann. Golly and LifeViewer also support C for Circular neighborhood. LifeViewer additionally supports 2 for L2, + for Cross, X for Saltire and * for Star neighborhoods and many more).
"""

from model.rules.baserule import BaseRule

class LtlRule(BaseRule):

    def __init__(self):
        super().__init__()

    def apply(self, curr_state: int, num_neighbors: int) -> int:
        pass
