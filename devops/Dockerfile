FROM python:3.10-slim

WORKDIR /app

# Instala dependências do sistema (ajustar conforme Oracle client, se necessário)
RUN apt-get update && apt-get install -y \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

# Copia API e arquivos necessários
COPY api/ ./api/
COPY ml/saved_models/ ./ml/saved_models/

WORKDIR /app/api

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV ORACLE_USER=""
ENV ORACLE_PASSWORD=""
ENV ORACLE_DSN=""

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
