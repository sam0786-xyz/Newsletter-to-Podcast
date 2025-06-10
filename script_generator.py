# script_generator.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Correctly loads the key from the .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Make sure it's in your .env file.")
genai.configure(api_key=GEMINI_API_KEY)

def generate_podcast_script(content):
    model = genai.GenerativeModel('gemini-1.5-flash')
    # ... (rest of your prompt is perfect, no changes needed)
    prompt = """
    Your Role: You are a scriptwriter for a short, engaging podcast. The podcast has two hosts:
    - Alex: The insightful and curious host. Alex loves digging into the details and asking "why".
    - Ben: The pragmatic and slightly skeptical host. Ben focuses on the real-world implications and the "so what?".

    Your Task: Read the following newsletter content and write a 3-minute conversational script between Alex and Ben.
    
    Script Guidelines:
    - Start with a brief, friendly introduction.
    - Discuss the 2-3 most interesting points from the newsletter.
    - Have Alex and Ben offer their different perspectives.
    - Ensure the conversation flows naturally.
    - End with a quick summary.
    - Format the script clearly, with each line starting with "Alex: " or "Ben: ".
    
    --- NEWSLETTER CONTENT START ---
    {newsletter_text}
    --- NEWSLETTER CONTENT END ---
    """
    
    response = model.generate_content(prompt.format(newsletter_text=content))
    return response.text