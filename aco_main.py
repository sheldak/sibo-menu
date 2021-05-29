from model.product import Solution
from ant_colony_optimization.aco_graph import AcoGraph
from ant_colony_optimization.aco_ant import Ant, calculate_pheromone_amount, calculate_nutritions
from genetic_main import get_loader_from_file
import matplotlib.pyplot as plt

import json
import numpy as np


config = json.load(open('config.json'))
# np.random.seed(config['numpy_random_state'])

restrictions = config["restrictions"]


def simple_cost(r_d, r_u, x):
    if x < r_d:
        return np.exp((r_d - x)/50)
    elif x <= r_u:
        return 0
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


def plot(solutions_costs, ants_count):
    iterations_averages = []
    for i in range(len(solutions_costs) // ants_count):
        sublist = solutions_costs[i*ants_count:(i+1)*ants_count]
        iterations_averages.append(sum(sublist) // len(sublist))

    plt.plot(np.arange(len(solutions_costs) // ants_count), iterations_averages)
    plt.title("Iterations averages")
    plt.xlabel("Iterations")
    plt.ylabel("Average cost")
    plt.yscale("log")

    plt.show()


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
    ants_count = config["aco"]["ants_count"]
    iterations = config["aco"]["iterations"]

    ants = [Ant(aco_graph, categories_count) for _ in range(ants_count)]

    solutions = []
    solutions_costs = []
    worst_taken_solution = None
    worst_taken_solution_cost = 10**9
    solutions_count = config["aco"]["solutions_count"]

    for _ in range(iterations):
        
        # Let ants find solutions
        for ant in ants: 
            ant.traverse_graph()

        # Pheromone evaporation
        aco_graph.decrease_pheromone(pheromone_decrease_ratio)

        # Add new pheromones and if good enough, then add to the best solutions list
        for ant in ants:
            amount = calculate_pheromone_amount(ant.get_solution(), Q, calculate_solution_cost)
            ant.leave_pheromone(amount)

            solution = ant.get_solution()
            solution_cost = calculate_solution_cost(solution)
            if len(solutions) < solutions_count:
                solutions.append((solution, solution_cost))
                worst_taken_solution, worst_taken_solution_cost = max(solutions, key=lambda sol: sol[1])
            elif solution_cost < worst_taken_solution_cost:
                solutions.remove((worst_taken_solution, worst_taken_solution_cost))
                solutions.append((solution, solution_cost))
                worst_taken_solution, worst_taken_solution_cost = max(solutions, key=lambda sol: sol[1])

            solutions_costs.append(solution_cost)

    plot(solutions_costs, ants_count)

    for solution in sorted(solutions, key=lambda sol: sol[1]):
        print(solution[1], solution[0])


if __name__ == '__main__':
    main()
