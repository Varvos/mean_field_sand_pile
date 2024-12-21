"""
Rules for toppling in the sandpile model.
"""

class TopplingRule:
    def topple(self, grid, cell, threshold, neighbors):
        raise NotImplementedError

class SymmetricToppling(TopplingRule):
    def topple(self, grid, cell, threshold, neighbors):
        updates = {}
        mass = grid[cell]
        topples = mass // threshold
        updates[cell] = -topples * threshold
        for neighbor in neighbors:
            updates[neighbor] = updates.get(neighbor, 0) + topples
        return updates

class RandomToppling(TopplingRule):
    def topple(self, grid, cell, threshold, neighbors):
        from numpy.random import multinomial
        updates = {}
        mass = grid[cell]
        topples = mass // threshold
        probs = [1 / len(neighbors)] * len(neighbors)
        redistributed = multinomial(topples, probs)
        updates[cell] = -topples * threshold
        for chips, neighbor in zip(redistributed, neighbors):
            updates[neighbor] = updates.get(neighbor, 0) + chips
        return updates