import numpy as np
import golpy.model.example_creatures as creatures


class Field:
    def __init__(self, cells=None, size=(0, 0), mode='default', neighborhood='M', bounded=True):
        self.size = size
        self.height, self.width = size
        if cells is None:
            self.clear_cells()
            #self.spawn_figure(self.height // 2, self.width // 2, creatures.rpentomino)
            self.soup_cells()  # TODO - Swap with default init
        else:
            self.cells = cells
            self.size = len(cells[0])

        self.mode = mode
        self.neighborhood = neighborhood
        self.bounded = bounded

    def get_neighborhood(self, x_coord: int, y_coord: int):
        """ Return list of coordinate pairs which describe the neighbors of a cell with the position x_coord, y_coord"""
        neighbor_cells = []

        # TODO - Support other topologies than torus-shaped
        if self.neighborhood == 'N':  # VonNeumann-Neighborhood
            neighbor_cells = [(x_coord, (y_coord - 1) % self.width),
                              (x_coord, (y_coord + 1) % self.width),
                              ((x_coord - 1) % self.height, y_coord),
                              ((x_coord + 1) % self.height, y_coord)]
        elif self.neighborhood == 'M':  # Moore-Neighborhood
            neighbor_cells = [(x_coord, (y_coord - 1) % self.width),
                              (x_coord, (y_coord + 1) % self.width),
                              ((x_coord - 1) % self.height, y_coord),
                              ((x_coord + 1) % self.height, y_coord),
                              ((x_coord - 1) % self.height, (y_coord - 1) % self.width),
                              ((x_coord - 1) % self.height, (y_coord + 1) % self.width),
                              ((x_coord + 1) % self.height, (y_coord - 1) % self.width),
                              ((x_coord + 1) % self.height, (y_coord + 1) % self.width)]
        else:
            print("Log Error, neighborhood-status undefined")
            # TODO - Logging

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
            for i in range(self.height):
                for j in range(self.width):
                    next_world[i][j] = self.update_cell(i, j, rule)
        self.cells = next_world.copy()

    def update_cell(self, x_coord: int, y_coord: int, rule) -> int:
        """ Apply rule to a single cell """
        # TODO - Refactor
        return rule.apply(self.cells[x_coord, y_coord], self.neighborhood_count(x_coord, y_coord))

    def clear_cells(self):
        """ Resets cells to zeros"""
        self.cells = np.zeros(shape=self.size)

    def soup_cells(self):
        """ Initializes the cells with random soup of 0's and 1's """
        self.cells = np.random.randint(2, size=self.size)

    def resize(self, new_width: int, new_height: int):
        """ Resize the field and copy existing cells into upper left corner"""
        old_cells = self.cells.copy()
        new_cells = np.zeros((new_height, new_width))  # TODO - Does this have to be swapped?
        i = j = 0
        for row in old_cells:
            for cell in row:
                new_cells[i, j] = cell
                j += 1
            i += 1
            j = 0
        self.cells = new_cells.copy()

    def spawn_figure(self, x_coord, y_coord, fig_data):
        """ Spawns a figure specified through an array starting at the pos specified by the coordinates"""
        # TODO - Error Handling & edge wrapping
        x_pos, y_pos = x_coord, y_coord
        for row in fig_data:
            for new_value in row:
                self.cells[x_pos, y_pos] = new_value
                x_pos += 1
            x_pos = x_coord  # Reset x_coord for next row
            y_pos += 1  # Increment
