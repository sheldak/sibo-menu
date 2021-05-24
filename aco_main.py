from model.product import Solution
from ant_colony_optimization.aco_graph import AcoGraph
from ant_colony_optimization.aco_ant import Ant, calculate_pheromone_ammount, calculate_nutritions
from genetic_main import get_loader_from_file

import json
import numpy as np


config = json.load(open('config.json'))
# np.random.seed(config['numpy_random_state'])

restrictions = config["restrictions"]

def simple_cost(r_d, r_u, x):
    if x < r_d:
        return np.exp((r_d - x)/50)
    elif x <= r_u:
        return 1
    else:
        return np.exp((x - r_u)/50)

cost_functions = {
    nutr: lambda x: simple_cost(
        restrictions[nutr][0], 
        restrictions[nutr][1], x) for nutr in ["calories", "carbs", "protein", "fat"]
}

def calculate_solution_cost(solution: Solution):
    nutritions_acc = calculate_nutritions(solution)
    return sum(
        [
            cost_func(
                nutritions_acc[nutrition_name]
            ) for nutrition_name, cost_func in cost_functions.items()
        ]
    )


def main():
    categories = config['categories']
    category_count = [config['aco_total_product_count'] // len(categories) for _ in categories]

    loader = get_loader_from_file(config['nutrition_data'])
    loader.allow_replacement_sampling()

    products_range = config['restrictions']['products_number']
    product_count = np.random.randint(products_range[0], products_range[1])

    aco_graph = AcoGraph(categories, category_count, loader, config['product_copies'])
    per_category_count = [max(1, product_count // len(categories))] * len(categories)

    categories_count = config["categories_count"]
    pheromone_decrease_ratio = config["aco"]["pheromone_decrease_ratio"]
    Q = config["aco"]["Q"]

    # Create ants (they can be used multiple times)
    ants = [Ant(aco_graph, categories_count) for i in range(10)]
    for _ in range(10):
        
        # Let ants find solutions
        for ant in ants: 
            ant.traverse_graph()

        # Pheromone evaporation
        aco_graph.decrease_pheromone(pheromone_decrease_ratio)

        # Add new pheromones
        for ant in ants:
            ammount = calculate_pheromone_ammount(ant.get_solution(), Q, calculate_solution_cost)
            ant.leave_pheromone(ammount)

if __name__ == '__main__':
    main()
