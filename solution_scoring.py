import numpy as np
from product import Solution

# ELU score function
# moved up by `alpha` so output values are positive
def score_activation(value: int, threshold: int, alpha: float = 1.0) -> float:
    centered = value - threshold
    return (centered + alpha) if centered >= 0 else alpha * np.exp(centered)


# Cumulative score for solution
def solution_score(solution: Solution) -> float:
    return sum([score_activation(amount, p.safety_limit) for p, amount in solution.products.values()])