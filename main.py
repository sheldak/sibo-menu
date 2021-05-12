from numpy.random import randint
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from genetic_algorithm.selection_algos import *
from genetic_algorithm.genetic_operations import mutate, cross
from nutrition_data.nutrition_data_loader import NutritionDataLoader
from iterative_improvement_algorithm.iterative_improvements_algorithm import IterativeImprovementsAlgorithm
from model.model import Model
from model.product import Solution

import json
import pickle
import matplotlib.pyplot as plt

config = json.load(open('config.json'))

selections = {
    'ranking': selection_ranking,
    'tournament': selection_tournament,
    'roulette': selection_roulette
}


def get_loader_from_file(file_name):
    loader = NutritionDataLoader(file_name)
    loader.initial_preprocessing()
    return loader


def generate_initial_solutions(num_initial, loader: NutritionDataLoader):
    products_range = config['restrictions']['products_number']
    categories = config['categories']
    mass_range = config['mass_range']

    initial_solutions = []
    for _ in range(num_initial):
        products_number = randint(products_range[0], products_range[1])
        products = loader.generate_products(
            categories, [max(1, products_number // len(categories))] * len(categories)
        )

        solution = Solution()
        for product in products:
            solution.add(product, randint(mass_range[0], mass_range[1] // len(products)))

        initial_solutions.append(solution)
    return initial_solutions


def main():
    products_loader = get_loader_from_file(config['nutrition_data'])
    model = Model(products_loader, config['restrictions'])
    initial_improver = IterativeImprovementsAlgorithm(**config['iterative_improvement_config'])

    genetic_algorithm = GeneticAlgorithm(
        scoring_function=solution_score,
        unary_genetic_operation=mutate,
        binary_genetic_operation=cross,
        model=model,
        selection_algorithm=selections[config['selection_method']],
    )

    initial_population = initial_improver.correct_solutions(
        generate_initial_solutions(config['initial_solutions_number'], products_loader)
    )
    pickle.dump(initial_population, open('initial_population.pkl', 'w+b'))

    plot_title = "Selection Method: {}".format(config['selection_method'])
    plt.title(plot_title)
    evolved_population = genetic_algorithm.run_evolution(
        epoch_count=config['epoch_count'],
        scoring_params=config['scoring_params'],
        selection_params=config['selection_params'],
        unary_op_params=config['unary_op_params'],
        binary_op_params=config['binary_op_params'],
        initial_population=initial_population,
    )
    plt.show()
    pickle.dump(evolved_population, open('evolved_population.pkl', 'w+b'))


if __name__ == "__main__":
    main()
