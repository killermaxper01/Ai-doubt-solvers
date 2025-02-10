from flask import Flask, request, jsonify
import os
import openai
# Updated OpenAI API compatibility
app = Flask(__name__)

# Load OpenAI API key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("API key not found. Set OPENAI_API_KEY in the environment variables.")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Corrected API usage

@app.route('/')
def home():
    return "AI Doubt Solver API is running!"

@app.route('/ask', methods=['POST'])  # Allow only POST requests
def ask_question():
    try:
        data = request.json  # Get JSON data from request
        question = data.get("question")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        # Use new OpenAI API format
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )

        answer = response.choices[0].message.content  # Extract answer

        return jsonify({"answer": answer})  # Return the answer

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)