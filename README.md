# Spotify Suggestion Script Setup

This README provides instructions on how to set up and run the Spotify suggestion script.

## Prerequisites

- Python 3.12.7
- Spotify Developer Account

## 1. Setting up Spotify Developer Dashboard

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Log in with your Spotify account or create a new one.
3. Click on "Create an App".
4. Fill in the app name and description, then click "Create".
5. In your new app's dashboard, click on "Edit Settings".
6. Add `http://localhost:8888/callback` to the Redirect URIs and save.
7. Note down your Client ID and Client Secret (you'll need these later).

## 2. Installing Python 3.12.7

### Windows

1. Download the Python 3.12.7 installer from the [official Python website](https://www.python.org/downloads/release/python-3127/).
2. Run the installer. Make sure to check "Add Python 3.12 to PATH".
3. Follow the installation wizard to complete the setup.

### macOS

1. Install Homebrew if you haven't already:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python 3.12.7:
   ```
   brew install python@3.12
   ```

### Linux (Ubuntu/Debian)

1. Update package list:
   ```
   sudo apt update
   ```
2. Install required dependencies:
   ```
   sudo apt install software-properties-common
   ```
3. Add deadsnakes PPA:
   ```
   sudo add-apt-repository ppa:deadsnakes/ppa
   ```
4. Install Python 3.12.7:
   ```
   sudo apt install python3.12
   ```

## 3. Setting Up the Project

1. Clone or download this repository to your local machine.
2. Navigate to the project directory in your terminal or command prompt.

## 4. Setting Up Environment Variables

1. In your project directory, create a file named `.env`.
2. Add your Spotify API credentials to this file:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```
3. Replace `your_client_id_here` and `your_client_secret_here` with your actual Spotify API credentials.

## 5. Creating a Virtual Environment

The `run_spotifyhelper.sh` script will handle creating and activating the virtual environment for you. However, if you need to create it manually:

### Windows

1. Open Command Prompt.
2. Navigate to your project directory.
3. Create a virtual environment:
   ```
   python -m venv spotify_venv
   ```

### macOS and Linux

1. Open Terminal.
2. Navigate to your project directory.
3. Create a virtual environment:
   ```
   python3 -m venv spotify_venv
   ```

## 6. Running the Script

To run the script, simply execute the `run_spotifyhelper.sh` file:

```
./run_spotifyhelper.sh
```

This script will:
1. Activate the virtual environment
2. Install the required packages from `requirements.txt`
3. Run the `suggest_spotify.py` script

If you're on Windows or prefer to run the steps manually:

1. Activate the virtual environment:
   - Windows: `spotify_venv\Scripts\activate`
   - macOS/Linux: `source spotify_venv/bin/activate`
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the script:
   ```
   python suggest_spotify.py
   ```

## Project Structure

- `suggest_spotify.py`: The main script for generating Spotify suggestions.
- `run_spotifyhelper.sh`: Shell script to set up the environment and run the main script.
- `requirements.txt`: List of Python packages required for the project.
- `.env`: File containing your Spotify API credentials (you need to create this).

## Troubleshooting

If you encounter any issues, ensure that:
- You're using Python 3.12.7
- Your `.env` file is in the correct location and contains valid credentials
- You have necessary permissions to execute the shell script

For any other problems, please check the error message and consult the Spotify API documentation or seek help in the project's issue tracker.
