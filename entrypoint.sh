#!/usr/bin/env sh
set -e

echo "🚀 Iniciando servidor Ollama..."
# usando OLLAMA_HOST para host:porta
ollama serve &

echo "⏳ Aguardando API do Ollama ficar disponível..."
while ! curl -s http://localhost:11434/v1/models > /dev/null; do
  sleep 2
done

echo "📥 Iniciando pull do modelo llama3..."
ollama pull llama3

echo "✅ Modelo llama3 pronto!"
wait
