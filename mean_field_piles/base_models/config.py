"""
This module defines configuration classes and enumerations for a sandpile model simulation.
Classes:
    TopplingType (Enum): Enumeration of different toppling types in the sandpile model.
        - SYMMETRIC: Symmetric toppling.
        - RANDOM: Random toppling.
        - MEAN_FIELD: Mean-field toppling.
        - POTENTIAL: Potential-based toppling.
    SandpileConfig (dataclass): Configuration class for the sandpile model.
        Attributes:
            grid_size (int): Size of the grid.
            threshold (int): Threshold value for toppling.
            toppling_type (TopplingType): Type of toppling mechanism.
            initial_chips (int): Initial number of chips in the grid.
            interaction_radius (Optional[int]): Interaction radius for mean-field or potential-based toppling.
            potential_params (Optional[Dict[str, Any]]): Parameters for potential-based toppling.
        Methods:
            __post_init__: Validates the configuration after initialization.
            validate: Validates the configuration parameters.

"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

class TopplingType(Enum):
    SYMMETRIC = "sym"
    RANDOM = "rnd"
    MEAN_FIELD = "mean_field"
    POTENTIAL = "potential"

@dataclass
class SandpileConfig:
    grid_size: int
    threshold: int
    toppling_type: TopplingType
    initial_chips: int
    interaction_radius: Optional[int] = None
    potential_params: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if self.grid_size <= 0:
            raise ValueError("Grid size must be positive.")
        if self.threshold <= 0:
            raise ValueError("Threshold must be positive.")
        if self.initial_chips <= 0:
            raise ValueError("Initial chips must be positive.")
        if self.toppling_type not in TopplingType:
            raise ValueError(f"Invalid toppling type. Choose from {[t.value for t in TopplingType]}")
        if self.toppling_type in (TopplingType.MEAN_FIELD, TopplingType.POTENTIAL) and not self.interaction_radius:
            raise ValueError("Interaction radius required for mean-field or potential-based toppling")
