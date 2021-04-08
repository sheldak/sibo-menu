from random import randint, sample

CALORIES_RANGE = (1500, 2500)
CARBS_RANGE = (220, 320)
PROTEIN_RANGE = (50, 80)
FAT_RANGE = (60, 80)
PRODUCTS_NUMBER_RANGE = (5, 15)


class Product:
    def __init__(self, name, harmfulness, calories, carbs, protein, fat):
        self.name = name
        self.harmfulness = harmfulness
        self.nutritional_values = {
            "calories": calories,
            "carbs": carbs,
            "protein": protein,
            "fat": fat
        }


class Solution:
    def __init__(self):
        self.products = dict()

    def add(self, key, value):
        self.products[key] = value


class Model:
    def __init__(self, products, restrictions):
        self.products = products
        self.restrictions = restrictions
        self.solutions = []

    def generate_naively(self, solutions_number):
        max_grams = 2000
        max_attempts = 1000

        while len(self.solutions) < solutions_number:
            products_number = randint(self.restrictions["products_number"][0], self.restrictions["products_number"][1])
            products = sample(self.products.keys(), products_number)

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
                    self.products[product_name].nutritional_values[element] * solution.products[product_name]

            if element_weight < self.restrictions[element][0] or element_weight > self.restrictions[element][1]:
                return False

        return True


def read_products_from_file(file_name):
    # TODO read products from file and return as dictionary:
    #  name -> Product(name, harmfulness function, kcal/g, carbs/g, protein/g, fat/g)

    # with open(file_name) as file:
    return {
        "water": Product("water", lambda _: 0, 0, 0, 0, 0),
        "water1": Product("water1", lambda _: 0, 1.5, 0.12, 0.01, 0.04),
        "water2": Product("water2", lambda _: 0, 2.3, 0.23, 0.06, 0.2),
        "water3": Product("water3", lambda _: 0, 4, 1, 0.03, 0.15),
        "water4": Product("water4", lambda _: 0, 3.2, 1.5, 0.04, 0.13),
        "water5": Product("water5", lambda _: 0, 0.6, 0.11, 0.02, 0.12),
        "water6": Product("water6", lambda _: 0, 0.5, 0.06, 0.01, 0.06),
        "water7": Product("water7", lambda _: 0, 6, 0.12, 0.1, 0.02),
        "water8": Product("water8", lambda _: 0, 1.2, 0.01, 0.12, 0.07),
        "water9": Product("water9", lambda _: 0, 2.3, 0.03, 0.08, 0.06),
        "water10": Product("water10", lambda _: 0, 7.5, 0, 0.16, 0.03),
        "water11": Product("water11", lambda _: 0, 1.1, 0.04, 0.4, 0.12),
        "water12": Product("water12", lambda _: 0, 2.6, 0.08, 0.32, 0.13),
        "water13": Product("water13", lambda _: 0, 0.4, 0.1, 0.22, 0.06),
        "water14": Product("water14", lambda _: 0, 0.2, 0.07, 0.05, 0.02),
        "water15": Product("water15", lambda _: 0, 0.1, 0.03, 0.09, 0.09),
    }


def main():
    products = read_products_from_file("some_file.csv")
    restrictions = {
        "calories": CALORIES_RANGE,
        "carbs": CARBS_RANGE,
        "protein": PROTEIN_RANGE,
        "fat": FAT_RANGE,
        "products_number": PRODUCTS_NUMBER_RANGE
    }

    model = Model(products, restrictions)
    model.generate_naively(10)

    for solution in model.solutions:
        print(solution.products)


if __name__ == "__main__":
    main()
