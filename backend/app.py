from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# URL do servidor Ollama (pode ser sobrescrito por Docker Compose)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def fetch_furia_info():
    """
    Faz scraping da página da FURIA no HLTV para extrair o roster atual
    e os próximos jogos agendados.
    """
    url = "https://www.hltv.org/team/6668/furia"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extrai nomes do roster
    roster = [p.text.strip() for p in soup.select(".playerLineupContainer .playerLineup a")]
    roster = roster[:5]

    # Extrai próximos jogos
    upcoming = []
    for m in soup.select(".matches .upcomingMatch")[:3]:
        time = m.select_one(".matchTime").text.strip()
        teams = m.select(".matchTeam")
        opponent = teams[1].text.strip() if len(teams) > 1 else "Indefinido"
        upcoming.append(f"{time} vs {opponent}")

    parts = []
    if roster:
        parts.append("Roster: " + ", ".join(roster))
    if upcoming:
        parts.append("Próximos jogos: " + "; ".join(upcoming))
    return " | ".join(parts) if parts else "Sem dados disponíveis."

@app.route("/mensagem-bot", methods=["POST"])
def responder():
    user_message = request.json.get("mensagem", "").strip()

    # 1) Busca contexto atualizado da FURIA
    try:
        context = fetch_furia_info()
    except Exception:
        context = "Sem dados HLTV disponíveis no momento."

    # 2) Monta prompt para o Ollama
    prompt = f"""
Contexto HLTV sobre a FURIA: {context}

Você é um chat treinado para responder qualquer coisa sobre a FURIA, NÃO pode falar de outro time.
Fale brevemente como um fã empolgado (pode usar emojis).
Se perguntarem sobre datas de jogos, responda que não tem informação precisa.
Sempre fale no idioma que está sendo perguntado!
Fale somente o que foi perguntado!

Pergunta do fã: "{user_message}"
"""

    # 3) Chama o Ollama local via variável de ambiente
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        texto = resp.json().get("response", "Desculpa, não consegui gerar uma resposta.")
    except Exception:
        texto = "Erro ao conectar com o Ollama."

    return jsonify({"resposta": texto})

@app.route("/verificar-jogo", methods=["GET"])
def verificar_jogo():
    """
    Scraping simples da página de partidas da HLTV
    para ver se a FURIA tem jogo hoje.
    """
    try:
        url = "https://www.hltv.org/matches"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        jogos = soup.find_all("div", class_="upcomingMatch")

        for jogo in jogos:
            if "FURIA" in jogo.text:
                hora = jogo.find("div", class_="matchTime").text.strip()
                teams = jogo.find_all("div", class_="matchTeam")
                adversario = teams[1].text.strip() if len(teams) > 1 else "Adversário indefinido"
                return jsonify({
                    "status": f"🎮 FURIA joga hoje às {hora} contra {adversario}!"
                })

        return jsonify({"status": "A FURIA não tem jogo hoje 😢"})
    except Exception:
        return jsonify({"status": "Erro ao buscar informações do jogo."})

if __name__ == "__main__":
    app.run(debug=True)
