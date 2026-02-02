from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    pergunta = data.get("texto", "")

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente jurídico especializado em direito previdenciário brasileiro."},
            {"role": "user", "content": pergunta}
        ]
    )

    texto_resposta = resposta["choices"][0]["]()_
