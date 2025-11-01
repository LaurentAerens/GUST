# GUST - Genetic Universal Stockfish Trainer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An AI-powered project for optimizing Stockfish chess engine parameters using genetic algorithms.

## Overview

GUST (Genetic Universal Stockfish Trainer) is a Python-based framework designed to automatically tune and optimize Stockfish chess engine parameters through evolutionary algorithms. The project aims to discover optimal configurations for various chess scenarios and playing styles.

### Key Features

- **Genetic Algorithm Optimization**: Evolve Stockfish parameters using sophisticated genetic algorithms
- **Automated Training**: Run long-term training sessions with automatic checkpointing
- **Performance Evaluation**: Comprehensive benchmarking and ELO rating calculations
- **REST API**: (Planned) HTTP API for remote training and monitoring
- **GUI Interface**: (Planned) User-friendly interface for configuration and visualization
- **Extensible Architecture**: Modular design for easy customization and extension

## Project Structure

```
GUST/
├── src/gust/           # Main source code
│   ├── genetic/        # Genetic algorithm implementation
│   ├── trainer/        # Training orchestration
│   ├── evaluator/      # Performance evaluation
│   ├── utils/          # Utility functions
│   ├── api/            # REST API (planned)
│   └── gui/            # GUI interface (planned)
├── tests/              # Test suite
│   ├── unit/          # Unit tests
│   └── integration/   # Integration tests
├── docs/              # Documentation
├── config/            # Configuration files
├── scripts/           # Utility scripts
├── data/              # Data storage
│   ├── training/      # Training data
│   ├── models/        # Saved models
│   └── results/       # Results and logs
└── examples/          # Example scripts and notebooks
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Stockfish chess engine (will need to be installed separately)
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/LaurentAerens/GUST.git
cd GUST
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install in development mode:
```bash
pip install -e .
```

## Usage

### Basic Usage (Coming Soon)

```python
from gust import GeneticTrainer, StockfishEvaluator

# Initialize trainer
trainer = GeneticTrainer(config_path="config/default_config.yaml")

# Run training
trainer.train(generations=100)

# Evaluate results
evaluator = StockfishEvaluator()
results = evaluator.evaluate(trainer.best_individual)
```

### Configuration

Edit `config/default_config.yaml` to customize training parameters:

```yaml
genetic:
  population_size: 50
  generations: 100
  mutation_rate: 0.01
  crossover_rate: 0.7
```

See the configuration file for all available options.

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/gust --cov-report=html

# Run specific test file
pytest tests/unit/test_genetic.py
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [x] Project structure setup
- [ ] Core genetic algorithm implementation
- [ ] Stockfish integration
- [ ] Training pipeline
- [ ] Evaluation framework
- [ ] REST API
- [ ] GUI interface
- [ ] Documentation
- [ ] Example notebooks
- [ ] Performance optimization

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Stockfish chess engine team for their incredible open-source chess engine
- The chess programming community for inspiration and resources

## Contact

Laurent Aerens - Project Maintainer

Project Link: [https://github.com/LaurentAerens/GUST](https://github.com/LaurentAerens/GUST)

---

**Note**: This project is in early development. The API and functionality are subject to change.