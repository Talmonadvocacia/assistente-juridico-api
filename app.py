from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Você é um assistente virtual de um escritório de advocacia focado em direito previdenciário e bancário.
Seja extremamente educado, acolhedor e use linguagem simples.
Nunca use termos jurídicos difíceis.
Sempre alerte sobre golpes.
Se não souber algo, diga que vai verificar no sistema.
"""

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    texto = data.get("texto", "")

    if not texto:
        return jsonify({"error": "Campo 'texto' é obrigatório"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": texto}
            ],
            temperature=0.5,
            max_tokens=500
        )

        resposta_ia = response.choices[0].message.content

        return jsonify({
            "resposta": resposta_ia
        })

    except Exception as e:
        return jsonify({
            "error": "Erro ao consultar IA",
            "detail": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
