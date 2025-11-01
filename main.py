import sys
import os

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

    while True:
        print(f"Starting tournament for generation {generation}...")
        for model in population:
            score, level = tournament.run_tournament(model.name, generation, model.model, debug=False)
            model.score = score
            model.level = level

        # Check if level-up condition is met
        level_up_threshold = settings.get("level_up_threshold", 5)
        current_level = level_up(population, current_level, level_up_threshold)

        print("Creating new generation...")
        population, survival_rate, temperature = create_new_generation(
            population, survival_rate, mutation_rate, population_size, temperature, decay_rate, generation
        )
        generation += 1
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