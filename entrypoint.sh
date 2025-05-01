#!/usr/bin/env bash
set -e

# Inicia o servidor Ollama em background
ollama serve &
pid=$!

# Dá um tempo pra ele subir
sleep 5

# Puxa o modelo
echo "📥 Pulling llama3 model..."
ollama pull llama3
echo "✅ llama3 ready!"

# Espera o servidor continuar rodando
wait $pid
