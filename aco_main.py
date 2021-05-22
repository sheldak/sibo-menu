from ant_colony_optimization.aco_graph import AcoGraph
from genetic_main import get_loader_from_file

import json
import numpy as np
import pickle

config = json.load(open('config.json'))
np.random.seed(config['numpy_random_state'])


def main():
    categories = config['categories']
    category_count = [config['aco_total_product_count'] // len(categories) for _ in categories]

    loader = get_loader_from_file(config['nutrition_data'])
    loader.allow_replacement_sampling()

    products_range = config['restrictions']['products_number']
    product_count = np.random.randint(products_range[0], products_range[1])
    per_category_count = [max(1, product_count // len(categories))] * len(categories)

    try:
        aco_graph = pickle.load(open('.pickled/aco_graph.pkl', 'rb'))
    except FileNotFoundError:
        aco_graph = AcoGraph(categories, category_count, loader, config['product_copies'])
        pickle.dump(aco_graph, open('.pickled/aco_graph.pkl', 'w+b'))


if __name__ == '__main__':
    main()
