from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    pergunta = data.get("texto", "")

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=pergunta
    )

    return {
        "pergunta": pergunta,
        "resposta": resp.output_text
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
