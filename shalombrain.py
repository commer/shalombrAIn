from flask import Flask, request, jsonify, send_from_directory
import os
from openai import OpenAI

app = Flask(__name__)

# Load API key safely
api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if not client:
        return jsonify({"answer": "API key not set yet."})

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are ShalomBrAIn, an expert in Torah, Talmud, and Rashi."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})
