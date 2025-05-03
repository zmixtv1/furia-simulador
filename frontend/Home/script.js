import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getDatabase, ref, push, onChildAdded } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-database.js";
import { firebaseConfig } from "../firebase-config.js";

// Base URL da API Flask
const API_BASE = "http://127.0.0.1:5000";

// Inicializa Firebase
const app     = initializeApp(firebaseConfig);
const db      = getDatabase(app);
const chatRef = ref(db, "chat-publico");

// ───────────────────────────────────────────────────────────────────────────
// Ao carregar a página, primeiro busca canal live e depois inicializa tudo
window.addEventListener("DOMContentLoaded", async () => {
  // 1) Monta o iframe do Twitch com o canal ao vivo
  const iframe = document.getElementById("twitch-iframe");
  try {
    const res = await fetch(`${API_BASE}/live-channel`);
    const { channel } = await res.json();
    iframe.src = `https://player.twitch.tv/?channel=${channel}&parent=${location.hostname}`;
  } catch (err) {
    console.error("Erro ao obter canal live:", err);
    // fallback para um canal padrão
    iframe.src = `https://player.twitch.tv/?channel=furiatv&parent=${location.hostname}`;
  }

  // 2) Dispara a carga de notícias (se houver perfil)
  const stored = localStorage.getItem("fanProfile");
  if (stored) {
    const profile = JSON.parse(stored);
    const tags = profile.activities
      .split(",")
      .map(a => a.trim().toLowerCase())
      .filter(Boolean);
    if (tags.length) {
      console.log("🔖 Carregando notícias gerais da NewsAPI", tags);
      carregarNoticiasGerais();
    }
  }
});

// ───────────────────────────────────────────────────────────────────────────
// Função para carregar notícias filtradas por activities (títulos como links)
async function carregarNoticiasGerais() {
  try {
    const res = await fetch(`${API_BASE}/noticias-geral`);
    if (!res.ok) throw new Error(res.status);
    const { noticias } = await res.json();

    const box = document.getElementById("news-container");
    if (!noticias.length) {
      box.innerHTML = "<p>Não encontramos notícias sobre a FURIA.</p>";
      return;
    }

    box.innerHTML = `
      <ul class="news-titles">
        ${noticias.map(n => `
          <li><a class="siteNoticia" href="${n.link}" target="_blank">${n.titulo}</a></li>
        `).join("")}
      </ul>
    `;
  } catch (err) {
    console.error("Erro ao carregar notícias gerais:", err);
    document.getElementById("news-container")
      .innerHTML = "<p>Falha ao buscar notícias.</p>";
  }
}

// ───────────────────────────────────────────────────────────────────────────
// Simulador de Chat (lado esquerdo)
const formLeft = document.getElementById("formulario");
const ulLeft   = document.getElementById("mensagens");

formLeft.addEventListener("submit", async e => {
  e.preventDefault();
  const inp = document.getElementById("entrada");
  const txt = inp.value.trim();
  if (!txt) return;

  // 1) Mensagem do usuário
  addLeft("Você", txt);
  inp.value = "";

  // 2) Cria e exibe o <li> de loading
  const loadingLi = document.createElement("li");
  loadingLi.classList.add("bot", "loading");
  loadingLi.innerHTML = `<strong>FURIA Bot:</strong> Carregando…`;
  ulLeft.appendChild(loadingLi);
  ulLeft.scrollTop = ulLeft.scrollHeight;

  try {
    // 3) Chama a API
    const res = await fetch(`${API_BASE}/mensagem-bot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem: txt })
    });
    const { resposta } = await res.json();

    // 4) Substitui o loading pela resposta real
    loadingLi.innerHTML = `<strong>FURIA Bot:</strong> ${resposta}`;
    loadingLi.classList.remove("loading");
  } catch (err) {
    console.error(err);
    loadingLi.innerHTML = `<strong>FURIA Bot:</strong> Erro ao carregar a resposta 😕`;
    loadingLi.classList.remove("loading");
    loadingLi.classList.add("error");
  } finally {
    ulLeft.scrollTop = ulLeft.scrollHeight;
  }
});

function addLeft(who, text) {
  const li = document.createElement("li");
  li.innerHTML = `<strong>${who}:</strong> ${text}`;
  ulLeft.appendChild(li);
  ulLeft.scrollTop = ulLeft.scrollHeight;
}

// ───────────────────────────────────────────────────────────────────────────
// Verifica se a FURIA tem jogo hoje
const btnVerificar = document.getElementById("btn-verificar");
btnVerificar.addEventListener("click", async () => {
  const p = document.getElementById("placar");
  try {
    const res = await fetch(`${API_BASE}/verificar-jogo`);
    const { status } = await res.json();
    p.textContent = status;
  } catch (err) {
    console.error(err);
    p.textContent = "Erro ao verificar";
  }
});

// ───────────────────────────────────────────────────────────────────────────
// Chat ao vivo e apelido
const nickInp  = document.getElementById("nickname-input");
const nickBtn  = document.getElementById("nickname-submit");
const chatForm = document.getElementById("chat-form");
const chatInp  = document.getElementById("mensagem");
const chatUl   = document.getElementById("chat-publico");

let nickname = null;
chatInp.disabled = true;
chatForm.querySelector("button").disabled = true;

nickBtn.addEventListener("click", () => {
  const v = nickInp.value.trim();
  if (!v) return alert("Digite um apelido");
  nickname = v;
  document.querySelector(".nickname-box").innerHTML = `<p>Você: <strong>${v}</strong></p>`;
  chatInp.disabled = false;
  chatForm.querySelector("button").disabled = false;
});

chatForm.addEventListener("submit", e => {
  e.preventDefault();
  if (!nickname) return alert("Escolha um apelido");
  const t = chatInp.value.trim();
  if (!t) return;
  push(chatRef, { nome: nickname, texto: t, hora: new Date().toLocaleTimeString() });
  chatInp.value = "";
});

onChildAdded(chatRef, snap => {
  const { nome, texto, hora } = snap.val();
  const li = document.createElement("li");
  li.textContent = `[${hora}] ${nome}: ${texto}`;
  chatUl.appendChild(li);
  chatUl.scrollTop = chatUl.scrollHeight;
});
