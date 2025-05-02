# Dockerfile (backend Flask)
FROM python:3.12-slim

WORKDIR /app

# Dependências de sistema (se precisar compilar algo)
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# Instala as dependências Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do backend e os arquivos estáticos
COPY backend/ ./
COPY frontend/ ./static/

# Variáveis de ambiente Flask
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
