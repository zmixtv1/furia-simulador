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
    url = "https://www.hltv.org/team/6668/furia"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    roster = [p.text.strip() for p in soup.select(".playerLineupContainer .playerLineup a")][:5]
    upcoming = []
    for m in soup.select(".matches .upcomingMatch")[:3]:
        time = m.select_one(".matchTime").text.strip()
        teams = m.select(".matchTeam")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        opponent = teams[1].text.strip() if len(teams) > 1 else "Indefinido"
        upcoming.append(f"{time} vs {opponent}")
=======
        opp = teams[1].text.strip() if len(teams)>1 else "Indefinido"
        upcoming.append(f"{time} vs {opp}")
>>>>>>> Stashed changes
=======
        opp = teams[1].text.strip() if len(teams)>1 else "Indefinido"
        upcoming.append(f"{time} vs {opp}")
>>>>>>> Stashed changes

    parts = []
    if roster:
        parts.append("Roster: " + ", ".join(roster))
    if upcoming:
        parts.append("Próximos jogos: " + "; ".join(upcoming))
    return " | ".join(parts) if parts else "Sem dados disponíveis."

@app.route("/mensagem-bot", methods=["POST"])
<<<<<<< Updated upstream
<<<<<<< Updated upstream
def responder():
    user_message = request.json.get("mensagem", "").strip()

    # 1) Busca contexto atualizado da FURIA
    try:
        context = fetch_furia_info()
    except Exception:
        context = "Sem dados HLTV disponíveis no momento."

    # 2) Monta prompt para o Ollama
=======
def mensagem_bot():
    user_message = request.json.get("mensagem","").strip()
    try:
        context = fetch_furia_info()
    except:
        context = "Sem dados HLTV disponíveis."
>>>>>>> Stashed changes
=======
def mensagem_bot():
    user_message = request.json.get("mensagem","").strip()
    try:
        context = fetch_furia_info()
    except:
        context = "Sem dados HLTV disponíveis."
>>>>>>> Stashed changes
    prompt = f"""
Contexto HLTV sobre a FURIA: {context}
Você é um chat treinado para responder qualquer coisa sobre a FURIA, NÃO pode falar de outro time.
Fale brevemente como um fã empolgado (pode usar emojis).
Se perguntarem sobre datas de jogos, responda que não tem informação precisa.
Sempre fale no idioma que está sendo perguntado!
Fale somente o que foi perguntado!

<<<<<<< Updated upstream
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
=======
Contexto adicional sobre a FURIA:
- Organização profissional brasileira fundada em 8 de agosto de 2017 por Jaime Pádua, André Akkari e Cris Guedes, com sede em São Paulo (e atuação nos EUA para CS:GO e Apex).
- Compete em CS:GO, Rocket League, League of Legends, Valorant, Rainbow Six Siege, Apex Legends, Super Smash Bros. e Kings League.
- Conquistas de destaque: semifinalista no IEM Rio Major 2022 (CS:GO), campeã da ESL Pro League Season 12 NA e 3º lugar no Six Invitational 2025 (R6).
- Proprietários: Jaime Pádua, André Akkari, Cris Guedes; parceiros incluem Red Bull, PokerStars, Lenovo, Hellmann’s, Betnacional e Cruzeiro do Sul.
- Elenco atual de CS:GO: FalleN, chelo, yuurih, skullz, KSCERATO.
- Elenco atual de Valorant: khalil, mwzera, havoc, heat, raafa.
- Nomeada 5ª organização de esports mais bem sucedida em 2022 pelo Nerd Street e integrante do Club Support Program da Esports World Cup 2024.

Além do CS:GO, a FURIA marca presença em várias outras modalidades de esports de alto nível (com todo o sangue nos olhos de um verdadeiro fã! 😎🔥):
- Rocket League 🚀
- League of Legends 🐲
- Valorant 🎯
- Rainbow Six Siege 🏰
- Apex Legends 🔫
- Super Smash Bros. 🥊
- Kings League ⚽️

- Elenco por modalidade:
  - **Counter-Strike 2 / CS:GO**  
    - yuurih (sniper)  
    - KSCERATO (sniper)  
    - FalleN (capitão e IGL)  
    - molodoy (sniper)  
    - YEKINDAR (stand-in)  
  - **Valorant**  
    - Khalil (duelista)  
    - havoc (iniciador)  
    - heat (sentinela)  
    - raafa (IGL)  
    - pryze (sentinela)  
  - **Rocket League**  
    - yANXNZ (atacante)  
    - Lostt (mid)  
    - DRUFINHO (atacante)  
  - **League of Legends**  
    - Guigo (top)  
    - Tatu (jungle)  
    - Tutsz (mid)  
    - Ayu (bot)  
    - Jojo (support)  
  - **Rainbow Six Siege**  
    - FelipoX (líder de equipe)  
    - HerdsZ (IGL)  
    - Jv92 (suporte)  
    - Kheyze (entry fragger)  
    - nade (suporte)  
  - **Apex Legends**  
    - Xeratricky (capitão)  
    - Pandxrz (atacante)  
    - HisWattson (capitão lendário)  
  - **Super Smash Bros. Ultimate**  
    - Fatality (jogador profissional) 
Pergunta: "{user_message}"
"""
    try:
        r = requests.post("http://localhost:11434/api/generate", json={
            "model":"llama3",
            "prompt":prompt,
            "stream":False
        })
        resp = r.json().get("response","Desculpa, não consegui gerar resposta.")
    except:
        resp = "Erro ao conectar com IA."
    return jsonify({"resposta":resp})
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

@app.route("/verificar-jogo", methods=["GET"])
def verificar_jogo():
    try:
        r = requests.get("https://www.hltv.org/matches", headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(r.text,"html.parser")
        for m in soup.find_all("div", class_="upcomingMatch"):
            if "FURIA" in m.text:
                time = m.find("div", class_="matchTime").text.strip()
                teams = m.find_all("div", class_="matchTeam")
                opp = teams[1].text.strip() if len(teams)>1 else "Indefinido"
                return jsonify({"status":f"🎮 FURIA joga hoje às {time} contra {opp}!"})
        return jsonify({"status":"A FURIA não tem jogo hoje 😢"})
    except:
        return jsonify({"status":"Erro ao buscar info de jogo."})

@app.route("/noticias", methods=["GET"])
def noticias():
    tags = request.args.get("tags","").split(",")
    articles = []
    r = requests.get("https://www.hltv.org/news", headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(r.text,"html.parser")
    for item in soup.select(".news-container .news")[:5]:
        title = item.select_one(".news-heading").text.strip()
        link  = "https://www.hltv.org" + item.select_one("a")["href"]
        desc  = item.select_one(".news-description").text.strip()
        txt   = (title+" "+desc).lower()
        if any(t.strip().lower() in txt for t in tags if t.strip()):
            articles.append({"titulo":title,"link":link,"resumo":desc})
    return jsonify({"noticias":articles})

<<<<<<< Updated upstream
<<<<<<< Updated upstream
        return jsonify({"status": "A FURIA não tem jogo hoje 😢"})
    except Exception:
        return jsonify({"status": "Erro ao buscar informações do jogo."})

if __name__ == "__main__":
=======
if __name__=="__main__":
>>>>>>> Stashed changes
=======
if __name__=="__main__":
>>>>>>> Stashed changes
    app.run(debug=True)
