
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
// Ao carregar a página, busca perfil e dispara a carga de notícias
window.addEventListener("DOMContentLoaded", () => {
  const stored = localStorage.getItem("fanProfile");
  if (!stored) return;

  const profile = JSON.parse(stored);
  const tags = profile.activities
    .split(",")
    .map(a => a.trim().toLowerCase())
    .filter(Boolean);

  if (tags.length) {
    console.log("🔖 Carregando notícias gerais da NewsAPI", tags);
    carregarNoticiasGerais(tags);
  }
});

// ───────────────────────────────────────────────────────────────────────────
// Simulador de Chat (lado esquerdo)
const formLeft = document.getElementById("formulario");
const ulLeft   = document.getElementById("mensagens");

formLeft.addEventListener("submit", async e => {
  e.preventDefault();
  const inp = document.getElementById("entrada");
  const txt = inp.value.trim();
  if (!txt) return;

  addLeft("Você", txt);
  inp.value = "";

  try {
    const res = await fetch(`${API_BASE}/mensagem-bot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem: txt })
    });
    const { resposta } = await res.json();
    addLeft("FURIA Bot", resposta);
  } catch (err) {
    console.error(err);
    addLeft("Erro", "Sem resposta do servidor");
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


