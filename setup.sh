#!/bin/bash

# DSim Card Setup Script
# This script prepares the application for systemd deployment

echo "Setting up DSim Card application..."

# Check if we're in the right directory
if [[ ! -f "run.py" ]]; then
    echo "Error: run.py not found. Please run this script from the application root directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [[ ! -d "venv" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [[ ! -f ".env" ]]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual configuration values!"
fi

# Set proper permissions
chmod +x manage_service.sh

echo ""
echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Ensure PostgreSQL is running and database is created"
echo "3. Run database migrations: source venv/bin/activate && python -m flask db upgrade"
echo "4. Install systemd service: ./manage_service.sh install"
echo "5. Start the service: ./manage_service.sh start"
echo ""
echo "Service management commands:"
echo "  ./manage_service.sh status   - Check service status"
echo "  ./manage_service.sh logs     - View service logs"
echo "  ./manage_service.sh restart  - Restart service"