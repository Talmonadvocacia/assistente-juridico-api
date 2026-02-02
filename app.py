from flask import Flask, request
import os
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    pergunta = data.get("texto", "")

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente jurídico especializado em direito previdenciário brasileiro."},
            {"role": "user", "content": pergunta}
        ]
    )

    texto_resposta = resposta["choices"][0]["message"]["content"]

    return {
        "pergunta": pergunta,
        "resposta": texto_resposta
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
