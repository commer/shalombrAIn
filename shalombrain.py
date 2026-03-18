from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__, static_folder='static')

# Serve index.html (must be in /templates folder)
@app.route("/")
def home():
    return render_template("index.html")

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# In-memory conversation history
conversation_history = []

# Ask endpoint
@app.route("/ask", methods=["POST"])
def ask():
    global conversation_history

    try:
        # Safely get JSON data, force=True ensures it parses even if headers are missing
        data = request.get_json(force=True)

        if not data or "question" not in data:
            return jsonify({"answer": "Invalid request."})

        user_question = data["question"].strip()

        if not user_question:
            return jsonify({"answer": "Please enter a question."})

        # Add user message
        conversation_history.append({
            "role": "user",
            "content": user_question
        })

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-5-mini",  # change if needed
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
        # Print the error to Render logs for debugging
        print("ERROR in /ask:", str(e))
        # Always return valid JSON
        return jsonify({"answer": f"Error: {str(e)}"})

# Clear conversation memory
@app.route("/clear", methods=["POST"])
def clear():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "cleared"})

# Run locally (Render uses Gunicorn instead)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
