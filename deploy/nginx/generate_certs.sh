#!/bin/bash

# Variables pour les certificats
CERT_DIR="/etc/nginx/certs"
CERT_FILE="$CERT_DIR/selfsigned.crt"
KEY_FILE="$CERT_DIR/selfsigned.key"

# Vérifier si les certificats existent déjà
if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "Génération des certificats SSL auto-signés..."

    mkdir -p "$CERT_DIR"

    # Générer un certificat auto-signé
    openssl req -x509 -nodes -days 365 \
        -newkey rsa:2048 \
        -keyout "$KEY_FILE" \
        -out "$CERT_FILE" \
        -subj "/C=FR/ST=IDF/L=Paris/O=42/OU=IT/CN=localhost"

    echo "Certificats générés et stockés dans $CERT_DIR."
else
    echo "Certificats SSL déjà présents. Utilisation des certificats existants."
fi

# Démarrer Nginx
exec "$@"
