import numpy as np
from typing import List
from model.product import Solution
import random


def mutate(solution: Solution, to_mutate: int, std: float) -> Solution:
    """
    :param solution: base solution; it will be mutated
    :param to_mutate: number of points in base solution to mutate
    :param std: standard deviation of the normal distribution used during mutation
    """

    new_solution = Solution()
    mutations = set(random.sample([x for x in range(len(solution.products))], to_mutate))

    for i, (product, weight) in enumerate(solution.products.values()):
        if i in mutations:
            new_weight = max(0, weight + int(np.random.normal(0, std)))
            new_solution.add(product, new_weight)
        else:
            new_solution.add(product, weight)

    return new_solution


def cross(solutions: List[Solution], cross_points_number: int, preserve_types=True) -> Solution:
    """
    :param solutions: list of solutions which will be crossed; all of solutions should have equal number of products
    :param cross_points_number: points of cross, e.g.:

                   0 1 2 3 4 5 6 7
    solution[0]:   a b c d e f g h
    solution[1]:   i j k l m n o p
    cross_points_number: 2

    program will get 2 random indices, for example: [1, 5]

    result of cross when preserve_types=True:    a j k l m f g h

    before adding products at indices 1 and 5 to the new solution, parent solution, from which the product is taken,
    has to be changed

    :param preserve_types: whether the number of products in every category should be preserved
    """

    solutions_lengths = list(map(lambda sol: len(sol.products), solutions))
    if min(solutions_lengths) != max(solutions_lengths):
        raise Exception("Solutions need to have the same number of products")

    cross_points = set(random.sample([x for x in range(len(solutions[0].products))], cross_points_number))
    products = []

    if preserve_types:
        food_types = list(set(map(lambda value: value[0].food_type, solutions[0].products.values())))
        for solution in solutions:
            solution_products = []
            for food_type in food_types:
                solution_products += \
                    list(filter(lambda values: values[0].food_type == food_type, solution.products.values()))
            products.append(solution_products)
    else:
        products = list(map(lambda sol: list(sol.products.values()), solutions))
        for solution_products in products:
            random.shuffle(solution_products)

    new_solution = Solution()
    curr_solution = 0
    for i in range(len(products[0])):
        if i in cross_points:
            curr_solution = (curr_solution + 1) % len(solutions)

        new_solution.add(*products[curr_solution][i])

    return new_solution
