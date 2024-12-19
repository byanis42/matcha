# Utiliser l'image officielle Nginx comme base
FROM nginx:latest

# Installer OpenSSL pour générer des certificats
RUN apt-get update && \
    apt-get install -y openssl && \
    rm -rf /var/lib/apt/lists/*

# Copier le fichier de configuration Nginx personnalisé
COPY nginx.conf /etc/nginx/nginx.conf

# Copier le script de génération de certificats
COPY generate_certs.sh /usr/local/bin/generate_certs.sh

# Donner les permissions d'exécution au script
RUN chmod +x /usr/local/bin/generate_certs.sh

# Définir le point d'entrée pour exécuter le script avant de démarrer Nginx
ENTRYPOINT ["/usr/local/bin/generate_certs.sh"]

# Exposer les ports 80 et 443
EXPOSE 80 443

# Démarrer Nginx en mode premier plan
CMD ["nginx", "-g", "daemon off;"]
