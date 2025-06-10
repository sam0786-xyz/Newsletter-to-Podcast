# main.py
import gmail_reader
import script_generator
import audio_generator

def main():
    print("--- Step 1: Fetching Newsletter ---")
    newsletter_text = gmail_reader.get_newsletter_content()
    
    if not newsletter_text:
        print("No content found. Exiting.")
        return

    print("--- Step 2: Generating Podcast Script ---")
    podcast_script = script_generator.generate_podcast_script(newsletter_text)
    print("--- Script Generated ---")
    print(podcast_script) # Print the script to the console
    
    print("\n--- Step 3: Generating Audio ---")
    audio_generator.create_podcast_audio(podcast_script, "newsletter_podcast.mp3")
    
    print("\n--- All Done! Your podcast is ready at newsletter_podcast.mp3 ---")

if __name__ == '__main__':
    main()