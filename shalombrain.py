from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask():

    data = request.json
    question = data["question"]

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role":"system","content":"You are ShalomBrAIn, an AI trained on Torah, Talmud, and Rashi. Give thoughtful Jewish learning answers."},
            {"role":"user","content":question}
        ]
    )

    answer = response.choices[0].message.content

    return jsonify({"answer":answer})


if __name__ == "__main__":
    app.run()
