#!/bin/bash
# run.sh - Development server script for the backend

set -e  # Exit on any error

echo "Starting RAG ChatBot Backend..."

# --- Activate virtual environment (Unix-like systems) ---
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Virtual environment not found. Run 'uv venv' first."
    exit 1
fi

# --- Ensure dependencies are installed ---
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found."
    exit 1
fi

echo "Installing dependencies..."
uv pip install -r requirements.txt

# --- Run the FastAPI server with reload for development ---
echo "Starting server on http://localhost:8000"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload