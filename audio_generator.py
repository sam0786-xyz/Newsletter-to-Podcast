# audio_generator.py
import io
import os
from dotenv import load_dotenv
from pydub import AudioSegment

from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found. Make sure it's in your .env file.")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def create_podcast_audio(script_content, output_path):
    script_lines = script_content.strip().split('\n')

    ALEX_VOICE_ID = 'pNInz6obpgDQGcFmaJgB'  # Adam - This one works!
    BEN_VOICE_ID = '21m00Tcm4TlvDq8ikWAM'   # Rachel - Swapped to a valid voice

    final_audio = AudioSegment.silent(duration=500)

    for line in script_lines:
        line = line.strip()
        if not line:
            continue

        audio_iterator = None

        if line.startswith("Alex:"):
            text = line.replace("Alex:", "").strip()
            print(f"Generating audio for Alex: {text}")
            audio_iterator = client.text_to_speech.convert(
                text=text,
                voice_id=ALEX_VOICE_ID,
                model_id="eleven_multilingual_v2"
            )

        elif line.startswith("Ben:"):
            text = line.replace("Ben:", "").strip()
            print(f"Generating audio for Ben: {text}")
            audio_iterator = client.text_to_speech.convert(
                text=text,
                voice_id=BEN_VOICE_ID,
                model_id="eleven_multilingual_v2"
            )

        if audio_iterator:
            full_audio_chunk = b"".join(audio_iterator)
            if full_audio_chunk:
                final_audio += AudioSegment.from_file(io.BytesIO(full_audio_chunk))
        else:
            final_audio += AudioSegment.silent(duration=750)

    print(f"\n--- Saving final audio to {output_path} ---")
    final_audio.export(output_path, format="mp3")