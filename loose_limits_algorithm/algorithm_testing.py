from nutrition_data.nutrition_data_loader import NutritionDataLoader
from loose_limits_algorithm import LooseLimitsAlgorithm
from random import randint
from product import Solution
from main import Model

import numpy as np

DATA_FILE = "./nutrition_data/nutrition_database.csv"
PRODUCTS_NUMBER_RANGE = (5, 15)
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
    "calories": (2100, 2500),
    "carbs": (260, 320),
    "protein": (65, 80),
    "fat": (70, 90)
}

avg_restrictions = {
    name: (r[0] + r[1]) / 2 for name, r in restrictions.items()
}

def simple_looseness(r_d, r_u, x):
    if x < r_d:
        return np.exp(min((r_d - x)/r_d, 2)) - 1
    elif x <= r_u:
        return 0
    else:
        return np.exp(min((x - r_u)/r_u, 2)) - 1

looseness_functions = {
    "calories": simple_looseness,
    "carbs": simple_looseness,
    "protein": simple_looseness,
    "fat": simple_looseness
}

products_data_loader = NutritionDataLoader(DATA_FILE)
products_data_loader.initial_preprocessing()
model = Model(products_data_loader, restrictions)

algo = LooseLimitsAlgorithm(restrictions, looseness_functions, 100, 50, MIN_GRAMS, MAX_GRAMS)
solutions = [
    algo.look_for_solution(products_data_loader.generate_products(CATEGORIES, [3, 2, 2, 2, 2, 2])) for _ in range(100)
]

# print(len(list(filter(lambda t: t[1] == 0, solutions)))/len(solutions))
print(len(list(filter(lambda t: t[1] < 0.1, solutions)))/len(solutions))

for sol, amount in filter(lambda t: 0 < t[1] < 0.1, solutions):
    print(algo.calculate_nutritions(sol).items(), amount)