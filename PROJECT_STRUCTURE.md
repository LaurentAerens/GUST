# GUST Project Structure

This document provides an overview of the GUST project structure created for development.

## Directory Structure

```
GUST/
├── src/gust/              # Main source code
│   ├── __init__.py       # Package initialization
│   ├── __main__.py       # CLI entry point
│   ├── genetic/          # Genetic algorithm module
│   ├── trainer/          # Training orchestration
│   ├── evaluator/        # Performance evaluation
│   ├── utils/            # Utility functions
│   ├── api/              # REST API (planned)
│   └── gui/              # GUI interface (planned)
│
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
│
├── docs/                  # Documentation
│   ├── README.md         # Documentation index
│   ├── architecture.md   # Architecture documentation
│   └── getting_started.md # Getting started guide
│
├── config/                # Configuration files
│   └── default_config.yaml # Default configuration
│
├── scripts/               # Utility scripts
│   ├── setup_environment.sh # Environment setup
│   ├── run_tests.sh        # Test runner
│   └── lint.sh             # Code quality checks
│
├── data/                  # Data storage (gitignored)
│   ├── training/         # Training data
│   ├── models/           # Saved models
│   └── results/          # Results and logs
│
├── examples/              # Example scripts
│   └── basic_usage.py    # Basic usage example
│
└── logs/                  # Application logs (gitignored)

## Configuration Files

- **setup.py**: Package installation and metadata
- **pyproject.toml**: Modern Python packaging config and tool settings
- **requirements.txt**: Core dependencies
- **requirements-dev.txt**: Development dependencies
- **.flake8**: Flake8 linter configuration
- **.env.example**: Environment variables template
- **.gitignore**: Git ignore patterns
- **CHANGELOG.md**: Project changelog
- **CONTRIBUTING.md**: Contribution guidelines

## Key Features

1. **Modular Architecture**: Clear separation between genetic algorithm, training, and evaluation
2. **Test Infrastructure**: Unit and integration test directories
3. **Documentation**: Comprehensive docs for getting started and understanding architecture
4. **Code Quality**: Pre-configured linting and formatting tools
5. **Extensible Design**: Easy to add new modules and features
6. **Development Tools**: Scripts for common development tasks

## Getting Started

See [docs/getting_started.md](docs/getting_started.md) for detailed setup instructions.

Quick start:
```bash
# Run setup script
bash scripts/setup_environment.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Next Steps

The structure is ready for development. The next phase would be to:
1. Implement core genetic algorithm components
2. Add Stockfish integration
3. Build training pipeline
4. Create evaluation framework
5. Add REST API
6. Develop GUI interface

All module placeholders are in place with descriptive docstrings indicating their purpose.
