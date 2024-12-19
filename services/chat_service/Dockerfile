FROM python:3.11-slim as builder

# Paramètres d’environnement pour que Python n'écrive pas de fichiers pyc, etc.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Mettez à jour les paquets
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier les requirements du service
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l’application
COPY . .

# Exposer le port du service (par exemple 8000)
EXPOSE 8000

# Commande de démarrage par défaut (à ajuster selon l'entrypoint FastAPI)
# On suppose que le fichier main FastAPI est dans interface/main.py avec app = FastAPI()
CMD ["uvicorn", "interface.main:app", "--host", "0.0.0.0", "--port", "8000"]
