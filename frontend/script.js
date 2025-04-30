import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import {
  getDatabase, ref, push, onChildAdded
} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-database.js";
import { firebaseConfig } from "./firebase-config.js";

// Inicializa Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const chatRef = ref(db, "chat-publico");

/* -----------------------
   SIMULADOR (lado esquerdo)
------------------------*/
const formLeft = document.getElementById("formulario");
const ulLeft   = document.getElementById("mensagens");

formLeft.addEventListener("submit", async e => {
  e.preventDefault();
  const inp = document.getElementById("entrada");
  const msg = inp.value.trim();
  if (!msg) return;
  addLeft("Você", msg);
  inp.value = "";

  // chama Flask /mensagem-bot
  try {
    const res = await fetch("http://127.0.0.1:5000/mensagem-bot", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({mensagem: msg})
    });
    const { resposta } = await res.json();
    addLeft("FURIA Bot", resposta);
  } catch {
    addLeft("Erro", "Sem resposta do servidor");
  }
});

function addLeft(who, text) {
  const li = document.createElement("li");
  li.innerHTML = `<strong>${who}:</strong> ${text}`;
  ulLeft.appendChild(li);
  ulLeft.scrollTop = ulLeft.scrollHeight;
}

// verificar jogo
document.getElementById("btn-verificar").addEventListener("click", async () => {
  try {
    const res  = await fetch("http://127.0.0.1:5000/verificar-jogo");
    const { status } = await res.json();
    document.getElementById("placar").textContent = status;
  } catch {
    document.getElementById("placar").textContent = "Erro ao verificar";
  }
});


/* -----------------------
   NICKNAME + CHAT AO VIVO
------------------------*/
const nickInp  = document.getElementById("nickname-input");
const nickBtn  = document.getElementById("nickname-submit");
const chatForm = document.getElementById("chat-form");
const chatInp  = document.getElementById("mensagem");
const chatList = document.getElementById("chat-publico");

let nickname = null;
chatInp.disabled = true;
chatForm.querySelector("button").disabled = true;

// define apelido
nickBtn.addEventListener("click", () => {
  const v = nickInp.value.trim();
  if (!v) return alert("Digite um apelido válido");
  nickname = v;
  document.querySelector(".nickname-box").innerHTML =
    `<p>Você está como: <strong>${nickname}</strong></p>`;
  chatInp.disabled = false;
  chatForm.querySelector("button").disabled = false;
});

// envia mensagem ao vivo
chatForm.addEventListener("submit", e => {
  e.preventDefault();
  if (!nickname) return alert("Escolha um apelido antes");
  const txt = chatInp.value.trim();
  if (!txt) return;
  push(chatRef, { nome: nickname, texto: txt, hora: new Date().toLocaleTimeString() });
  chatInp.value = "";
});

// recebe mensagens em tempo real
onChildAdded(chatRef, snap => {
  const { nome, texto, hora } = snap.val();
  const li = document.createElement("li");
  li.textContent = `[${hora}] ${nome}: ${texto}`;
  chatList.appendChild(li);
  chatList.scrollTop = chatList.scrollHeight;
});
