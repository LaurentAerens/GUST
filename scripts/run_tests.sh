#!/bin/bash
# Script to run tests with coverage

echo "Running GUST test suite..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
pytest tests/ \
    --cov=src/gust \
    --cov-report=html \
    --cov-report=term \
    --cov-report=xml \
    -v

echo "Test run complete!"
echo "View coverage report: open htmlcov/index.html"
