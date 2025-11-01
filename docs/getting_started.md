# Getting Started with GUST

## Introduction

This guide will help you get started with GUST (Genetic Universal Stockfish Trainer).

## Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- Stockfish chess engine installed
- Basic understanding of genetic algorithms (helpful but not required)
- Familiarity with command-line tools

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/LaurentAerens/GUST.git
cd GUST
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Step 4: Install Stockfish

Download and install Stockfish from the [official website](https://stockfishchess.org/download/).

Make note of the installation path, as you'll need it for configuration.

## Configuration

### Step 1: Create Environment File

```bash
cp .env.example .env
```

Edit `.env` and set your Stockfish path:
```
STOCKFISH_PATH=/path/to/your/stockfish
```

### Step 2: Review Configuration

Review `config/default_config.yaml` and adjust parameters as needed:
- Population size
- Number of generations
- Mutation/crossover rates
- Stockfish settings

## Running Your First Training Session

(Coming soon - will be added as code is implemented)

## Next Steps

- Read the [Architecture Documentation](architecture.md)
- Explore example scripts in `examples/`
- Check out the API documentation (when available)
- Join the community discussions

## Troubleshooting

### Common Issues

**Issue**: Import errors after installation
**Solution**: Ensure virtual environment is activated and packages are installed

**Issue**: Stockfish not found
**Solution**: Verify STOCKFISH_PATH in .env points to correct location

**Issue**: Permission errors
**Solution**: Ensure you have write permissions for data/ directory

## Getting Help

- Check existing [GitHub Issues](https://github.com/LaurentAerens/GUST/issues)
- Read the documentation in `docs/`
- Open a new issue if you encounter problems
