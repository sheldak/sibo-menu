from typing import Dict, Tuple, Union, List
from product import Solution


class IterativeImprovementsAlgorithm:

    def __init__(self, restrictions: Dict[str, Tuple[int, int]],
                 restrictions_weights: Dict[str, float],
                 max_steps: int, step_rate: float,
                 rate_scheduler=lambda _, x: x):

        self.restrictions = restrictions
        self.restrictions_weights = restrictions_weights
        self.max_steps = max_steps
        self.step_rate = step_rate
        self.rate_scheduler = rate_scheduler

    def _update_solution(self, restriction: str, solution: Solution, slope: int, epoch: int):
        for product_name, (product_data, product_amount) in solution.products.items():
            product_amount += self.rate_scheduler(epoch, self.step_rate) * slope \
                              * product_data.nutritional_values[restriction] / 100
            solution.products[product_name] = (product_data, product_amount)

    def _dominant_restriction(self, solution: Solution) -> Union[Tuple[str, int], None]:
        violations = []

        for restriction, (low, high) in self.restrictions.items():
            weight = sum(
                [product_amount * product_data.nutritional_values[restriction] / 100
                 for product_name, (product_data, product_amount) in solution.products.items()]
            )

            if weight < low:
                violations.append((restriction, self.restrictions_weights[restriction] * (low - weight) / low, 1))
            elif weight > high:
                violations.append((restriction, self.restrictions_weights[restriction] * (weight - high) / high, -1))

        if not violations:
            return None

        violations.sort(key=lambda x: x[1])
        return violations[-1][0], violations[-1][2]

    def correct_solutions(self, solutions: List[Solution]):
        for epoch in range(self.max_steps):
            for solution in solutions:
                dominant_restriction = self._dominant_restriction(solution)
                if dominant_restriction is not None:
                    restriction, slope = dominant_restriction
                    self._update_solution(restriction, solution, slope, epoch)
