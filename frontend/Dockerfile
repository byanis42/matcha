# Étape 1 : Builder
FROM node:18-alpine AS builder

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install
# Copier le reste du code source
COPY . .

# Construire l'application Next.js
RUN npm run build

# Étape 2 : Production
FROM node:18-alpine AS runner

WORKDIR /app

# Copier uniquement les fichiers nécessaires depuis le builder
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Installer les dépendances de production
RUN npm install --production

# Exposer le port 3000
EXPOSE 3000

# Définir la commande de démarrage
CMD ["npm", "start"]
