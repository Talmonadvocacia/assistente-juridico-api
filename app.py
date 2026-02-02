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
    data = request.json
    pergunta = data.get("texto", "")

    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente jurídico especializado em direito previdenciário brasileiro. Responda de forma clara, simples e ética."
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]
    )

    texto_resposta = resposta.choices[0].message.content

    return {
        "pergunta": pergunta,
        "resposta": texto_resposta
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
