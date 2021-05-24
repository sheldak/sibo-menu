from collections import defaultdict
from model.product import Solution
from typing import Callable, DefaultDict, Dict, List, Tuple
# from nutrition_data.nutrition_data_loader import NutritionDataLoader
from ant_colony_optimization.aco_graph import AcoGraph, AcoVertex, EXTERNAL_EDGE, INTERNAL_EDGE

import numpy as np

class Ant:
    def __init__(self, 
            graph: AcoGraph,
            categories_count: List[int]):
        self.graph = graph
        self.trace = []
        self.categories_count = categories_count

    def traverse_graph(self):
        self.trace = list(self.graph.start_ant_walk(self.categories_count))

    def leave_pheromone(self, ammount):
        for u, v in zip([(None, self.graph.starting_vertex)] + self.trace, self.trace):
            _,      u_vertex = u
            v_type, v_vertex = v
            if v_type == INTERNAL_EDGE:
                u_vertex.update_internal_pheromone(ammount, v_vertex)

            if v_type == EXTERNAL_EDGE:
                u_vertex.update_external_pheromone(ammount, v_vertex)

    def get_solution(self) -> Solution:
        solution = Solution()
        for _, vertex in self.trace:
            solution.add(vertex.content, vertex.mass)
        return solution


def calculate_nutritions(solution: Solution) -> DefaultDict[str, float]:
    nutritions_acc = defaultdict(lambda: 0.0)
    for product_data, product_ammount in solution.products.values():
        for nutrition_name, nutrition_ammount in product_data.nutritional_values.items():
            nutritions_acc[nutrition_name] = nutritions_acc[nutrition_name] + (nutrition_ammount/100)*product_ammount
    return nutritions_acc

def calculate_pheromone_ammount(solution: Solution, Q: float, solution_cost_function: Callable) -> float:
    return Q / solution_cost_function(solution)