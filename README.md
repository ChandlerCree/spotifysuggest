<div id="readme-top"></div>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPLv3][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h2 align="center">Spotify Suggest</h2>

  <p align="center">
    Created by: Chandler Cree
    <br />
    <a href="https://github.com/ChandlerCree/spotifysuggest">View Demo</a>
    ·
    <a href="https://github.com/ChandlerCree/spotifysuggest/issues">Report Bug</a>
    ·
    <a href="https://github.com/ChandlerCree/spotifysuggest/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#structure">Structure</a></li>
    <li><a href="#tasks">Tasks</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## Problem Statement

Provide a better recommendation system based off of user liked songs and artists.

## About The Project

This is very early stages of the project. Open to contributor. Currently this README is also a wkr in progress. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

The main library used in this project is Spotipy. A library that can be installed using pip.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Prerequisites

- Python 3.12.7
- Spotify Developer Account
- OpenAI Account (Can be skipped)
- Spotify Authorization Token

## 1. Setting up Spotify Developer Dashboard

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Log in with your Spotify account or create a new one.
3. Click on "Create an App".
4. Fill in the app name and description, then click "Create".
5. In your new app's dashboard, click on "Edit Settings".
6. Add `http://localhost:8888/callback` to the Redirect URIs and save.
7. Note down your Client ID and Client Secret (you'll need these later).

## 2. Setting up OpenAI Account

1. Go to the [OpenAI website](https://openai.com/) and sign up for an account.
2. Once logged in, navigate to the [API keys page](https://platform.openai.com/account/api-keys).
3. Create a new secret key and save it securely (you'll need this later).
4. Set up billing for your OpenAI account to ensure API access.

## 3. Installing Python 3.12.7

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

## 4. Setting Up the Project

1. Clone or download this repository to your local machine.
2. Navigate to the project directory in your terminal or command prompt.

## 5. Setting Up Environment Variables

1. In your project directory, create a file named `.env`.
2. Add your Spotify API and OpenAI API credentials to this file:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id_here
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
   # OPENAI_API_KEY=your_openai_api_key_here #uncomment if you have a key
   SPOTIFY_REFRESH_TOKEN=your_spotify_refresh_token_here
   
   ```
3. Replace the placeholder values with your actual credentials.
	1. Note this is file with private contents and you should add it to your .gitignore.

## 6. Creating a Virtual Environment

The `run_spotifyhelper.sh` script will handle creating and activating the virtual environment for you. However, if you need to create it manually:

### Windows

1. Open Command Prompt.
2. Navigate to your project directory.
3. Create a virtual environment:
	1. Note the current configuration requires the env to be named "spotify_venv".
   ```
   python -m venv spotify_venv
   ```

### macOS and Linux

1. Open Terminal.
2. Navigate to your project directory.
3. Create a virtual environment:
	1. Note the current configuration requires the env to be named "spotify_venv".
   ```
   python3 -m venv spotify_venv
   ```

## 7. Obtain Spotify Refresh Token:

   a. Run the helper script:
      ```
      ./run_refreshtokenhelper.sh
      ```

   b. Follow the prompts:
      - Visit the provided URL in your browser
      - Authorize the application
      - Copy the URL you're redirected to

   c. Paste the redirected URL when prompted in the terminal

   d. Copy the refresh token from the output

   e. Add the refresh token to your `.env` file:
      ```
      SPOTIFY_REFRESH_TOKEN=your_refresh_token_here
      ```
## 8. Running the Script

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

- `suggest_spotify.py`: The main script for generating Spotify suggestions and creating a playlist with an AI-generated description.
- `run_spotifyhelper.sh`: Shell script to set up the environment and run the main script.
- `requirements.txt`: List of Python packages required for the project.

- `.env`: File containing your Spotify and OpenAI API credentials (you need to create this).

- `run_refreshtokenhelper.sh`: Shell script to activate the virtual environment and run the refresh token script.

- `get_refresh_token.py`: Python script to obtain a refresh token from Spotify.

- `README.md`: Documentation file providing setup instructions and project information.

- `LICENSE.txt`: Contains the GNU General Public License version 3.0 (GPLv3) for the project.

## How It Works

This script does the following:

1. Fetches your top tracks, recently played tracks, and top artists from Spotify.
2. Uses this data to get recommendations for new tracks.
3. Creates a new playlist with these recommended tracks.
4. Uses OpenAI's GPT model to analyze your music preferences and generate a description for the playlist. (If OpenAI is linked)
5. Sets the AI-generated description as the playlist description on Spotify.
6. Saves all this information to a markdown file for your reference.

## OpenAI Integration

The script uses OpenAI's GPT model to analyze your music preferences based on your top tracks, recently played tracks, and top artists. It then generates a brief, human-like description of the playlist and what the recommended songs have in common. This description is used as the playlist description on Spotify, providing a personalized touch to your auto-generated playlist.

## Troubleshooting

If you encounter any issues, ensure that:
- You're using Python 3.12.7
- Your `.env` file is in the correct location and contains valid credentials for both Spotify and OpenAI
- You have necessary permissions to execute the shell script
- Your OpenAI account has active billing set up to use the API

For any other problems, please check the error message and consult the Spotify API or OpenAI API documentation, or seek help in the project's issue tracker.

## Note on API Usage

Be aware that using the OpenAI API incurs costs based on your usage. Make sure to review OpenAI's pricing structure and set up appropriate usage limits in your OpenAI account settings to avoid unexpected charges.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

TBD.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- STRUCTURE -->
## Structure

*TBD.*
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TASKS -->
## Tasks

By publicly displaying the to-do list of the project, users are able to see any feature that is nearing implementation. The list also allows new developers to quickly find potential tasks for them to complete which is an ideal way to familiarize them with the source code and to continue to make commits.

- [ ] TBD

See the [open issues](https://github.com/ChandlerCree/suggestspotify/issues) for a full list of issues and proposed features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are open and requested. Please take advantage of the open source code and 

1. [Fork the Project](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
2. Create your Feature Branch (`git checkout -b f/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin f/AmazingFeature`)
5. [Open a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

*Documentation must include a license section in which the type of license and a link or reference to the full license in the repository is given.*

Distributed under the GPL-3.0 license . See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Michael Montanaro - [LinkedIn](https://www.linkedin.com/in/chandlercree/) - chandlercreegk@gmail.com

Project Link: [https://github.com/ChandlerCree/spotifysuggest](https://github.com/ChandlerCree/spotifysuggest)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list any resources used or that may be helpful in understanding the project

* [Spotify Developer](https://developer.spotify.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ChandlerCree/suggestspotify.svg?style=for-the-badge
[contributors-url]: https://github.com/ChandlerCree/suggestspotify/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ChandlerCree/suggestspotify.svg?style=for-the-badge
[forks-url]: https://github.com/ChandlerCree/suggestspotify/network/members
[stars-shield]: https://img.shields.io/github/stars/ChandlerCree/suggestspotify.svg?style=for-the-badge
[stars-url]: https://github.com/ChandlerCree/suggestspotify/stargazers
[issues-shield]: https://img.shields.io/github/issues/ChandlerCree/suggestspotify.svg?style=for-the-badge
[issues-url]: https://github.com/ChandlerCree/suggestspotify/issues
[license-shield]: https://img.shields.io/github/license/ChandlerCree/suggestspotify.svg?style=for-the-badge
[license-url]: https://github.com/ChandlerCree/suggestspotify/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
