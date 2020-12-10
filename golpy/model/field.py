import numpy as np
from golpy.model.rules.lifeRules import LifeRule

class Field:
    def __init__(self, cells=None, size=0, mode='default', neighborhood='M', rule_str="", bounded=True, ):
        self.size = size
        if cells == None:
            self.cells = np.random.randint(2, size=(self.size, self.size))#TODO - Change with default init
        else:
            self.cells = cells
        self.mode = mode
        self.neighborhood = neighborhood
        self.bounded = bounded
        self.rule = LifeRule(rule_str)

    def neighborhood_count(self, x_coord: int, y_coord: int) -> int:  # TODO - Support other topologies than torus-shaped
        """ Returns an Integer containing the amount of living cells in the neighborhood of a given cell """
        score = 0
        neighbor_cells = []
        if self.neighborhood == 'N':  # VonNeumann-Neighborhood
            neighbor_cells = [(x_coord, (y_coord - 1) % self.size),
                              (x_coord, (y_coord + 1) % self.size),
                              ((x_coord - 1) % self.size, y_coord),
                              ((x_coord + 1) % self.size, y_coord)]

        elif self.neighborhood == 'M':  # Moore-Neighborhood
            neighbor_cells = [(x_coord, (y_coord - 1) % self.size),
                              (x_coord, (y_coord + 1) % self.size),
                              ((x_coord - 1) % self.size, y_coord),
                              ((x_coord + 1) % self.size, y_coord),
                              ((x_coord - 1) % self.size, (y_coord - 1) % self.size),
                              ((x_coord - 1) % self.size, (y_coord + 1) % self.size),
                              ((x_coord + 1) % self.size, (y_coord - 1) % self.size),
                              ((x_coord + 1) % self.size, (y_coord + 1) % self.size)]
        else:
            print("Log Error, neighborhood-status undefined")
            # TODO - Implement Error Management

        for neighbor_coord in neighbor_cells:
            x, y = neighbor_coord
            score += self.cells[x, y]   # TODO - Implement for games with more than 2 states

        return score

    def update(self):
        """ Apply the rule to each cell to create the field for the next time step"""
        next_world = self.cells.copy()
        if self.bounded:
            for i in range(self.size):
                for j in range(self.size):
                    next_world[i][j] = self.rule.apply(self.cells[i, j], self.neighborhood_count(i, j))
        self.cells = next_world.copy()

    def print_cells(self):
        """ DEBUG: Prints the field to console"""
        for i in range(self.size):
            printstr = ""
            for j in range(self.size):
                printstr += str(self.cells[i, j])
            print(printstr)
