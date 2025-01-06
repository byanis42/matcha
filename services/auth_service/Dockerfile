# services/auth_service/Dockerfile

FROM python:3.11-slim as builder

# Paramètres d’environnement pour que Python n'écrive pas de fichiers pyc, etc.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Mettre à jour les paquets et installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements du service
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Créer le répertoire services/auth_service
RUN mkdir -p services/auth_service

# Copier le code de l’application dans /app/services/auth_service
COPY . services/auth_service

ENV PYTHONPATH="/app:${PYTHONPATH}"

# Exposer le port du service (par exemple 8000)
EXPOSE 8000

# Commande de démarrage par défaut
CMD ["uvicorn", "services.auth_service.interface.main:app", "--host", "0.0.0.0", "--port", "8000"]
