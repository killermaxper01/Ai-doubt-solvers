import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import threading

# Load API key securely from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

def call_openai(prompt):
    """ Runs OpenAI API call in a separate thread. """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            api_key=OPENAI_API_KEY
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask():
    """ API endpoint to process student queries. """
    data = request.get_json()
    prompt = data.get("question")

    if not prompt:
        return jsonify({"error": "No question provided"}), 400

    # Run OpenAI call in a thread for performance
    response = threading.Thread(target=call_openai, args=(prompt,))
    response.start()
    response.join()

    return jsonify({"response": response.run()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)