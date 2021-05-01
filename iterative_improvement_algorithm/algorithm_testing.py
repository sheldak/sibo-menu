from nutrition_data.nutrition_data_loader import NutritionDataLoader
from iterative_improvement_algorithm.iterative_improvements_algorithm import IterativeImprovementsAlgorithm
from random import randint
from product import Solution
from main import Model

import numpy as np

DATA_FILE = "../nutrition_data/nutrition_database.csv"
PRODUCTS_NUMBER_RANGE = (12, 15)
MIN_GRAMS = 50
MAX_GRAMS = 2000

CATEGORIES = [
    "Vegetables",
    "Meats",
    "Dairy and Egg Products",
    "Fats and Oils",
    "Grains and Pasta",
    "Fruits"
]

restrictions = {
    "calories": (1500, 2500),
    "carbs": (220, 320),
    "protein": (50, 80),
    "fat": (60, 90)
}

restrictions_weights = {
    "calories": 1.0,
    "carbs": 1.0,
    "protein": 1.0,
    "fat": 1.0
}

products_data_loader = NutritionDataLoader(DATA_FILE)
products_data_loader.initial_preprocessing()
model = Model(products_data_loader, restrictions)


def run_tests(step_rate, max_steps, num_initial, rate_scheduler=lambda _epoch, rate: rate):
    initial_solutions = []
    for _ in range(num_initial):
        products_number = randint(PRODUCTS_NUMBER_RANGE[0], PRODUCTS_NUMBER_RANGE[1])
        products = products_data_loader.generate_products(
            CATEGORIES, [max(1, products_number // len(CATEGORIES))] * len(CATEGORIES)
        )

        solution = Solution()
        for product in products:
            solution.add(product, randint(MIN_GRAMS, MAX_GRAMS // len(products)))

        initial_solutions.append(solution)

    incorrect_count = len([sol for sol in initial_solutions if not model.validate(sol)])
    print("before: " + str(incorrect_count) + " out of " + str(num_initial))

    improver = IterativeImprovementsAlgorithm(restrictions, restrictions_weights, max_steps, step_rate, rate_scheduler)
    improver.correct_solutions(initial_solutions)

    incorrect_count = len([sol for sol in initial_solutions if not model.validate(sol)])
    print("after: " + str(incorrect_count) + " out of " + str(num_initial))


sched_1 = lambda epoch, rate: rate * np.exp(-epoch / (1000 * rate))
sched_2 = lambda epoch, rate: rate - np.exp(epoch / rate)

parameters = [(5, 200, 1000, sched_1), (5, 300, 1000, sched_1), (7, 200, 1000, sched_1), (7, 300, 1000, sched_1),
              (9, 200, 1000, sched_1), (9, 300, 1000, sched_1)]

for s, m, n, r in parameters:
    print("Parameters: step rate " + str(s) + " max steps " + str(m))
    run_tests(s, m, n)
