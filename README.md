# Newsletter-to-Podcast Generator

This project automates the process of converting your favorite email newsletters into an engaging, conversational podcast. It fetches unread newsletters from your Gmail, uses a Large Language Model (LLM) to write a two-host podcast script, and then generates a high-quality audio file using Text-to-Speech (TTS).

The final output is an MP3 file that sounds like two hosts discussing the key points of the newsletter, perfect for listening on the go.

## Features

-   **Gmail Integration:** Securely connects to your Gmail account to find specific unread newsletters.
-   **Automated Content Extraction:** Parses HTML emails to extract clean, readable text content.
-   **AI-Powered Scriptwriting:** Feeds the newsletter content to Google's Gemini Pro to generate a natural, conversational script between two distinct host personas (Alex, the curious host, and Ben, the pragmatic host).
-   **High-Quality Audio Generation:** Uses ElevenLabs' API to generate distinct, lifelike voices for each host.
-   **Audio Stitching:** Combines the individual audio clips into a single, seamless MP3 podcast file.
-   **Cost-Effective:** Designed to run entirely within the generous free tiers of the required APIs.

## Tech Stack

-   **Language:** Python 3.12
-   **APIs & Services:**
    -   **Email:** Google Gmail API
    -   **LLM (Scripting):** Google Gemini API
    -   **TTS (Audio):** ElevenLabs API
-   **Key Python Libraries:**
    -   `google-api-python-client` & `google-auth-oauthlib` for Gmail access.
    -   `google-generativeai` for the Gemini LLM.
    -   `elevenlabs` for text-to-speech.
    -   `pydub` for audio manipulation.
    -   `python-dotenv` for managing API keys.
    -   `beautifulsoup4` for HTML parsing.

## Prerequisites

Before you can run this project, you need a few things:

1.  **Python 3.12:** The project is built and tested on Python 3.12. Using other versions may cause dependency issues.
2.  **Google Cloud Project:** A project with the **Gmail API** and **Generative Language API** enabled.
3.  **API Keys:**
    -   Google Gemini API Key.
    -   ElevenLabs API Key.
4.  **FFmpeg:** A command-line tool required by `pydub` to process audio files.

## Setup & Installation

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Newsletter-to-Podcast.git
cd Newsletter-to-Podcast
```

### 2. Set Up Google Cloud Credentials

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2.  Enable the **Gmail API** and the **Generative Language API** in the "Library" section.
3.  Go to "OAuth consent screen", choose "External", and add your own Google account as a "Test user".
4.  Go to "Credentials", create an "OAuth 2.0 Client ID" for a "Desktop app", and download the `credentials.json` file.
5.  **Place the `credentials.json` file in the root of the project directory.**

### 3. Install Dependencies

It's highly recommended to use a virtual environment.

```bash
# Create a virtual environment using Python 3.12
python3.12 -m venv venv

# Activate it
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

### 4. Install FFmpeg

`pydub` needs FFmpeg to work with MP3 files.

-   **On macOS (using Homebrew):**
    ```bash
    brew install ffmpeg
    ```
-   **On Debian/Ubuntu:**
    ```bash
    sudo apt-get install ffmpeg
    ```
-   **On Windows:**
    Download from the [official site](https://ffmpeg.org/download.html) and add the `bin` folder to your system's PATH.

### 5. Configure API Keys

1.  Create a file named `.env` in the root of the project directory.
2.  Add your API keys to this file. **Do not commit this file to Git.**

    ```env
    # .env file
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY_HERE"
    ```

## How to Run

1.  **Customize the Newsletter Query:**
    Open `gmail_reader.py` and modify the `q` parameter in the `service.users().messages().list()` call to match the sender of the newsletter you want to process.

    ```python
    # gmail_reader.py
    results = service.users().messages().list(
        userId='me',
        # Change this query to find your newsletter
        q='from:(newsletter@example.com) is:unread', 
        maxResults=1
    ).execute()
    ```

2.  **Run the Main Script:**
    Make sure your virtual environment is activated, then run:

    ```bash
    python main.py
    ```

3.  **First-Time Authorization:**
    The first time you run the script, a browser window will open asking you to authorize access to your Gmail account. Log in and grant the permissions. The script will save a `token.json` file to handle future authentications automatically.

4.  **Listen to Your Podcast:**
    Once the script finishes, you will find your generated audio file named `newsletter_podcast.mp3` in the project directory.

## Project Structure

```
.
├── .env                  # Stores secret API keys (ignored by Git)
├── .gitignore            # Specifies files to be ignored by Git
├── audio_generator.py    # Generates audio from the script using ElevenLabs
├── credentials.json      # Google OAuth credentials (ignored by Git)
├── gmail_reader.py       # Fetches and parses emails from Gmail
├── main.py               # The main orchestrator script
├── newsletter_podcast.mp3 # Example output file (ignored by Git)
├── README.md             # This file
├── requirements.txt      # List of Python dependencies
├── script_generator.py   # Generates a podcast script using Gemini
└── token.json            # Stores Gmail access token (ignored by Git)
```

## Future Improvements

-   Process multiple newsletters in a single run.
-   Add background music or intro/outro jingles.
-   Deploy as a cloud function to run automatically on a schedule (e.g., daily).
-   Create a simple web interface to trigger the process and download the audio.