#!/bin/bash

# Activate the virtual environment
source spotify_venv/bin/activate

# Run the Python script
python get_refresh_token.py

# Deactivate the virtual environment
deactivate