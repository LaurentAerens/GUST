# GUST Architecture

## Overview

GUST follows a modular architecture with clear separation of concerns between genetic algorithm logic, training orchestration, and evaluation components.

## Core Components

### 1. Genetic Algorithm Module (`src/gust/genetic/`)

Handles the evolutionary computation aspects:
- **Population Management**: Initialize and maintain population of candidate solutions
- **Selection**: Tournament, roulette, and rank-based selection strategies
- **Crossover**: Combine parent solutions to create offspring
- **Mutation**: Introduce random variations for exploration
- **Fitness Evaluation**: Assess candidate solution quality

### 2. Trainer Module (`src/gust/trainer/`)

Orchestrates the training process:
- **Training Loop**: Manage generation iterations
- **Checkpoint Management**: Save and restore training state
- **Progress Tracking**: Monitor and log training metrics
- **Resource Management**: Handle compute resources efficiently

### 3. Evaluator Module (`src/gust/evaluator/`)

Evaluates Stockfish configurations:
- **Game Simulation**: Run chess games with different parameters
- **Performance Metrics**: Calculate ELO ratings and win rates
- **Benchmarking**: Compare against baseline configurations
- **Statistical Analysis**: Provide confidence intervals and significance tests

### 4. Utilities Module (`src/gust/utils/`)

Shared functionality:
- **Configuration Loading**: Parse YAML/JSON configs
- **Logging**: Structured logging utilities
- **Data I/O**: File operations and data persistence
- **Visualization**: Plot training progress and results

### 5. API Module (`src/gust/api/`)

REST API interface (planned):
- **Endpoints**: CRUD operations for training sessions
- **WebSocket**: Real-time training updates
- **Authentication**: API key management
- **Documentation**: OpenAPI/Swagger docs

### 6. GUI Module (`src/gust/gui/`)

Graphical interface (planned):
- **Dashboard**: Training overview and statistics
- **Configuration**: Visual parameter editing
- **Visualization**: Real-time charts and graphs
- **Control Panel**: Start/stop training sessions

## Data Flow

```
Configuration → Genetic Algorithm → Trainer → Evaluator → Results
                       ↑                                      ↓
                       └──────────── Fitness Score ←─────────┘
```

## Technology Stack

- **Core**: Python 3.8+
- **Numerical Computing**: NumPy, Pandas
- **Testing**: pytest, pytest-cov
- **Code Quality**: Black, flake8, mypy
- **Configuration**: YAML, python-dotenv
- **API** (planned): FastAPI, Uvicorn
- **GUI** (planned): TBD (tkinter, PyQt, or Streamlit)

## Design Principles

1. **Modularity**: Each component is independent and loosely coupled
2. **Testability**: All components have comprehensive unit tests
3. **Configurability**: Behavior controlled through configuration files
4. **Extensibility**: Easy to add new selection/crossover/mutation strategies
5. **Performance**: Optimized for long-running training sessions
