import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getDatabase, ref, push, onChildAdded } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-database.js";
import { firebaseConfig } from "../firebase-config.js";

// Inicializa Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const chatRef = ref(db, "chat-publico");

// — Simulador (esquerda) —
const formLeft = document.getElementById("formulario"), ulLeft = document.getElementById("mensagens");
formLeft.addEventListener("submit", async e => {
  e.preventDefault();
  const inp=document.getElementById("entrada"), txt=inp.value.trim();
  if(!txt) return; addLeft("Você",txt); inp.value="";
  try {
    let res=await fetch("http://127.0.0.1:5000/mensagem-bot", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body:JSON.stringify({mensagem:txt})
    });
    let { resposta } = await res.json();
    addLeft("FURIA Bot",resposta);
  } catch { addLeft("Erro","Sem resposta do servidor"); }
});
function addLeft(w,t){
  let li=document.createElement("li");
  li.innerHTML=`<strong>${w}:</strong> ${t}`;
  ulLeft.appendChild(li); ulLeft.scrollTop=ulLeft.scrollHeight;
}

// — Verificar jogo —
document.getElementById("btn-verificar").addEventListener("click", async()=>{
  const p=document.getElementById("placar");
  try {
    let res=await fetch("http://127.0.0.1:5000/verificar-jogo"), { status }=await res.json();
    p.textContent=status;
  } catch { p.textContent="Erro ao verificar"; }
});

// — Chat ao vivo + nickname —
const nickInp=document.getElementById("nickname-input"), nickBtn=document.getElementById("nickname-submit"),
      chatForm=document.getElementById("chat-form"), chatInp=document.getElementById("mensagem"),
      chatUl=document.getElementById("chat-publico");
let nickname=null; chatInp.disabled=true; chatForm.querySelector("button").disabled=true;

nickBtn.addEventListener("click", ()=>{
  const v=nickInp.value.trim(); if(!v) return alert("Digite um apelido");
  nickname=v;
  document.querySelector(".nickname-box").innerHTML=`<p>Você: <strong>${v}</strong></p>`;
  chatInp.disabled=false; chatForm.querySelector("button").disabled=false;
  carregarNoticias(["CS:GO","FURIA"]);
});

chatForm.addEventListener("submit", e=>{
  e.preventDefault(); if(!nickname) return alert("Escolha um apelido");
  const t=chatInp.value.trim(); if(!t) return;
  push(chatRef,{nome:nickname,texto:t,hora:new Date().toLocaleTimeString()});
  chatInp.value="";
});
onChildAdded(chatRef, snap=>{
  const {nome,texto,hora}=snap.val();
  let li=document.createElement("li");
  li.textContent=`[${hora}] ${nome}: ${texto}`;
  chatUl.appendChild(li); chatUl.scrollTop=chatUl.scrollHeight;
});

// — Notícias para você —
async function carregarNoticias(interesses){
  const tags=encodeURIComponent(interesses.join(","));
  try {
    let res=await fetch(`http://127.0.0.1:5000/noticias?tags=${tags}`),
        { noticias } = await res.json();
    const box=document.getElementById("news-container");
    box.innerHTML = noticias.map(n=>`
      <article>
        <a href="${n.link}" target="_blank">${n.titulo}</a>
        <p>${n.resumo}</p>
      </article>
    `).join("");
  } catch(e){
    console.error("Erro ao carregar notícias:", e);
  }
}
