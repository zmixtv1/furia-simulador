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
 seu idioma é portugues
  
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

@app.route("/noticias-geral", methods=["GET"])
def noticias_geral():
    """
    Busca as últimas notícias que mencionem 'FURIA' via NewsAPI.org.
    Se não vier q= na query string, pesquisa por 'FURIA'.
    """
    
    # Títulos padrão para busca
    titulos_padrao = ["FURIA", "CS", "Valorant", "LoL"]

    # Pega o parâmetro q da query string ou usa os títulos padrão
    q_raw = request.args.get("q", "").strip()

    # Se q for fornecido, use-o; caso contrário, use todos os títulos padrão concatenados
    if q_raw:
        query = q_raw
    else:
        query = " OR ".join(titulos_padrao)  # exemplo de como juntar os termos numa única busca
        
        
    # 2) Faz a requisição à NewsAPI
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "SUA_CHAVE_AQUI")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "pt",
        "pageSize": 10,
        "sortBy": "publishedAt",
        "apiKey": "952e1d13c7204913a12e63808f364cd3"
    }
    resp = requests.get(url, params=params)
    # 3) Se não for 200, devolve o erro
    if resp.status_code != 200:
        return jsonify({
            "error": "NewsAPI retornou erro",
            "status_code": resp.status_code,
            "body": resp.json()
        }), resp.status_code

    data = resp.json()
    # 4) Extrai os artigos
    articles = data.get("articles", [])
    resultados = [{
        
        "titulo": art.get("title") if art.get("title") else "Artigo sem titulo",
        "link":   art.get("url")
    } for art in articles]

    return jsonify({"noticias": resultados})


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