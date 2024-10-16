#!/bin/bash


# Set the project directory to the current working directory
export SPOTIFY_PROJECT_DIR="$(pwd)"

# Check if we're running in GitHub Actions
if [ -n "$GITHUB_ACTIONS" ]; then
    # We're in GitHub Actions, so we don't need to activate a virtual environment
    # or load the .env file (we use secrets instead)
    python3 suggest_spotify.py
else

    # Check if the virtual environment already exists
    if [ ! -d "spotify_venv" ]; then
        python3 -m venv spotify_venv
        echo "Virtual environment created."
    else
        echo "Virtual environment already exists."
    fi

    # Make the virtual environment executable
    chmod +x spotify_venv/bin/activate

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
fi

# Unset the project directory environment variable
unset SPOTIFY_PROJECT_DIR
