from typing import Callable, DefaultDict, Dict, Tuple, Union, List
from product import Product, Solution
from dataclasses import dataclass
from collections import defaultdict
import numpy as np
import copy

@dataclass
class LooseLimitsAlgorithm: 
    restrictions: Dict[str, Tuple[int, int]]
    looseness_functions: Dict[str, Callable[[int, int, int], float]] 
    max_steps: int
    max_looseness: float
    min_grams: int
    max_grams: int

    def calculate_looseness(self, solution: Solution) -> float:
        nutritions_acc = self.calculate_nutritions(solution)
        return sum(
            [
                loose_func(
                    self.restrictions[nutrition_name][0],
                    self.restrictions[nutrition_name][1],
                    nutritions_acc[nutrition_name]
                ) for nutrition_name, loose_func in self.looseness_functions.items()
            ]
        )

    def calculate_nutritions(self, solution: Solution) -> DefaultDict[str, float]:
        nutritions_acc = defaultdict(lambda: 0.0)
        for product_data, product_ammount in solution.products.values():
            for nutrition_name, nutrition_ammount in product_data.nutritional_values.items():
                nutritions_acc[nutrition_name] = nutritions_acc[nutrition_name] + (nutrition_ammount/100)*product_ammount
        return nutritions_acc

    def calculate_nutrition_avg_factor(self, solution: Solution) -> float:
        avg_restrictions = {
            name: (r[0] + r[1]) / 2 for name, r in self.restrictions.items()
        }    
        nutritions = self.calculate_nutritions(solution)
        factors = [ammount / avg_restrictions[name] for name, ammount in nutritions.items()]
        return sum(factors)/len(factors)

    def look_for_solution(self, products: List[Product]):
        solution = Solution()
        for product in products:
            solution.add(product, 2000)

        factor = self.calculate_nutrition_avg_factor(solution)
        for name in solution.products.keys():
            product_data, product_ammount = solution.products[name]
            solution.products[name] = (
                product_data, 
                max(
                    self.min_grams, 
                    int(product_ammount / np.random.normal(factor, factor/5))
                )
            )

        best_solution = solution
        best_solution_score = self.calculate_looseness(solution)
        temp = 0.1
        for _ in range(100):
            solution = Solution()

            factor = self.calculate_nutrition_avg_factor(best_solution)
            for name in best_solution.products.keys():
                product_data, product_ammount = best_solution.products[name]
                solution.add(
                    product_data, 
                    max(
                        self.min_grams, 
                        int(product_ammount / np.random.normal(factor, temp*factor))
                    )
                )

            sol_score = self.calculate_looseness(solution)
            if sol_score == 0:
                return (solution, 0)
            if sol_score < best_solution_score:
                temp = max(temp/1.01, 0.05)
                best_solution_score = sol_score
                best_solution = solution
            else:
                temp = min(temp*1.01, 0.2)

        return (best_solution, best_solution_score)
        
            
