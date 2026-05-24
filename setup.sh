#!/bin/bash

# QR Contact App - Quick Start Script
# This script sets up the entire application

set -e

echo "🚀 QR Contact App - Setup Script"
echo "================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}✓ Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "   Python version: $PYTHON_VERSION"

# Create virtual environment
echo -e "${BLUE}✓ Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   Virtual environment created"
else
    echo "   Virtual environment already exists"
fi

# Activate virtual environment
echo -e "${BLUE}✓ Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}✓ Installing Python dependencies...${NC}"
cd backend
pip install -q -r requirements.txt
cd ..
echo "   Dependencies installed successfully"

# Create .env file if it doesn't exist
echo -e "${BLUE}✓ Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "   .env file created from .env.example"
    echo "   ⚠️  Please update .env with your settings, especially:"
    echo "      - MONGODB_URL (if not using local MongoDB)"
    echo "      - SECRET_KEY (change to a random string)"
else
    echo "   .env file already exists"
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Start MongoDB (if running locally)"
echo "2. Run: ./run.sh"
echo "   Or start components separately:"
echo "   - Backend: cd backend && python main.py"
echo "   - Frontend: cd frontend && python3 -m http.server 8001"
echo ""
