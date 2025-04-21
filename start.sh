#!/bin/bash

# Load environment variables
source .env 2>/dev/null || true

# Set default port if not specified
PORT=${PORT:-12000}

echo "Starting News Agent on port $PORT..."
echo "Access the application at http://localhost:$PORT"

# Run the application
python run.py