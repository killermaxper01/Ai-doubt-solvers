from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Load API key securely from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("API key not found. Set OPENAI_API_KEY in the environment variables.")

openai.api_key = OPENAI_API_KEY  # Set API key for OpenAI

@app.route('/')
def home():
    return "AI Doubt Solver API is running!"

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get("question")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )

        return jsonify({"answer": response['choices'][0]['message']['content']})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
