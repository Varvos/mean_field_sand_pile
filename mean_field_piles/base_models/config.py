"""
Base Sandpile config
"""

class SandpileConfig:
    def __init__(self, grid_size: int, threshold: int, toppling_rule: str, initial_chips: int):
        self.grid_size = grid_size
        self.threshold = threshold
        self.toppling_rule = toppling_rule
        self.initial_chips = initial_chips

        self.validate()

    def validate(self):
        if self.grid_size <= 0:
            raise ValueError("Grid size must be positive.")
        if self.threshold <= 0:
            raise ValueError("Threshold must be positive.")
        if self.initial_chips <= 0:
            raise ValueError("Initial chips must be positive.")
        if self.toppling_rule not in ["sym", "rnd"]:
            raise ValueError("Invalid toppling rule. Choose 'sym' or 'rnd'.")