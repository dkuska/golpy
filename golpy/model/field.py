from loguru import logger
import numpy as np
import torch
import torch.nn.functional as F

import model.rules as rules

class Field:
    def __init__(self, size=(0, 0), neighborhood='M'):
        self.size = size
        self.height, self.width = size
        self.cells =  self.soup()

        self.neighborhood = neighborhood
        self.neighborhood_kernel = self.get_neighborhood()

    def get_neighborhood(self):
        if self.neighborhood == 'N':  # VonNeumann-Neighborhood
            neighborhood = np.array([[0, 1, 0],
                                     [1, 0, 1],
                                     [0, 1, 0]])
        elif self.neighborhood == 'M':  # Moore-Neighborhood
            neighborhood = np.array([[1, 1, 1],
                                     [1, 0, 1],
                                     [1, 1, 1]])
        else:
            logger.error("Log Error, neighborhood-status undefined")

        return neighborhood

    def get_neighborhood_counts(self) -> int:
        padded_universe = np.pad(self.cells, 1, mode="wrap")
        tensor_universe = torch.tensor(padded_universe).unsqueeze(0).unsqueeze(0)
        tensor_neighborhood_kernel = torch.tensor(self.neighborhood_kernel).unsqueeze(0).unsqueeze(0)

        return F.conv2d(input=tensor_universe, weight=tensor_neighborhood_kernel).squeeze().numpy()

    def update(self, rule: rules.BaseRule):
        """ Apply the rule to each cell to create the field for the next time step"""
        # Create copy of cells 
        next_generation = self.cells.copy()
        # Get neighborhood counts for all cells
        neighborhood_counts = self.get_neighborhood_counts()
        # Get living and dead cells
        alive = np.where(self.cells == 1)
        dead = np.where(self.cells < 1)
        
        # TODO: Make this more efficient
        # Decide which logic to apply to update the fields
        if isinstance(rule, rules.LifeRule):
            next_generation[alive] = np.where(np.isin(neighborhood_counts[alive], rule.survive), 
                                              1, 0)
            next_generation[dead] = np.where(np.isin(neighborhood_counts[dead], rule.birth), 
                                             1, 0)
        elif isinstance(rule, rules.GenerationsRule):
            # Update alive cells to either stay alive or start aging
            next_generation[alive] = np.where(np.isin(neighborhood_counts[alive], rule.survive), 
                                              1, (next_generation[alive] + 1) % rule.num_states)
            # Update dead cells to either stay dead or become alive
            next_generation[dead] = np.where(np.isin(neighborhood_counts[dead], rule.birth), 
                                             1, 0)
            # Already aging cells age even more
            already_aging = np.where(self.cells > 1)
            next_generation[already_aging] += 1
            next_generation[already_aging] = next_generation[already_aging] % rule.num_states
        else:
            logger.error("Invalid rule")
        
        self.cells = next_generation

    def clear(self):
        """ Resets cells to zeros"""
        self.cells = np.zeros(shape=self.size)

    def soup(self):
        """ Initializes the cells with random soup of 0's and 1's """
        return np.random.randint(2, size=self.size)
