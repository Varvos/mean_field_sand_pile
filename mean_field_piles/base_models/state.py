
"""
A module to handle the state of the sandpile model.
"""
from typing import Set, Tuple, Dict
import numpy as np
from scipy.sparse import dok_matrix

class SandpileState:
    def __init__(self, config: SandpileConfig):
        self.grid = dok_matrix((config.grid_size, config.grid_size), dtype=float)
        self.active_cells: Set[Tuple[int, int]] = set()
        self.threshold = config.threshold
        self.force_field = np.zeros((config.grid_size, config.grid_size, 2))
        self.density_field = np.zeros((config.grid_size, config.grid_size))
        
        # Initialize center
        center = config.grid_size // 2
        self.grid[center, center] = config.initial_chips
        self.active_cells.add((center, center))
        self._update_fields()
    
    def _update_fields(self):
        """Update density and force fields based on current state."""
        self.density_field = self.grid.toarray()
        # Force field updates will be handled by specific toppling rules
    
    def apply_updates(self, updates: Dict[Tuple[int, int], float]):
        """Apply updates and update fields."""
        new_active_cells = set()
        for cell, value in updates.items():
            self.grid[cell] += value
            if self.grid[cell] >= self.threshold:
                new_active_cells.add(cell)
        self.active_cells = new_active_cells
        self._update_fields()
    
    @property
    def center_of_mass(self) -> np.ndarray:
        """Compute center of mass of the sandpile."""
        grid_array = self.grid.toarray()
        total_mass = np.sum(grid_array)
        if total_mass == 0:
            return np.array([self.grid.shape[0]//2, self.grid.shape[1]//2])
        
        y, x = np.mgrid[0:self.grid.shape[0], 0:self.grid.shape[1]]
        com_x = np.sum(x * grid_array) / total_mass
        com_y = np.sum(y * grid_array) / total_mass
        return np.array([com_x, com_y])