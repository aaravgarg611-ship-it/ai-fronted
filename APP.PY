from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# IMPORTANT: API key must be set in Render ENV variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return "Backend is running"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"answer": "Please ask a question."})

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )

        answer = completion.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Server error: {str(e)}"})
