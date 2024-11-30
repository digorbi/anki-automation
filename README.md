# Anki Cards Creation Automation

Enhance your language learning experience with this automation script tailored for [AnkiApp](https://apps.ankiweb.net/). This tool simplifies the process of creating flashcards by generating CSV files and audio files from JSON-formatted data, which can be directly imported into Anki. The script leverages gTTS to create audio for words and sentences, enabling voice-supported flashcards.


## Features
- Automatically generates audio files for flashcards.
- Converts JSON-formatted data into CSV for easy Anki import.
- Supports custom configuration for Anki media paths.
- Seamlessly integrates with Anki's voice-supported cards.


## Input File Generation
### Generating JSON Content

Consider using Big Language Models such as ChatGPT to generate JSON content. Here is the promt to help you started.

```
Generate JSON-formatted data that translates words from German to English, including example sentences in both languages. The structure should include:

1. A unique "Note ID" for each word, formatted as a lowercase version of the German word with underscores replacing spaces.
2. The German word ("de_word"):
   -  For verbs, include the following forms: present, 3rd person singular, preteritum, and perfect, separated by commas.
   - For nouns, include the appropriate article (e.g., "der," "die," "das") with the word. If there are changes in the plural form, include them; otherwise, provide the respective ending.
3. An example sentence in German ("de_sentence").
4. The English translation of the word ("en_word").
5. An example sentence in English, corresponding to the German sentence ("en_sentence").
6. Keep notes ("en_note") and audio links ("de_audio") as nulls.
7. Use A2/B1-level vocabulary in the example sentences to ensure they are relevant to intermediate learners.

For example:
[
    {
        "Note ID": "guten_tag",
        "de_word": "Guten Tag",
        "de_sentence": "Guten Tag! Wie geht es Ihnen?",
        "en_word": "Good day",
        "en_sentence": "Good day! How are you?",
        "en_note": null,
        "de_audio": null
    },
    {
      "Note ID": "gehen",
      "de_word": "gehen, geht, ging, ist gegangen",
      "de_sentence": "Ich gehe jeden Tag zur Arbeit.",
      "en_word": "to go",
      "en_sentence": "I go to work every day.",
      "en_note": null,
      "de_audio": null
    }
]

In the following messages, I will provide you with words and, occasionally, their translations to emphasize the meaning I want reflected in the examples.

Sometimes, instead of English translations, I may use another language. In such cases, you must include the provided language in the en_word and en_sentence fields of the JSON structure without changing the JSON keys.
```

After you finished with content generation you can run the script to prepated files in suitable for anki format.


## Project setup

### Prerequisites

Before setting up the project, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [AnkiApp](https://apps.ankiweb.net/)

### Installation

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Configuration

| Variable Name      | Description                                      | Example Value                                      |
|--------------------|--------------------------------------------------|----------------------------------------------------|
| `ANKI_MEDIA_PATH`  | Path to the Anki media collection directory      | `~/Library/Application Support/Anki2/User 1/collection.media` |

Create a `.env` file in the root directory and include the necessary configuration variables, or alternatively, set them in the shell session or operating system environment.


## Usage

### Prepare `cards.json`
Save the generated JSON content to a file named `cards.json` in the project directory. Ensure the structure of the JSON matches the required format as shown in the [Input File Generation](#input-file-generation) section.

### Run the Script
Execute the script to generate Anki-compatible files:
```sh
python gen_anki.py
```

### Output
The script will create:
1. An output folder `out` containing:
   - A CSV file (`anki_cards.csv`) formatted for Anki import.
   - Generated audio files for the flashcards.
2. A prompt to confirm copying audio files:
   ```
   Do you want to copy the audio files to '$ANKI_MEDIA_PATH'? (yes/no): 
   ```
   - Type `yes` to copy the audio files to your Anki media folder.
   - Type `no` to skip this step.

### Importing Cards into AnkiApp

1. Open AnkiApp.
2. Go to `File -> Import`.
3. Select the generated CSV file (`out/anki_cards.csv`).
4. Ensure the field separator is set to a comma (`,`).
5. Check that the Notetype matches the CSV format:
   - If a suitable Notetype does not exist, create the new one. See instructions bellow. 
6. Complete the import process.
7. Verify the imported cards, including audio playback, in your Anki deck.


## Notes

- To customize the audio language, adjust the `lang` parameter in the `generate_audio` function inside the script.
- Ensure your JSON input follows the required schema to avoid errors during the generation process.

## Setup Notetype in AnkiApp

The generator works with a specific Note Type format. To ensure compatibility, you will need to create a custom Note Type in AnkiApp with the exact fields, templates, and styling described below. Follow the steps to set up the Note Type correctly:

### Step 1: Create a New Note Type

1. Open AnkiApp and navigate to the **Manage Note Types** section:
   - On the main menu, click **Tools > Manage Note Types**.
   - Click **Add** to create a new Note Type.
2. Choose a template to clone (e.g., **Basic**) or create a custom Note Type from scratch.
3. Name your new Note Type, e.g., `German Vocabulary with Audio`.

### Step 2: Define Fields

In the Note Type editor, click **Fields** to add the following fields:

- `Note ID`: A unique identifier for each card (useful for syncing or tracking).
- `de_word`: The German word or phrase to learn.
- `de_sentence`: A German example sentence using the word.
- `en_word`: The English translation of the German word.
- `en_sentence`: The English translation of the German example sentence.
- `en_note`: Additional notes or explanations for the word or sentence.
- `de_audio`: An audio file of the German word or sentence.

### Step 3: Set Up Templates

#### Front Template
The front side of the card will display the German word and optionally the German sentence (if provided). Here's the template:

```html
{{de_word}}
{{#de_sentence}}
<br><br>
<i>{{de_sentence}}</i>
{{/de_sentence}}
{{de_audio}}
```

#### Back Template
The back side of the card will display the translation, including the English word, sentence, and optional notes. It will also include the content of the front side for context. Here's the template:

```html
{{FrontSide}}

<hr id=answer>

{{en_word}}
{{#en_sentence}}
<br><br>
<i>{{en_sentence}}</i>
{{/en_sentence}}
{{#en_note}}
<br><br>
<small>{{en_note}}</small>
{{/en_note}}
```

### Step 4: Customize Styling
Customize the appearance of your cards by adding the following CSS in the Styling section of the Note Type editor:

```css
.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
```

### Step 5: Save and Use the Note Type

Once you’ve completed these steps save your Note Type configuration.