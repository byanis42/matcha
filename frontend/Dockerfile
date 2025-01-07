# frontend/Dockerfile

FROM node:20-alpine AS builder

WORKDIR /app

# Copie des manifests
COPY package*.json ./
# Installation des dépendances
RUN npm install

# Copie du code
COPY . .

# Build de l'application Next.js
RUN npm run build

# Étape runner : image de production plus légère
FROM node:20-alpine AS runner
WORKDIR /app

# Copier seulement le build final
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/tailwind.config.ts ./
COPY --from=builder /app/postcss.config.mjs ./

# Installer les deps de prod
RUN npm install --production

EXPOSE 3000

# Démarrer Next.js
CMD ["npm", "start"]
