import csv
from gtts import gTTS
import os
import shutil
import json
from dotenv import load_dotenv

load_dotenv()

input_json_file = "cards.json"
with open(input_json_file, 'r') as file:
    cards = json.load(file)

destination_path = os.getenv('ANKI_MEDIA_PATH')
if not destination_path:
    print("Error: The environment variable 'ANKI_MEDIA_PATH' is not defined.")
    exit(1)

destination_path = os.path.expanduser(destination_path)
if not os.path.exists(destination_path):
    print(f"Error: The destination path '{destination_path}' does not exist.")
    exit(1)

output_folder = "out"
os.makedirs(output_folder, exist_ok=True)

def generate_audio(text, lang, sound_id):
    tts = gTTS(text, lang=lang)
    audio_filename = f"gtts-{sound_id}.mp3"
    audio_file = os.path.join(output_folder, audio_filename)
    tts.save(audio_file)
    return audio_file

audio_files = []
for card in cards:
    audio_file = generate_audio(card["de_sentence"], 'de', card['Note ID'])
    audio_files.append(audio_file)
    card["de_audio"] = f"[sound:{os.path.basename(audio_file)}]"

output_file = "anki_cards.csv"
output_file_path = os.path.join(output_folder, output_file)
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=cards[0].keys())
    writer.writerows(cards)

confirmation = input(f"Do you want to copy the audio files to '{destination_path}'? (yes/no): ").strip().lower()
if confirmation == 'yes':
    for audio_file in audio_files:
        shutil.copy(audio_file, destination_path)
    
    print("Audio files have been copied to the Anki media folder.")
else:
    print("Audio files were not copied.")