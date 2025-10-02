"""
Rules Module (rules.py)
"""
from abc import ABC, abstractmethod
from typing import Dict, Tuple, List
import numpy as np

class TopplingRule(ABC):
    @abstractmethod
    def topple(self, state: SandpileState, cell: Tuple[int, int], 
               neighbors: List[Tuple[int, int]]) -> Dict[Tuple[int, int], float]:
        pass

class SymmetricToppling(TopplingRule):
    def topple(self, state: SandpileState, cell: Tuple[int, int],
               neighbors: List[Tuple[int, int]]) -> Dict[Tuple[int, int], float]:
        updates = {cell: -state.grid[cell]}
        share = state.grid[cell] / len(neighbors)
        for neighbor in neighbors:
            updates[neighbor] = share
        return updates

class MeanFieldToppling(TopplingRule):
    def __init__(self, config: SandpileConfig):
        self.interaction_radius = config.interaction_radius
    
    def topple(self, state: SandpileState, cell: Tuple[int, int],
               neighbors: List[Tuple[int, int]]) -> Dict[Tuple[int, int], float]:
        # Compute force from mean field
        com = state.center_of_mass
        direction = np.array(cell) - com
        if np.any(direction):
            direction = direction / np.linalg.norm(direction)
            
        # Weight neighbors based on force direction
        weights = []
        for neighbor in neighbors:
            neighbor_direction = np.array(neighbor) - np.array(cell)
            weight = np.dot(direction, neighbor_direction) if np.any(neighbor_direction) else 0
            weights.append(max(0, weight))
            
        total_weight = sum(weights) or 1
        weights = [w/total_weight for w in weights]
        
        # Apply toppling with weighted distribution
        updates = {cell: -state.grid[cell]}
        for neighbor, weight in zip(neighbors, weights):
            updates[neighbor] = state.grid[cell] * weight
        return updates
