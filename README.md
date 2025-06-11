# Automated AI Newsletter-to-Podcast Generator

This project automates the process of converting your favorite email newsletters into an engaging, conversational podcast. It fetches all unread newsletters from a specific Gmail label, uses a Large Language Model (LLM) to write a cohesive two-host podcast script summarizing them, and then generates a high-quality audio file using Text-to-Speech (TTS).

The final output is a single MP3 file that sounds like two hosts discussing the key points from all your latest newsletters, perfect for listening on the go.

## Features

-   **Multi-Newsletter Aggregation:** Connects to your Gmail to find and combine all unread emails from a designated label (e.g., "Newsletters").
-   **Automated Content Extraction:** Parses HTML emails to extract clean, readable text content from multiple sources.
-   **AI-Powered Scriptwriting:** Feeds the combined newsletter content to Google's Gemini Pro to generate a natural, conversational script between two distinct host personas.
-   **High-Quality Audio Generation:** Uses the ElevenLabs API to generate distinct, lifelike voices for each host.
-   **Seamless Audio Production:** Programmatically combines the individual audio clips into a single, polished MP3 podcast file.
-   **Ready for Automation:** Designed to be run automatically on a schedule using tools like `cron`.
-   **Cost-Effective:** Built to run entirely within the generous free tiers of the required APIs for personal use.

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

1.  **Python 3.12:** The project is built and tested on Python 3.12.
2.  **A Gmail Label:** You must have a label created in your Gmail account for your newsletters (e.g., named "Newsletters").
3.  **Google Cloud Project:** A project with the **Gmail API** and **Generative Language API** enabled.
4.  **API Keys:**
    -   Google Gemini API Key.
    -   ElevenLabs API Key.
5.  **FFmpeg:** A command-line tool required by `pydub` to process audio files.

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

-   **On macOS (using Homebrew):** `brew install ffmpeg`
-   **On Debian/Ubuntu:** `sudo apt-get install ffmpeg`
-   **On Windows:** Download from the [official site](https://ffmpeg.org/download.html) and add the `bin` folder to your system's PATH.

### 5. Configure API Keys & Label ID

1.  **Get your Gmail Label ID:**
    -   Run the helper script: `python list_labels.py`
    -   Find your newsletter label in the output and copy its ID (e.g., `Label_2`).

2.  **Configure `gmail_reader.py`:**
    -   Open `gmail_reader.py` and paste your label ID into the `NEWSLETTER_LABEL_ID` variable.

3.  **Create your `.env` file:**
    -   Create a file named `.env` in the root of the project directory.
    -   Add your API keys to this file. **Do not commit this file to Git.**

    ```env
    # .env file
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY_HERE"
    ```

## How to Run Manually

1.  Make sure your virtual environment is activated (`source venv/bin/activate`).
2.  Run the main script:

    ```bash
    python main.py
    ```

3.  **First-Time Authorization:** The first time you run it, a browser window will open asking you to authorize access to your Gmail. Log in and grant permissions. A `token.json` file will be saved to handle future authentications.

4.  **Listen to Your Podcast:** Once the script finishes, you will find your generated audio file (e.g., `podcast_2024-06-11.mp3`) in the project directory.

## Automating with Cron (macOS/Linux)

To make this a truly set-and-forget system, you can schedule it to run automatically.

1.  **Find your absolute paths:**
    -   Activate your venv and run `which python` to get the full path to the Python interpreter.
    -   Navigate to your project folder and run `pwd` to get the full path to the project directory.

2.  **Open your crontab for editing:**
    ```bash
    crontab -e
    ```

3.  **Add the job:**
    Paste the following line at the end of the file, replacing the placeholder paths with your actual paths. This example runs the script daily at 8:00 AM and logs all output.

    ```cron
    # Run the Newsletter-to-Podcast script daily at 8 AM
    0 8 * * * /path/to/your/venv/bin/python /path/to/your/project/main.py >> /path/to/your/project/podcast_generator.log 2>&1
    ```

4.  **Save and exit** the editor. The job is now scheduled.
    *(Note: On modern macOS, you may need to grant "Full Disk Access" to `cron` in System Settings -> Privacy & Security).*

## Project Structure

```
.
├── .env                  # Stores secret API keys (ignored by Git)
├── .gitignore            # Specifies files to be ignored by Git
├── audio_generator.py    # Generates audio from the script using ElevenLabs
├── credentials.json      # Google OAuth credentials (ignored by Git)
├── gmail_reader.py       # Fetches and parses emails from Gmail by label
├── list_labels.py        # Helper script to find Gmail label IDs
├── main.py               # The main orchestrator script
├── requirements.txt      # List of Python dependencies
└── token.json            # Stores Gmail access token (ignored by Git)
```
