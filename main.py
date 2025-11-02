import sys
import os
from concurrent.futures import ThreadPoolExecutor

import chess
import chess.engine
from engines.load_engine import (
    load_engine, 
    sort_engines_by_elo, 
    load_engine_by_index, 
    get_max_index, 
    get_engine_elo, 
    get_engine_info_by_index
)
import tournaments.tournament as tournament
import random
from neural_network.model import generate_stockfish_nn
import json
from neural_network.neural_network import create_new_generation, load_population_from_folder, PopulationModel
from neural_network.neural_network import generate_population_from_nnue
from neural_network.model import generate_nn_from_config



def main():
    print("""
              .',                      _   
       ,`/ _.' _.-                    | |  
       /  `---'         __ _ _   _ ___| |_ 
       \;/\            / _` | | | / __| __|
          \`.`        | (_| | |_| \__ \ |_ 
           \ `.`       \__, |\__,_|___/\__|
          / /   `.`     __/ |              
         /, / `,'      |___/               
         \\\\ \\
          \\\\ \\
    ejm    -`-'""")
    print("Welcome to GUST - Genetic Universal Stockfish Trainer")

    # Load settings from appsettings.json
    with open("appsettings.json", "r") as settings_file:
        settings = json.load(settings_file)

    population_size = settings["population_size"]
    survival_rate = settings["survival_rate"]
    mutation_rate = settings["mutation_rate"]
    temperature = settings["temperature"]
    decay_rate = settings["decay_rate"]
    generation = 0
    current_level = 0

    # Load initial population or generate a new one
    try:
        population = load_population_from_folder(f"models/generation{generation}")
        print(f"Loaded population from generation {generation}.")
    except FileNotFoundError:
        print("No existing population found. Generating a new one.")
        
        # Check if starting from an existing NNUE model
        if settings.get("base_nnue_path"):
            print("Generating population from existing NNUE model...")
            population = generate_population_from_nnue(settings["base_nnue_path"], population_size)
        # Check if using custom hidden layers
        elif settings.get("custom_hidden_layers"):
            print("Generating population with custom hidden layers...")
            custom_hidden_layers = settings["custom_hidden_layers"]
            population = [
                PopulationModel(
                    generate_nn_from_config({"hidden_layers": custom_hidden_layers}),
                    f"model{i}",
                    score=0.0
                )
                for i in range(1, population_size + 1)
            ]
        else:
            print("Generating population with default Stockfish-compatible architecture...")
            population = [
                PopulationModel(generate_stockfish_nn(), f"model{i}", score=0.0)
                for i in range(1, population_size + 1)
            ]

    max_generations = settings.get("max_generations", 100)  # Default to 100 generations if not specified
    stagnation_limit = settings.get("stagnation_limit", 10)  # Default to 10 generations if not specified
    stagnation_counter = 0
    previous_total_score = float("-inf")
    last_level_up_generation = -1

    while generation < max_generations:
        print(f"Starting tournament for generation {generation}...")
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(
                lambda model: tournament.run_tournament(model.name, generation, model.model, debug=False),
                population
            ))

        for model, (score, level) in zip(population, results):
            model.score = score
            model.level = level

        # Calculate the total score of the current generation
        current_total_score = sum(model.score for model in population)
        print(f"Total score for generation {generation}: {current_total_score:.2f}")

        # Check for stagnation
        if current_total_score <= previous_total_score and generation - last_level_up_generation > stagnation_limit:
            stagnation_counter += 1
            print(f"No improvement detected. Stagnation counter: {stagnation_counter}")
        else:
            stagnation_counter = 0
            print("Improvement detected or recent level-up. Resetting stagnation counter.")

        previous_total_score = current_total_score

        if stagnation_counter >= stagnation_limit:
            print("Stagnation limit reached. Stopping training.")
            break

        # Check if max generations reached
        if generation >= max_generations:
            print("Maximum generations reached. Stopping training.")
            break

        # Check if any model has beaten all engines
        max_engine_score = get_max_index() * 20
        best_model = max(population, key=lambda m: m.score)
        if best_model.score >= max_engine_score:
            print(f"Model {best_model.name} has beaten all engines. Stopping training.")
            break

        # Check if level-up condition is met
        level_up_threshold = settings.get("level_up_threshold", 5)
        new_level = level_up(population, current_level, level_up_threshold)
        if new_level > current_level:
            last_level_up_generation = generation
            print(f"Level-up detected! New level: {new_level}")
        current_level = new_level

        print("Creating new generation...")
        population, survival_rate, temperature = create_new_generation(
            population, survival_rate, mutation_rate, population_size, temperature, decay_rate, generation
        )
        generation += 1

    print("Training stopped.")
def level_up(population, current_level, level_up_threshold):
    """Check if the level-up condition is met based on the population's performance.

    Args:
        population (list): List of PopulationModel instances.
        current_level (int): The current level of the models.
        level_up_threshold (float): The threshold ratio for leveling up.
    Returns:
        int : the new level
    """
    # count of nn were index is higher then the current level
    level_up_count = sum(1 for model in population if model.index >= current_level + 1)
    if level_up_count / len(population) >= level_up_threshold:
        new_level = current_level + 1
        return level_up(population, new_level, level_up_threshold)
    return current_level
if __name__ == "__main__":
    main()