from typing import List, Callable, Dict, Union
from model.product import Solution
from model.model import Model

import logging
import numpy as np
import itertools


class GeneticAlgorithm:
    def __init__(self, selection_algorithm: Callable[[List[Solution], int], List[Solution]],
                 unary_genetic_operation: Callable[[Solution, int, float], Solution],
                 binary_genetic_operation: Callable[[List[Solution], int, bool], Solution],
                 model: Model,
                 scoring_function: Callable[[Solution, float], float]):

        self.selection_algorithm = selection_algorithm
        self.unary_genetic_operation = unary_genetic_operation
        self.binary_genetic_operation = binary_genetic_operation
        self.model = model
        self.scoring_function = scoring_function

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("genetic algorithm")

    def _get_population_info(self, population: List[Solution], epoch: int, scoring_params: Dict[str, float]):
        scores = [self.scoring_function(solution, **scoring_params) for solution in population]
        population_info = [np.min(scores), np.max(scores), np.mean(scores), np.std(scores)]
        self.logger.info(
            'Epoch: {}, minimal score: {}, maximal score: {}, average score: {}, score std: {}'.format(
                epoch, *population_info
            )
        )
        return population_info

    def _warn_restrictions(self, operation: str, population: List[Solution]):
        violated = len(list(filter(lambda x: x, [self.model.validate(sol) for sol in population])))
        in_use = len(population) - violated
        self.logger.warning(
            '{} created {} solutions that violate restrictions. {} will be used.'.format(
                operation, str(violated), str(in_use)
            )
        )

    def _compare(self, population1: List[Solution], population2: List[Solution], scoring_params) -> bool:
        avg_score1 = sum([self.scoring_function(sol, **scoring_params) for sol in population1])
        avg_score2 = sum([self.scoring_function(sol, **scoring_params) for sol in population2])
        return avg_score1 < avg_score2

    def run_evolution(self, epoch_count: int,
                      initial_population: List[Solution],
                      selection_params: Dict[str, int],
                      unary_op_params: Dict[str, Union[int, float]],
                      binary_op_params: Dict[str, Union[int, float, bool]],
                      scoring_params: Dict[str, float]) -> List[Solution]:

        best_population = self.selection_algorithm(initial_population, **selection_params)
        curr_population = initial_population
        for epoch in range(epoch_count):
            curr_population = self.selection_algorithm(curr_population, **selection_params)
            self._get_population_info(curr_population, epoch, scoring_params)
            if self._compare(curr_population, best_population, scoring_params):
                best_population = curr_population

            mutated = [
                self.unary_genetic_operation(solution, **unary_op_params) for solution in curr_population
            ]
            self._warn_restrictions("unary operation", mutated)
            mutated = [mutant for mutant in mutated if self.model.validate(mutant)]

            copulated = np.apply_along_axis(
                lambda x: self.binary_genetic_operation(list(x), **binary_op_params), 1,
                list(filter(lambda x: x[0] != x[1] and len(x[0].products) == len(x[1].products),
                            itertools.product(curr_population, curr_population))))
            self._warn_restrictions("binary operation", copulated)
            copulated = [child for child in copulated if self.model.validate(child)]

            curr_population.extend(mutated)
            curr_population.extend(copulated)

        return best_population
