
from flask import Flask, request, jsonify
import os
import openai
import threading

app = Flask(__name__)

# Load API key securely from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("API key not found. Set OPENAI_API_KEY in the environment variables.")

# Set OpenAI API key
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def process_question(question, result):
    """ Function to process AI response in a separate thread """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        result["answer"] = response.choices[0].message.content
    except Exception as e:
        result["error"] = str(e)

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

        result = {}  # Dictionary to store the response

        # Run OpenAI API call in a separate thread
        thread = threading.Thread(target=process_question, args=(question, result))
        thread.start()
        thread.join()  # Wait for the thread to finish

        if "error" in result:
            return jsonify({"error": result["error"]}), 500

        return jsonify({"answer": result["answer"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True)