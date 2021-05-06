from product import Solution
from random import randint

CATEGORIES = [
    "Vegetables",
    "Meats",
    "Dairy and Egg Products",
    "Fats and Oils",
    "Grains and Pasta",
    "Fruits"
]


def generate_naively(model, solutions_number):
    max_grams = 2000
    max_attempts = 1000

    while len(model.solutions) < solutions_number:
        products_number = randint(model.restrictions["products_number"][0], model.restrictions["products_number"][1])
        products = model.products_data_loader.generate_products(
            CATEGORIES, [max(1, products_number // len(CATEGORIES))] * len(CATEGORIES)
        )

        attempt = 0
        while attempt <= max_attempts:
            solution = Solution()
            for product in products:
                solution.add(product, randint(50, max_grams // len(products)))

            if model.validate(solution):
                model.solutions.append(solution)
                break

            attempt += 1
