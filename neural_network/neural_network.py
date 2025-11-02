# Neural Network Integration
# This module will handle the integration of a neural network for evaluating chess positions.

from neural_network.model import generate_stockfish_nn, generate_nn_from_config
import torch
from torch import nn
import random
import os

class PopulationModel:
    """Class to represent a model in the population with its name, score, level, and metadata."""
    def __init__(self, model: nn.Module, name: str, score: float = 0.0, level: int = 0, metadata: dict = None, index: int = 0):
        self.model = model
        self.name = name
        self.score = score
        self.level = level  # Added level attribute
        self.index = index  # Added index attribute
        self.metadata = metadata or {}

def generate_population(population_size: int, custom_config_path: str = None):
    """Generate a population of neural networks with names, scores, and metadata.

    Args:
        population_size (int): The number of neural networks to generate.
        custom_config_path (str, optional): Path to a custom configuration file for generating custom networks.

    Returns:
        list: A list of PopulationModel instances.
    """
    population = []

    for i in range(1, population_size + 1):
        if custom_config_path:
            # Generate a custom NNUE model based on the provided configuration
            model = generate_nn_from_config(custom_config_path)
        else:
            # Generate a Stockfish-compatible NNUE model
            model = generate_stockfish_nn()

        # Randomize weights heavily for diversity
        for layer in model.model:
            if isinstance(layer, nn.Linear):
                layer.weight.data = torch.randn_like(layer.weight) * 0.1
                layer.bias.data = torch.randn_like(layer.bias) * 0.1

        # Assign a name and initialize score to 0.0
        name = f"model{i}"
        population.append(PopulationModel(model, name, score=0.0))

    return population


def generate_population_from_nnue(base_nnue_path: str, population_size: int):
    """Generate a population of neural networks starting from an existing NNUE file.

    Args:
        base_nnue_path (str): Path to the base NNUE file.
        population_size (int): The number of neural networks to generate.

    Returns:
        list: A list of PopulationModel instances.
    """
    from neural_network.model import NNUEModel

    # Load the base model
    base_model = NNUEModel.load_stockfish_format(base_nnue_path)
    population = []

    for i in range(1, population_size + 1):
        # Clone the base model
        model = NNUEModel(
            input_size=base_model.model[0].in_features,
            hidden_sizes=[layer.out_features for layer in base_model.model if isinstance(layer, nn.Linear)][:-1],
            output_size=base_model.model[-1].out_features,
        )
        model.load_state_dict(base_model.state_dict())

        # Apply slight modifications to the weights
        for layer in model.model:
            if isinstance(layer, nn.Linear):
                layer.weight.data += torch.randn_like(layer.weight) * 0.01
                layer.bias.data += torch.randn_like(layer.bias) * 0.01

        # Assign a name and initialize score to 0.0
        name = f"model{i}"
        metadata = {"parent": "base_nnue"}
        population.append(PopulationModel(model, name, score=0.0, metadata=metadata))

    return population

def create_new_generation(population: list[PopulationModel], survival_rate: float, mutation_rate: float, population_size: int, temperature: float, decay_rate: float, generation: int):
    """Create a new generation of models based on survival, mutation, and breeding.

    Args:
        population (list[PopulationModel]): The current population of models.
        survival_rate (float): The proportion of models that survive to the next generation unchanged.
        mutation_rate (float): The proportion of new models that are mutations of top models.
        population_size (int): The total size of the population.
        temperature (float): The temperature for mutation randomness.
        decay_rate (float): The rate at which survival rate and temperature decay.
        generation (int): The current generation number.

    Returns:
        list[PopulationModel]: The new generation of models.
    """
    from neural_network.model import mutate_model, breed_models

    # Sort population by score in descending order
    population.sort(key=lambda x: x.score, reverse=True)

    # Serialize the current population to files
    generation_folder = f"models/generation{generation}"
    os.makedirs(generation_folder, exist_ok=True)
    for model in population:
        model_path = os.path.join(generation_folder, f"{model.name}_{model.score:.2f}.nnue")
        model.model.save_stockfish_format(model_path)

    # Determine the number of survivors
    num_survivors = max(1, int(survival_rate * population_size))

    # Select survivors using the softmax-based selection function
    survivors = select_with_softmax(population, num_survivors)

    # Initialize the new generation with survivors
    new_generation = [PopulationModel(s.model, s.name, s.score, s.metadata) for s in survivors]

    # Fill the rest of the population
    while len(new_generation) < population_size:
        if random.random() < mutation_rate:
            # Select a top model to mutate using softmax-scaled probabilities
            top_models = select_with_softmax(population[:num_survivors], 1)
            parent = top_models[0]
            mutated_model = mutate_model(parent.model, temperature=temperature)

            # Generate a new name for the mutated model
            existing_names = {m.name for m in new_generation}
            mutation_count = parent.metadata.get("mutations", 0) + 1
            name = f"{parent.name}.{mutation_count}"

            # Ensure the name is unique
            while name in existing_names:
                mutation_count += 1
                name = f"{parent.name}.{mutation_count}"

            # Update metadata
            metadata = parent.metadata.copy()
            metadata["mutations"] = mutation_count

            new_generation.append(PopulationModel(mutated_model, name, score=0.0, metadata=metadata))
        else:
            # Select two top models to breed with weighted probability based on scores
            top_models = select_with_softmax(population[:num_survivors], 2)
            parent1, parent2 = top_models

            # Ensure the parent combination hasn't already bred
            existing_combinations = {(m.metadata.get("parents", [None, None])[0], m.metadata.get("parents", [None, None])[1]) for m in new_generation if "parents" in m.metadata}
            if (parent1.name, parent2.name) in existing_combinations or (parent2.name, parent1.name) in existing_combinations:
                continue

            child_model = breed_models(parent1.model, parent2.model)

            # Generate a new name for the child model
            name = f"{parent1.name}-{parent2.name}"

            # Update metadata
            metadata = {"parents": [parent1.name, parent2.name]}

            new_generation.append(PopulationModel(child_model, name, score=0.0, metadata=metadata))

    # Decay survival rate and temperature
    survival_rate = max(0.01, survival_rate * (1 - decay_rate))
    temperature = max(0.01, temperature * (1 - decay_rate))

    return new_generation, survival_rate, temperature

def select_with_softmax(population: list[PopulationModel], num_to_select: int) -> list[PopulationModel]:
    """Select unique models from the population using softmax-scaled probabilities.

    Args:
        population (list[PopulationModel]): The population of models to select from.
        num_to_select (int): The number of models to select.

    Returns:
        list[PopulationModel]: The selected models.
    """
    import math

    # Extract scores and compute softmax probabilities
    scores = [model.score for model in population]
    exp_scores = [math.exp(score) for score in scores]
    total = sum(exp_scores)
    probabilities = [exp_score / total for exp_score in exp_scores]

    # Select unique models based on probabilities
    selected = set()
    while len(selected) < num_to_select:
        chosen = random.choices(population, weights=probabilities, k=1)[0]
        if chosen not in selected:
            selected.add(chosen)

    return list(selected)

def load_population_from_folder(folder_path: str) -> list[PopulationModel]:
    """Load a population of models from a folder.

    Args:
        folder_path (str): Path to the folder containing serialized models.

    Returns:
        list[PopulationModel]: The loaded population of models.
    """
    from neural_network.model import NNUEModel

    population = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".nnue"):
            file_path = os.path.join(folder_path, file_name)
            model = NNUEModel.load_stockfish_format(file_path)

            # Extract name and score from the file name
            base_name = os.path.splitext(file_name)[0]
            name, score = base_name.rsplit("_", 1)
            population.append(PopulationModel(model, name, score=float(score)))

    return population

# Example usage:
# stockfish_population = generate_population(10)
# custom_population = generate_population(10, "path/to/custom_config.json")
# nnue_population = generate_population_from_nnue("path/to/base.nnue", 10)