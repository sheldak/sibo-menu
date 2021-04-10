from random import randint
from nutrition_data.nutrition_data_loader import NutritionDataLoader
from product import Solution

CALORIES_RANGE = (1500, 2500)
CARBS_RANGE = (220, 320)
PROTEIN_RANGE = (50, 80)
FAT_RANGE = (60, 80)
PRODUCTS_NUMBER_RANGE = (5, 15)

CATEGORIES = [
    "Vegetables",
    "Meats",
    "Dairy and Egg Products",
    "Fats and Oils",
    "Grains and Pasta",
    "Fruits"
]

DATA_FILE = "nutrition_data/nutrition_database.csv"


class Model:
    def __init__(self, products_data_loader: NutritionDataLoader, restrictions):
        self.products_data_loader = products_data_loader
        self.restrictions = restrictions
        self.solutions = []

    def generate_naively(self, solutions_number):
        max_grams = 2000
        max_attempts = 1000

        while len(self.solutions) < solutions_number:
            products_number = randint(self.restrictions["products_number"][0], self.restrictions["products_number"][1])
            products = self.products_data_loader.generate_products(
                CATEGORIES, [max(1, products_number // len(CATEGORIES))] * len(CATEGORIES)
            )

            attempt = 0
            while attempt <= max_attempts:
                solution = Solution()
                for product in products:
                    solution.add(product, randint(50, max_grams // len(products)))

                if self.validate(solution):
                    self.solutions.append(solution)
                    break

                attempt += 1

    def validate(self, solution):
        for element in list(self.restrictions.keys())[:-1]:
            element_weight = 0
            for product_name in solution.products.keys():
                element_weight += \
                    solution.products[product_name][0].nutritional_values[element] * solution.products[product_name][1]

            if element_weight < self.restrictions[element][0] or element_weight > self.restrictions[element][1]:
                return False

        return True


def get_loader_from_file(file_name):
    loader = NutritionDataLoader(file_name)
    loader.initial_preprocessing()
    return loader


def main():
    products_loader = get_loader_from_file(DATA_FILE)
    restrictions = {
        "calories": CALORIES_RANGE,
        "carbs": CARBS_RANGE,
        "protein": PROTEIN_RANGE,
        "fat": FAT_RANGE,
        "products_number": PRODUCTS_NUMBER_RANGE
    }

    model = Model(products_loader, restrictions)
    model.generate_naively(10)

    for solution in model.solutions:
        print(solution)


if __name__ == "__main__":
    main()
