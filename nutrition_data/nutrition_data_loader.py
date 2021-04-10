from main import Product
from typing import Set, List
import pandas as pd


class NutritionDataLoader:

    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, sep=';')

    def initial_preprocessing(self):
        self.data.pop("ID")
        self.data.dropna(inplace=True)
        sugars = self.data.pop("Sugars (g)")
        sugars = sugars.str.replace(',', '.').astype(float)

        self.data.columns = ["name", "food_type", "calories", "fat", "protein", "carbs"]

        for macro in ["calories", "protein", "fat", "carbs"]:
            self.data[macro] = self.data[macro].str.replace(',', '.').astype(float)

        self.data["carbs"] += sugars

    def display_food_types(self) -> Set[str]:
        return set(self.data["food_type"].tolist()) - {0.0}

    def generate_products(self, categories: List[str], category_counts: List[int]) -> List[Product]:

        rows = [self.data[self.data["food_type"].str.contains(category)].sample(n=category_count)
                for category in categories for category_count in category_counts]

        products = [Product(
            name=row["name"].values[0],
            food_type=row["food_type"].values[0],
            calories=row["calories"].values[0],
            carbs=row["carbs"].values[0],
            protein=row["protein"].values[0],
            fat=row["fat"].values[0]
        ) for row in rows]

        return products



