"""
A module to handle the state of the sandpile model.
"""
from mean_field_piles.base_models.config import SandpileConfig
from scipy.sparse import dok_matrix

class SandpileState:
    def __init__(self, config: SandpileConfig):
        self.grid = dok_matrix((config.grid_size, config.grid_size), dtype=int)
        self.active_cells = set()
        self.threshold = config.threshold

        # Initialize the grid with chips at the center
        center = config.grid_size // 2
        self.grid[center, center] = config.initial_chips
        self.active_cells.add((center, center))

    def get_active_cells(self):
        return self.active_cells

    def apply_updates(self, updates):
        """Apply updates to the grid and determine new active cells."""
        new_active_cells = set()
        for cell, value in updates.items():
            self.grid[cell] += value
            if self.grid[cell] >= self.threshold:
                new_active_cells.add(cell)
        self.active_cells = new_active_cells

    def reset_active_cells(self):
        self.active_cells.clear()