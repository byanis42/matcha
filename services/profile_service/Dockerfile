# services/profile_service/Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du service
COPY . services/profile_service

# Ajouter /app au PYTHONPATH
ENV PYTHONPATH="/app:${PYTHONPATH}"

EXPOSE 8000

CMD ["uvicorn", "services.profile_service.interface.main:app", "--host", "0.0.0.0", "--port", "8000"]
