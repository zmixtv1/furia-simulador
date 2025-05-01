# 🐆 FURIA Fan Simulator v1.0

**Uma plataforma completa para fãs da FURIA e-sports**, combinando um chatbot de torcida, transmissão ao vivo, chat comunitário, perfil de fã e feed de notícias personalizado.

---

## 📂 Estrutura do Projeto

```
furia-simulador/
├── backend/
│   ├── app.py              # API Flask (/mensagem-bot, /verificar-jogo, /noticias)
│   └── requirements.txt    # Dependências Python
├── frontend/
│   ├── index.html          # Tela principal: simulador + transmissão + chat + feed
│   ├── auth.html           # Split-screen cadastro / login
│   ├── login.html          # Página de login standalone
│   ├── style.css           # Estilos gerais do site
│   ├── style-auth.css      # Estilos de cadastro/login
│   └── firebase-config.js  # Configurações do Firebase Realtime Database
├── entrypoint.sh           # Script customizado para iniciar Ollama e puxar modelo
├── Dockerfile              # Dockerfile do backend + frontend estático
├── Dockerfile.ollama       # Dockerfile customizado para o Ollama
├── docker-compose.yml      # Orquestração Docker: Ollama + Flask (backend)
└── README.md               # Documentação (este arquivo)
```

---

## 🎯 Principais Funcionalidades

1. **Simulador de Torcida (Chatbot)**
   - IA baseada em **Ollama (Llama3)**.
   - Contexto atualizado da HLTV (roster, próximos jogos) via scraping.
   - Respostas emocionadas e no idioma do usuário.

2. **Transmissão Ao Vivo & Chat Comunitário**
   - Integração com Twitch/HLTV para embed ao vivo.
   - Chat em tempo real usando **Firebase Realtime Database**.
   - Apelido único configurável no painel.

3. **Verificação de Partidas**
   - Endpoint `/verificar-jogo` faz scraping na HLTV para indicar quando a FURIA joga.

4. **Feed de Notícias Personalizadas**
   - Endpoint `/noticias?tags=` filtra artigos da HLTV por interesses do usuário.
   - Renderização dinâmica abaixo dos cards principais.

5. **Perfil de Fã & Autenticação**
   - Telas de cadastro (`auth.html`) e login (`login.html`) em estilo split-screen.
   - Coleta de nome de usuário, nome completo, CPF, endereço, interesses, atividades, eventos e compras.

6. **Containerização com Docker Compose**
   - Serviço **ollama** para IA conversacional.
   - Serviço **backend** (Flask API + frontend estático).
   - Volume persistente para modelos e dados do Ollama.

---

## 🛠️ Tecnologias Utilizadas

| Camada              | Tecnologia                                  |
|---------------------|---------------------------------------------|
| Backend             | Python 3.12, Flask, Flask-CORS, Requests    |
| IA Conversacional   | Ollama (Llama3)                             |
| Real-Time Database  | Firebase Realtime DB (JS SDK v9)            |
| Web Scraping        | BeautifulSoup (HLTV.org)                    |
| Frontend            | HTML5, CSS3, JavaScript (ES6 Modules)       |
| Containerização     | Docker, Docker Compose                      |

---

## 🚀 Instalação & Execução

### Pré-requisitos

- Docker & Docker Compose v2+
- (Opcional) Ollama CLI para pré-pull de modelos

### Passo a Passo com Docker Compose

1. **Clone** este repositório:
   ```bash
   git clone https://github.com/seu-usuario/furia-simulador.git
   cd furia-simulador
   ```

2. **(Opcional)** Pré-baixe o modelo Llama3:
   ```bash
   ollama pull llama3
   ```

3. **Suba** os containers:
   ```bash
   docker compose down
   docker compose up --build
   ```

4. **Acesse**:
   - **Frontend**: `http://localhost:5000/static/index.html`
   - **API**: `http://localhost:5000`
   - **Ollama API**: `http://localhost:11434/api/list`

---

### Execução Local (sem Docker)

1. Crie e ative ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Instale dependências:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Configure o Firebase em `frontend/firebase-config.js`.
4. Inicie o Ollama:
   ```bash
   ollama run llama3
   ```
5. Inicie o Flask:
   ```bash
   cd backend
   python app.py
   ```
6. Sirva o front-end (ex: Live Server ou abrindo o arquivo Home - index.html).

---


## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

*Desenvolvido com ❤️ por Rodrigo Alaôr Lopes Moreira*

