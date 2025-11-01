#!/bin/bash
# Script to run code quality checks

echo "Running code quality checks..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Running Black formatter..."
black --check src/ tests/

echo "Running flake8 linter..."
flake8 src/ tests/ --max-line-length=100

echo "Running isort import checker..."
isort --check-only src/ tests/

echo "Running mypy type checker..."
mypy src/

echo "Code quality checks complete!"
