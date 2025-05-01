FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 FLASK_APP=app.py FLASK_RUN_HOST=0.0.0.0

# instala deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia código
COPY backend/ ./
COPY frontend/ ./static/

EXPOSE 5000
CMD ["flask", "run"]
