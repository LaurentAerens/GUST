.',                      _   
       ,`/ _.' _.-                    | |  
       /  `---'         __ _ _   _ ___| |_ 
       \;/\            / _` | | | / __| __|
          \`.`        | (_| | |_| \__ \ |_ 
           \ `.`       \__, |\__,_|___/\__|
          / /   `.`     __/ |              
         /, / `,'      |___/               
         \\ \
          \\ \
    ejm    -`-'

# GUST - Genetic Universal Stockfish Trainer

## Overview
GUST is a framework designed to train neural network models for chess evaluation. It uses games against chess engines to evaluate the performance of models and applies genetic algorithms, including mutation and breeding, to evolve the networks over generations.

## Features

### Model Training
- Train neural network models to evaluate chess positions.
- Use games against chess engines to determine model performance.
- Support for Stockfish-compatible NNUE models.

### Genetic Algorithms
- **Mutation**: Modify neural network weights to introduce diversity.
- **Breeding**: Combine top-performing models to create new ones.
- **Selection**: Retain the best models based on performance.

### Tournament System
- Simulate games between neural networks and chess engines.
- Assign scores to models based on their performance in games.
- Progress models to harder engines as they improve.

## Project Structure
```
GUST/
├── engines/
│   ├── enginelist.csv          # List of chess engines with ELO and paths
│   ├── load_engine.py          # Functions to load and manage engines
│   └── executables/            # Folder for engine executables
├── neural_network/
│   ├── model.py                # Neural network architecture and utilities
│   ├── neural_network.py       # Population management and evolution
│   └── serialize.py            # Serialization for Stockfish-compatible models
├── tournaments/
│   └── tournament.py           # Tournament execution logic
├── main.py                     # Entry point for the framework
├── appsettings.json            # Configuration file for the framework
├── README.md                   # Project documentation
└── LICENSE                     # License file
```

## Getting Started

### Prerequisites
- Python 3.10 or higher.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Configuration
Edit the `appsettings.json` file to configure the framework:
```json
{
    "population_size": 100,
    "survival_rate": 0.4,
    "mutation_rate": 0.9,
    "temperature": 2.0,
    "decay_rate": 0.05,
    "level_up_threshold": 80,
    "base_nnue_path": "path/to/existing/nnue/model.nnue",
    "custom_hidden_layers": [64, 128, 64]
}
```

### Running the Framework
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/GUST.git
   cd GUST
   ```
2. Run the main script:
   ```bash
   python main.py
   ```

## How It Works

### Neural Network Evolution
1. **Population Generation**: Create a population of neural networks with randomized weights.
2. **Tournament Execution**: Each model competes against chess engines, and scores are assigned based on performance.
3. **Selection**: Top-performing models are selected for the next generation.
4. **Mutation and Breeding**: New models are created by mutating or breeding the top models.

### Tournament System
- Engines are loaded from [`engines/enginelist.csv`](engines/enginelist.csv).
- Games are played using the `chess` library, with moves evaluated by the neural network.
- Results are used to rank models and guide evolution.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

