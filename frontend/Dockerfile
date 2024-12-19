# Stage 1: Build the Next.js application
FROM node:22.9.0-alpine AS builder

WORKDIR /app

# Copier les fichiers package.json et package-lock.json (ou yarn.lock)
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code source
COPY . .

# Construire l'application Next.js
RUN npm run build

# Stage 2: Serve the Next.js application
FROM node:22.9.0-alpine AS runner

WORKDIR /app

# Copier les fichiers buildés depuis l'étape builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/next.config.ts ./next.config.ts

# Installer uniquement les dépendances de production
RUN npm install --production

# Définir les variables d'environnement pour la production
ENV NODE_ENV=production

# Exposer le port utilisé par l'application
EXPOSE 3000

# Démarrer l'application Next.js en mode production
CMD ["npm", "start"]
