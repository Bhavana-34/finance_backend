#!/bin/bash

# Finance Backend Startup Script for macOS/Linux

echo ""
echo "====================================="
echo "  Finance Dashboard Backend"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements (if needed)
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Start the server
echo ""
echo "Starting FastAPI server on http://localhost:8000"
echo ""
echo "Documentation available at:"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
