from model.product import Product
from typing import List
from nutrition_data.nutrition_data_loader import NutritionDataLoader
from itertools import groupby, chain

import numpy as np


class AcoVertex:

    def __init__(self, idx, content: Product, mass: int):
        self.id = idx
        self.content = content
        self.mass = mass

        self.internal_layer = []
        self.external_layer = []

        self.internal_edges = []
        self.external_edges = []

    def __repr__(self):
        return str((self.id, self.content.name, self.mass))

    def connect(self, internal_layer, external_layer):
        self.internal_layer = internal_layer
        self.external_layer = external_layer

        self.internal_edges = np.where([(self.content.name != x.content.name) for x in internal_layer], 1.0, 0.0)
        self.external_edges = np.full(len(external_layer), 1.0 / len(external_layer))

        self.internal_edges /= np.sum(self.internal_edges)
        return self

    def get_next_internal(self):
        return np.random.choice(self.internal_layer, p=self.internal_edges)

    def get_next_external(self):
        return np.random.choice(self.external_layer, p=self.external_edges)

    def update_internal_edge(self, value: float, u):
        self.internal_edges[u.id] = value

    def update_external_edge(self, value: float, u):
        self.external_edges[u.id] = value

    def start_ant_walk(self, category_counts: List[int]):
        current_vertex = self
        for category_count in category_counts:
            for _ in range(category_count - 1):
                yield current_vertex
                current_vertex = current_vertex.get_next_internal()
            yield current_vertex
            current_vertex = current_vertex.get_next_external()


class AcoGraph:
    def __init__(self, categories: List[str],
                 category_count: List[int],
                 loader: NutritionDataLoader,
                 product_copies: int,
                 alpha: float = 1.0):

        products = [
            list(group) for _key, group in
            groupby(
                sorted(
                    chain.from_iterable(
                        map(
                            lambda x: [(x, mass) for mass in np.arange(
                                1.0, alpha * x.safety_limit, (alpha * x.safety_limit / product_copies)
                            )],
                            loader.generate_products(categories, category_count)
                        )
                    ),
                    key=lambda x: x[0].food_type
                ),
                key=lambda x: x[0].food_type
            )
        ]

        vertices = [
            list(map(lambda x: AcoVertex(x[0], x[1][0], x[1][1]), enumerate(product_group)))
            for product_group in products
        ]

        self.layers = [
            list(map(lambda x: x.connect(vertices[group_id], vertices[(group_id + 1) % len(vertices)]), group))
            for group_id, group in enumerate(vertices)
        ]

    def __getitem__(self, item):
        return self.layers[item]
