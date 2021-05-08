import numpy as np
from model.product import Solution


# ELU score function
# moved up by `alpha` so output values are positive
def score_activation(value: int, threshold: int, alpha: float) -> float:
    centered = value - threshold
    return (centered + alpha) if centered >= 0 else alpha * np.exp(centered)


# Cumulative score for solution
def solution_score(solution: Solution, alpha: float = 1.0) -> float:
    return sum([score_activation(amount, p.safety_limit, alpha) for p, amount in solution.products.values()])
