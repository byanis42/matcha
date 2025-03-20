from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    """
    Service d'envoi d'emails.
    """

    def __init__(self):
        # Configuration SMTP
        self.smtp_host = "smtp.example.com"
        self.smtp_port = 587
        self.smtp_user = "noreply@matcha.com"
        self.smtp_password = "password"  # À récupérer depuis les variables d'environnement
        self.from_email = "noreply@matcha.com"

    async def send_email(self, to_email: str, subject: str, content: str, is_html: bool = False):
        """
        Envoie un email.
        """
        # Construction du message
        message = MIMEMultipart()
        message["From"] = self.from_email
        message["To"] = to_email
        message["Subject"] = subject

        # Ajout du contenu
        content_type = "html" if is_html else "plain"
        message.attach(MIMEText(content, content_type))

        # Envoi via SMTP
        # En production, on connecterait réellement au serveur SMTP
        print(f"[EMAIL] À: {to_email}, Sujet: {subject}")
        print(f"[EMAIL] Contenu: {content[:100]}...")

    async def send_verification_email(self, to_email: str, user_name: str, verification_token: str):
        """
        Envoie un email de vérification de compte.
        """
        subject = "Vérification de votre compte Matcha"

        # URL de vérification avec le token
        verification_url = f"https://matcha.com/verify?token={verification_token}"

        # Contenu de l'email en HTML
        content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .btn {{ display: inline-block; padding: 10px 20px; background-color: #ff4b4b; color: white;
                        text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Bienvenue sur Matcha, {user_name} !</h2>
                <p>Merci de vous être inscrit. Pour activer votre compte, veuillez cliquer sur le bouton ci-dessous :</p>
                <p><a href="{verification_url}" class="btn">Vérifier mon compte</a></p>
                <p>Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :</p>
                <p>{verification_url}</p>
                <p>Ce lien expirera dans 24 heures.</p>
                <p>Cordialement,<br>L'équipe Matcha</p>
            </div>
        </body>
        </html>
        """

        await self.send_email(to_email, subject, content, is_html=True)

    async def send_password_reset_email(self, to_email: str, user_name: str, reset_token: str):
        """
        Envoie un email de réinitialisation de mot de passe.
        """
        subject = "Réinitialisation de votre mot de passe Matcha"

        # URL de réinitialisation avec le token
        reset_url = f"https://matcha.com/reset-password?token={reset_token}"

        # Contenu de l'email en HTML
        content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .btn {{ display: inline-block; padding: 10px 20px; background-color: #ff4b4b; color: white;
                        text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Réinitialisation de mot de passe</h2>
                <p>Bonjour {user_name},</p>
                <p>Vous avez demandé à réinitialiser votre mot de passe. Cliquez sur le bouton ci-dessous pour procéder :</p>
                <p><a href="{reset_url}" class="btn">Réinitialiser mon mot de passe</a></p>
                <p>Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :</p>
                <p>{reset_url}</p>
                <p>Ce lien expirera dans 1 heure. Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.</p>
                <p>Cordialement,<br>L'équipe Matcha</p>
            </div>
        </body>
        </html>
        """

        await self.send_email(to_email, subject, content, is_html=True)
