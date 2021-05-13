from nutrition_data.nutrition_data_loader import NutritionDataLoader

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
