import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ....config.settings import get_settings
from ....core.services.email_service import EmailService


class SMTPEmailService(EmailService):
    """SMTP email service implementation"""

    def __init__(self):
        self.settings = get_settings()

    async def send_verification_email(self, email: str, username: str, token: str) -> bool:
        """Send email verification email"""
        subject = "Verify Your Email - Matcha"

        # In development, we'll use a simple verification URL
        verification_url = f"http://localhost:5174/verify-email?token={token}&email={email}"

        html_body = f"""
        <html>
        <body>
            <h2>Welcome to Matcha, {username}!</h2>
            <p>Thank you for registering with Matcha. Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p>{verification_url}</p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't create an account with Matcha, please ignore this email.</p>
            <br>
            <p>Best regards,<br>The Matcha Team</p>
        </body>
        </html>
        """

        text_body = f"""
        Welcome to Matcha, {username}!

        Thank you for registering with Matcha. Please verify your email address by visiting:
        {verification_url}

        This link will expire in 24 hours.

        If you didn't create an account with Matcha, please ignore this email.

        Best regards,
        The Matcha Team
        """

        return await self._send_email(email, subject, text_body, html_body)

    async def send_password_reset_email(self, email: str, username: str, token: str) -> bool:
        """Send password reset email"""
        subject = "Reset Your Password - Matcha"

        reset_url = f"http://localhost:5174/reset-password?token={token}&email={email}"

        html_body = f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Hi {username},</p>
            <p>We received a request to reset your password for your Matcha account.</p>
            <p><a href="{reset_url}" style="background-color: #ff6b6b; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p>{reset_url}</p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request a password reset, please ignore this email.</p>
            <br>
            <p>Best regards,<br>The Matcha Team</p>
        </body>
        </html>
        """

        text_body = f"""
        Password Reset Request

        Hi {username},

        We received a request to reset your password for your Matcha account.

        Please visit: {reset_url}

        This link will expire in 1 hour.

        If you didn't request a password reset, please ignore this email.

        Best regards,
        The Matcha Team
        """

        return await self._send_email(email, subject, text_body, html_body)

    async def send_notification_email(self, email: str, subject: str, message: str) -> bool:
        """Send a general notification email"""
        html_body = f"""
        <html>
        <body>
            <h2>Matcha Notification</h2>
            <p>{message}</p>
            <br>
            <p>Best regards,<br>The Matcha Team</p>
        </body>
        </html>
        """

        return await self._send_email(email, subject, message, html_body)

    async def _send_email(self, to_email: str, subject: str, text_body: str, html_body: str) -> bool:
        """Send email using SMTP"""
        try:
            # Check if SMTP is configured (MailHog or real SMTP)
            if not self.settings.SMTP_HOST or self.settings.SMTP_HOST.strip() == "":
                # Fallback to console logging if no SMTP configured
                print("\n📧 EMAIL WOULD BE SENT (NO SMTP):")
                print(f"To: {to_email}")
                print(f"Subject: {subject}")
                print(f"Body: {text_body}")
                print(f"HTML Body: {html_body}")
                print("=" * 50)
                return True
            

            # For production, use actual SMTP
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.settings.EMAILS_FROM_EMAIL
            msg["To"] = to_email

            # Create the plain-text and HTML version of your message
            text_part = MIMEText(text_body, "plain")
            html_part = MIMEText(html_body, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            msg.attach(text_part)
            msg.attach(html_part)

            # Create connection with server and send email
            with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
                # Use TLS only if not MailHog (port 1025 = MailHog)
                if self.settings.SMTP_PORT != 1025:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                
                # Login only if credentials provided
                if self.settings.SMTP_USER and self.settings.SMTP_PASSWORD:
                    server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
