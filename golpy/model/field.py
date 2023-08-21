from loguru import logger
import numpy as np
import torch
import torch.nn.functional as F

import model.rules as rules

class Field:
    def __init__(self, cells=None, size=(0, 0), mode='default', neighborhood='M', bounded=True):
        self.size = size
        self.height, self.width = size
        if cells is None:
            self.clear()
            self.soup()  # TODO - Swap with default init
        else:
            self.cells = cells
            self.size = len(cells[0])

        self.mode = mode
        self.neighborhood = neighborhood
        self.neighborhood_kernel = self.get_neighborhood
        self.bounded = bounded

    def get_neighborhood(self):
        """ Return list of coordinate pairs which describe the neighbors of a cell with the position x_coord, y_coord"""
        # TODO - Support other topologies than torus-shaped
        if self.neighborhood == 'N':  # VonNeumann-Neighborhood
            neighborhood = np.array(
                [[0, 1, 0],
                [1, 0, 1],
                [0, 1, 0]]
            )
        elif self.neighborhood == 'M':  # Moore-Neighborhood
            neighborhood = np.array(
                [[1, 1, 1],
                [1, 0, 1],
                [1, 1, 1]]
            )
        else:
            logger.error("Log Error, neighborhood-status undefined")

        return neighborhood

    def get_neighborhood_counts(self) -> int:
        
        padded_universe = np.pad(self.cells, 1, mode="wrap")
    
        return F.conv2d(input=torch.tensor(padded_universe).unsqueeze(0).unsqueeze(0), 
                        weight=torch.tensor(self.neighborhood_kernel()).unsqueeze(0).unsqueeze(0)).squeeze().numpy()

    def update(self, rule: rules.BaseRule):
        """ Apply the rule to each cell to create the field for the next time step"""
        next_generation = self.cells.copy()
        neighborhood_counts = self.get_neighborhood_counts()
        
        alive = np.where(self.cells == 1)
        dead = np.where(self.cells < 1)

        # Apply Rule       
        # TODO Generation Rules 
        next_generation[alive] = np.where(neighborhood_counts[alive] in rule.survive, 1.0, 0)
        next_generation[dead] = np.where(neighborhood_counts[dead] in rule.birth, 1.0, 0)
        
        self.cells = next_generation


    def clear(self):
        """ Resets cells to zeros"""
        self.cells = np.zeros(shape=self.size)

    def soup(self):
        """ Initializes the cells with random soup of 0's and 1's """
        self.cells = np.random.randint(2, size=self.size)

    def resize(self, new_width: int, new_height: int):
        """ Resize the field and copy existing cells into upper left corner"""
        old_cells = self.cells.copy()
        new_cells = np.zeros((new_height, new_width))
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
