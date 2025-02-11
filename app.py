from flask import Flask, request, jsonify
import openai
import os
import threading

app = Flask(__name__)

# Securely fetch OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Please set it as an environment variable.")

openai.api_key = OPENAI_API_KEY

# Function to handle OpenAI requests in a separate thread
def get_openai_response(question, response_dict):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        response_dict["answer"] = response["choices"][0]["message"]["content"]
    except Exception as e:
        response_dict["error"] = str(e)

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get("question")

        if not question:
            return jsonify({"error": "Missing question parameter"}), 400

        response_dict = {}
        thread = threading.Thread(target=get_openai_response, args=(question, response_dict))
        thread.start()
        thread.join()

        if "error" in response_dict:
            return jsonify({"error": "It is a server-side problem, please be patient."}), 500

        return jsonify({"answer": response_dict["answer"]})

    except Exception as e:
        return jsonify({"error": "It is a server-side problem, please be patient."}), 500

if __name__ == '__main__':
    app.run(debug=True)