from typing import List, Dict, Any


class MockEmailService:
    """
    Version simulée du service d'email pour les tests.
    Stocke les emails envoyés pour vérification dans les tests.
    """

    def __init__(self):
        self.sent_emails: List[Dict[str, Any]] = []

    async def send_email(self, to_email: str, subject: str, content: str, is_html: bool = False):
        """
        Simule l'envoi d'un email en l'enregistrant dans la liste.
        """
        self.sent_emails.append({
            "to": to_email,
            "subject": subject,
            "content": content,
            "is_html": is_html
        })

        print(f"[MOCK EMAIL] À: {to_email}, Sujet: {subject}")

    async def send_verification_email(self, to_email: str, user_name: str, verification_token: str):
        """
        Simule l'envoi d'un email de vérification de compte.
        """
        subject = "Vérification de votre compte Matcha"
        content = f"Vérifiez votre compte avec le token: {verification_token}"

        await self.send_email(to_email, subject, content)

        # Ajouter des métadonnées supplémentaires pour faciliter les tests
        self.sent_emails[-1]["type"] = "verification"
        self.sent_emails[-1]["user_name"] = user_name
        self.sent_emails[-1]["token"] = verification_token

    async def send_password_reset_email(self, to_email: str, user_name: str, reset_token: str):
        """
        Simule l'envoi d'un email de réinitialisation de mot de passe.
        """
        subject = "Réinitialisation de votre mot de passe Matcha"
        content = f"Réinitialisez votre mot de passe avec le token: {reset_token}"

        await self.send_email(to_email, subject, content)

        # Ajouter des métadonnées supplémentaires pour faciliter les tests
        self.sent_emails[-1]["type"] = "password_reset"
        self.sent_emails[-1]["user_name"] = user_name
        self.sent_emails[-1]["token"] = reset_token

    def clear_sent_emails(self):
        """
        Effacer tous les emails enregistrés.
        """
        self.sent_emails.clear()

    def get_sent_emails(self, email_type=None):
        """
        Récupérer tous les emails envoyés, filtré par type si nécessaire.
        """
        if email_type is None:
            return self.sent_emails

        return [email for email in self.sent_emails if email.get("type") == email_type]
