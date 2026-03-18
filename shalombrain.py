from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os

app = Flask(__name__, static_folder='static')

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# In-memory conversation history
conversation_history = []

# Serve index.html
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Ask endpoint
@app.route("/ask", methods=["POST"])
def ask():
    global conversation_history

    user_question = request.json.get("question")

    if not user_question:
        return jsonify({"answer": "Please enter a question."})

    # Add user message
    conversation_history.append({
        "role": "user",
        "content": user_question
    })

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are ShalomBrAIn, an expert in Torah, Rashi, and Talmud. Answer clearly and, when possible, reference Jewish sources."
                }
            ] + conversation_history
        )

        answer = response.choices[0].message.content

        # Add AI response
        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

# Clear conversation memory
@app.route("/clear", methods=["POST"])
def clear():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "cleared"})

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
