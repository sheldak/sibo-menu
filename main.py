from nutrition_data.nutrition_data_loader import NutritionDataLoader
from genetic_operations import mutate, cross
from naive_initialization.naive_initialization import generate_naively

CALORIES_RANGE = (1500, 2500)
CARBS_RANGE = (220, 320)
PROTEIN_RANGE = (50, 80)
FAT_RANGE = (60, 80)
PRODUCTS_NUMBER_RANGE = (5, 15)

DATA_FILE = "nutrition_data/complete_database.csv"


class Model:
    def __init__(self, products_data_loader: NutritionDataLoader, restrictions):
        self.products_data_loader = products_data_loader
        self.restrictions = restrictions
        self.solutions = []

    def validate(self, solution):
        for element in list(self.restrictions.keys()):
            if element not in list(solution.products.values())[0][0].nutritional_values:
                continue
            element_weight = 0
            for product_name in solution.products.keys():
                element_weight += \
                    solution.products[product_name][0].nutritional_values[element] * solution.products[product_name][1] / 100

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
    generate_naively(model, 2)

    for solution in model.solutions:
        print(solution)

    print()
    print(mutate(cross(model.solutions[:2], 3, True), 2, 15))


if __name__ == "__main__":
    main()
