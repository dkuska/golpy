import numpy as np
from golpy.model.rules.lifeRules import LifeRule


class Field:
    def __init__(self, cells=None, size=0, mode='default', neighborhood='M', rule_str="", bounded=True):
        self.size = size
        if cells is None:
            self.clear_cells()
            self.spawn_glider(1, 1)
            self.spawn_glider(40, 40)
            # self.cells = np.random.randint(2, size=(self.size, self.size))  # TODO - Change with default init
        else:
            self.cells = cells
        self.mode = mode
        self.neighborhood = neighborhood
        self.bounded = bounded
        self.rule = LifeRule(rule_str)

    def get_neighborhood(self, x_coord: int, y_coord: int):
        """ Return list of coordinate pairs which describe the neighbors of a cell with the position x_coord, y_coord"""
        neighbor_cells = []
        # TODO - Support other topologies than torus-shaped
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

        return neighbor_cells

    def neighborhood_count(self, x_coord: int, y_coord: int) -> int:
        """ Returns an Integer containing the amount of living cells in the neighborhood of a given cell """
        score = 0
        neighborhood = self.get_neighborhood(x_coord, y_coord)

        for neighbor_coord in neighborhood:
            x, y = neighbor_coord
            if self.cells[x, y] == 1:  # Only increment score if neighboring cell is alive
                score += 1

        return score

    def update(self, rule):
        """ Apply the rule to each cell to create the field for the next time step"""
        next_world = self.cells.copy()
        if self.bounded:
            for i in range(self.size):
                for j in range(self.size):
                    next_world[i][j] = self.update_cell(i, j, rule)
        self.cells = next_world.copy()

    def update_cell(self, x_coord: int, y_coord: int, rule) -> int:
        return rule.apply(self.cells[x_coord, y_coord], self.neighborhood_count(x_coord, y_coord))

    def print_cells(self):
        """ DEBUG: Prints the field to console"""
        for i in range(self.size):
            print_str = ""
            for j in range(self.size):
                print_str += str(self.cells[i, j])
            print(print_str)

    def clear_cells(self):
        self.cells = np.zeros(shape=(self.size, self.size))

    def spawn_figure(self):
        pass

    def spawn_glider(self, x_coord: int, y_coord: int):
        self.cells[x_coord, y_coord] = 1
        self.cells[x_coord + 1, y_coord + 1] = 1
        self.cells[x_coord + 2, y_coord - 1] = 1
        self.cells[x_coord + 2, y_coord] = 1
        self.cells[x_coord + 2, y_coord + 1] = 1
