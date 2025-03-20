class MockAuthService:
    """
    Version simulée du service d'authentification pour les tests.
    Stocke les mots de passe en clair pour faciliter les tests.
    """

    def __init__(self):
        self.token_expiry = 3600
        self.password_map = {}  # Mapping user_id -> password
        self.tokens = {}  # Mapping token -> user_id
        self.verification_tokens = {}  # Mapping token -> user_id

    async def hash_password(self, password: str) -> str:
        """Simule un hachage en retournant le mot de passe en clair."""
        return f"hashed_{password}"

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Vérifie si le mot de passe en clair correspond au "hash" simulé."""
        return hashed_password == f"hashed_{plain_password}"

    def generate_token(self, user_id: str) -> str:
        """Génère un token fictif pour l'authentification."""
        token = f"token_{user_id}_{len(self.tokens)}"
        self.tokens[token] = user_id
        return token

    def verify_token(self, token: str) -> dict:
        """Vérifie un token fictif."""
        if token in self.tokens:
            user_id = self.tokens[token]
            return {"sub": user_id, "exp": 9999999999}
        raise ValueError("Token invalide ou expiré")

    def generate_verification_token(self, user_id: str) -> str:
        """Génère un token fictif pour la vérification d'email."""
        token = f"verify_{user_id}_{len(self.verification_tokens)}"
        self.verification_tokens[token] = user_id
        return token
