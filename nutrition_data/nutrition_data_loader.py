from product import Product
from typing import List
import pandas as pd


class NutritionDataLoader:

    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, sep=';')

    def initial_preprocessing(self):
        self.data.pop("ID")
        self.data.dropna(inplace=True)
        sugars = self.data.pop("Sugars (g)")
        sugars = sugars.str.replace(',', '.').astype(float)

        self.data.columns = ["name", "food_type", "calories", "fat", "protein", "carbs", "safety_limit"]

        for macro in ["calories", "protein", "fat", "carbs"]:
            self.data[macro] = self.data[macro].astype(str).str.replace(',', '.').astype(float)

        self.data["carbs"] += sugars

    def generate_products(self, categories: List[str], category_counts: List[int]) -> List[Product]:
        rows = pd.concat(
            [self.data[self.data["food_type"].str.contains(category)].sample(n=category_count)
             for category, category_count in zip(categories, category_counts)]
        )

        products = [Product(
            name=row["name"],
            food_type=row["food_type"],
            calories=row["calories"],
            carbs=row["carbs"],
            protein=row["protein"],
            fat=row["fat"],
            safety_limit=row["safety_limit"]
        ) for _, row in rows.iterrows()]

        return products
