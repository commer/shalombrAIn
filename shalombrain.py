from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("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"))

@app.route("/ask", methods=["POST"])
def ask():

    data = request.json
    question = data["question"]

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role":"system","content":"You are shalombrAIn, an AI trained on Torah, Talmud, and Rashi. Give thoughtful Jewish learning answers."},
            {"role":"user","content":question}
        ]
    )

    answer = response.choices[0].message.content

    return jsonify({"answer":answer})


if __name__ == "__main__":
    app.run()
