#!/bin/bash
# Setup script for GUST development environment

echo "Setting up GUST development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in development mode
echo "Installing GUST in development mode..."
pip install -e .

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/training
mkdir -p data/models
mkdir -p data/results
mkdir -p logs

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env to configure your environment"
fi

echo "Setup complete!"
echo "Activate the virtual environment with: source venv/bin/activate"
