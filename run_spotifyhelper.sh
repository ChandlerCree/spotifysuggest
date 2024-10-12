#!/bin/bash

# Activate the virtual environment
source spotify_venv/bin/activate

# Install the dependencies
pip3 install -r requirements.txt

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found"
    exit 1
fi

# Run the suggest_spotify.py script
python3 suggest_spotify.py

# Unset environment variables for security
if [ -f .env ]; then
    unset $(cat .env | sed -E 's/(.*)=.*/\1/' | xargs)
fi

# Deactivate the virtual environment
deactivate