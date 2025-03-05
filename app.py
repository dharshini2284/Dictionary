from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_word', methods=['POST'])
def get_word():
    if request.method == 'POST':
        word = request.form['word'].strip()  # Get user input & remove extra spaces
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(api_url)

        if response.status_code == 200:
            try:
                data = response.json()[0]  
                word_text = data["word"]
                if len(data["phonetics"]) > 0:
                    phonetic_text = data["phonetics"][0]["text"]
                    phonetic_audio = data["phonetics"][0]["audio"]
                else:
                    phonetic_text = "N/A"
                    phonetic_audio = ""
                if len(data["meanings"]) > 0:
                    noun_definition = data["meanings"][0]["definitions"][0]["definition"]
                else:
                    noun_definition = "No definition available."

                if len(data["meanings"]) > 1:
                    verb_definition = data["meanings"][1]["definitions"][0]["definition"]
                else:
                    verb_definition = "No definition available."

                if len(data["meanings"]) > 2:
                    interjection_definition = data["meanings"][2]["definitions"][0]["definition"]
                else:
                    interjection_definition = "No definition available."

                if len(data["meanings"][2]["definitions"]) > 0 and "example" in data["meanings"][2]["definitions"][0]:
                    example_usage = data["meanings"][2]["definitions"][0]["example"]
                else:
                    example_usage = "No example available."

                if "synonyms" in data["meanings"][0] and len(data["meanings"][0]["synonyms"]) > 0:
                    synonyms = data["meanings"][0]["synonyms"]
                else:
                    synonyms = ["No synonyms available"]

                if "antonyms" in data["meanings"][2] and len(data["meanings"][2]["antonyms"]) > 0:
                    antonyms = data["meanings"][2]["antonyms"]
                else:
                    antonyms = ["No antonyms available"]

                if "sourceUrls" in data and len(data["sourceUrls"]) > 0:
                    source_url = data["sourceUrls"][0]
                else:
                    source_url = "#"

                return render_template("index.html",
                                       word=word_text,
                                       phonetic_text=phonetic_text,
                                       phonetic_audio=phonetic_audio,
                                       noun_definition=noun_definition,
                                       verb_definition=verb_definition,
                                       interjection_definition=interjection_definition,
                                       example_usage=example_usage,
                                       synonyms=synonyms,
                                       antonyms=antonyms,
                                       source_url=source_url)

            except (IndexError, KeyError) as e:
                return render_template("index.html", error="Invalid word format or missing data.")
        
        else:
            return render_template("index.html", error="Word not found or API error!")

if __name__ == '__main__':
    app.run()