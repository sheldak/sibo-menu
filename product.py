class Product:
    def __init__(self, name, food_type, calories, carbs, protein, fat, safety_limit=None):
        self.name = name
        self.safety_limit = safety_limit
        self.food_type = food_type
        self.nutritional_values = {
            "calories": calories,
            "carbs": carbs,
            "protein": protein,
            "fat": fat
        }

    def __repr__(self):
        return self.name


class Solution:
    def __init__(self):
        self.products = dict()

    def add(self, key: Product, value):
        self.products[key.name] = (key, value)

    def __repr__(self):
        return str({key: val[1] for key, val in self.products.items()})
