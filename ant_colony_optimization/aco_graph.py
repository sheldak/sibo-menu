from model.product import Product
from typing import List
from nutrition_data.nutrition_data_loader import NutritionDataLoader
from itertools import groupby, chain

import numpy as np

INTERNAL_EDGE = 0
EXTERNAL_EDGE = 1

class AcoVertex:

    def __init__(self, idx, content: Product, mass: int):
        self.id = idx
        self.content = content
        self.mass = mass

        self.internal_layer = []
        self.external_layer = []

        self.internal_edges_pheromone = []
        self.external_edges_pheromone = []

        self.internal_edges_probability = []
        self.external_edges_probability = []

    def __repr__(self):
        return str((self.id, self.content.name, self.mass))

    def connect(self, internal_layer, external_layer):
        self.internal_layer = internal_layer
        self.external_layer = external_layer

        self.internal_edges_pheromone_changed = True
        self.external_edges_pheromone_changed = True

        self.internal_edges_pheromone = np.where([(self.content.name != x.content.name) for x in internal_layer], 1.0, 0.0)
        self.external_edges_pheromone = np.full(len(external_layer), 1.0)

        self.calculate_internal_prob()
        self.calculate_external_prob()

        return self

    def get_next_internal(self):
        self.calculate_internal_prob()
        return np.random.choice(self.internal_layer, p=self.internal_edges_probability)

    def get_next_external(self):
        self.calculate_external_prob()
        return np.random.choice(self.external_layer, p=self.external_edges_probability)

    def scale_internal_pheromones(self, factor: float):
        self.internal_edges_pheromone *= factor
        self.internal_edges_pheromone_changed = True

    def scale_external_pheromones(self, factor: float):
        self.external_edges_pheromone *= factor
        self.external_edges_pheromone_changed = True

    def update_internal_pheromone(self, value: float, u):
        self.internal_edges_pheromone[u.id] += value
        self.internal_edges_pheromone_changed = True

    def update_external_pheromone(self, value: float, u):
        self.external_edges_pheromone[u.id] += value
        self.external_edges_pheromone_changed = True

    def replace_internal_pheromone(self, value: float, u):
        self.internal_edges_pheromone[u.id] = value
        self.internal_edges_pheromone_changed = True

    def replace_external_pheromone(self, value: float, u):
        self.external_edges_pheromone[u.id] = value
        self.external_edges_pheromone_changed = True

    def calculate_internal_prob(self):
        if self.internal_edges_pheromone_changed:
            self.internal_edges_probability = self.internal_edges_pheromone / np.sum(self.internal_edges_pheromone)
            self.internal_edges_pheromone_changed = False

    def calculate_external_prob(self):
        if self.external_edges_pheromone_changed:
            self.external_edges_probability = self.external_edges_pheromone / np.sum(self.external_edges_pheromone)
            self.external_edges_pheromone_changed = False


    # def start_ant_walk(self, category_counts: List[int]):
    #     '''
    #     :param category_counts: How many products from each category do we want in a solution, constructed by this walk
    #     :return: Iterator of products that may create a solution.
    #     '''

    #     current_vertex = self
    #     for category_count in category_counts:
    #         for _ in range(category_count - 1):
    #             yield current_vertex
    #             current_vertex = current_vertex.get_next_internal()
    #         yield current_vertex
    #         current_vertex = current_vertex.get_next_external()


class AcoGraph:
    def __init__(self, categories: List[str],
                 category_count: List[int],
                 loader: NutritionDataLoader,
                 product_copies: int,
                 alpha: float = 1.0):

        '''
        :param categories: List of food categories recognized by NutritionDataLoader
        :param category_count: How many products from each category do we want in a graph
        :param loader: NutritionDataLoader instance
        :param product_copies: How many vertices we want to create from one product sampled by data loader
        :param alpha: This parameter governs our tolerance for the value of cost function
        '''

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

        self.starting_vertex = AcoVertex(0, None, 0)
        self.starting_vertex.connect([], vertices[0])

    def __getitem__(self, item):
        return self.layers[item]


    def start_ant_walk(self, category_counts: List[int]):
        '''
        :param category_counts: How many products from each category do we want in a solution, constructed by this walk
        :return: Iterator of (edge_type, product) that may create a solution.
        '''

        current_edge_type = EXTERNAL_EDGE
        current_vertex = self.starting_vertex
        current_vertex = current_vertex.get_next_external()
        for category_count in category_counts:
            for _ in range(category_count - 1):
                yield (current_edge_type, current_vertex)
                current_vertex = current_vertex.get_next_internal()
                current_edge_type = INTERNAL_EDGE
            yield (current_edge_type, current_vertex)
            current_vertex = current_vertex.get_next_external()
            current_edge_type = EXTERNAL_EDGE

    def decrease_pheromone(self, ratio: float):
        for v in [self.starting_vertex] + sum(self.layers, []):
            v.scale_external_pheromones(ratio)
            v.scale_internal_pheromones(ratio)
