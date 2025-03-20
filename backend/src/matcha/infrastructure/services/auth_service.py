import bcrypt
import jwt
import time
import os


class AuthService:
    """
    Service d'authentification qui gère les tokens, le hachage de mots de passe,
    et la vérification des identités.
    """

    def __init__(self):
        # Configuration à initialiser ici
        self.token_expiry = 3600  # 1 heure par défaut

    async def hash_password(self, password: str) -> str:
        """Hash un mot de passe en utilisant bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Vérifie si un mot de passe correspond au hash."""
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    def generate_token(self, user_id: str) -> str:
        """Génère un token JWT pour l'authentification."""
        # Dans un vrai projet, récupérer la clé depuis les variables d'environnement
        secret_key = os.environ.get("JWT_SECRET", "dev-secret-key")

        payload = {
            "sub": user_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + self.token_expiry
        }

        return jwt.encode(payload, secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> dict:
        """Vérifie la validité d'un token JWT et retourne les informations qu'il contient."""
        secret_key = os.environ.get("JWT_SECRET", "dev-secret-key")

        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.PyJWTError:
            raise ValueError("Token invalide ou expiré")

    def generate_verification_token(self, user_id: str) -> str:
        """Génère un token pour la vérification d'email."""
        secret_key = os.environ.get("JWT_SECRET", "dev-secret-key")

        payload = {
            "sub": user_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + 86400,  # 24 heures
            "purpose": "email_verification"
        }

        return jwt.encode(payload, secret_key, algorithm="HS256")
