from product import Solution
from typing import List
from solution_scoring import solution_score
import numpy as np

def selection_ranking(solutions: List[Solution], k: int):
    scores = list(map(solution_score, solutions))
    best_indices = np.argpartition(scores, k)
    return list(np.array(solutions)[best_indices[:k]])


def selection_tournament(solutions: List[Solution], k: int):
    n = len(solutions)
    groups_choice = list(range(k)) + [np.random.randint(0, k) for _ in range(n-k)]
    np.random.shuffle(groups_choice)
    groups = [[] for _ in range(k)]
    for (g, s) in zip(groups_choice, solutions):
        groups[g].append(s)
    
    groups_scores = [list(map(solution_score, s_group)) for s_group in groups]
    best_index_in_groups = [np.argmin(scores) for scores in groups_scores]
    return [group[ind] for ind, group in zip(best_index_in_groups, groups)]


def selection_roulette(solutions: List[Solution], k: int):
    scores = np.array(list(map(solution_score, solutions)))
    scores = 1.0 / scores
    scores = scores / np.sum(scores)
    return list(np.random.choice(solutions, k, p=scores))
