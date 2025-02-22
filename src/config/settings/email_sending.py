import os

from src.config.env import BASE_DIR, env, env_to_enum
from src.hr_management_system.emails.enums import EmailSendingStrategy


# Load environment variables from .env file
env.read_env(os.path.join(BASE_DIR, ".env"))


# Default email configurations
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@example.com")
USE_ASYNC_EMAIL = False # Flag to enable/disable asynchronous email sending

# Email sending strategy: local | mailtrap | smtp4dev
EMAIL_SENDING_STRATEGY = env_to_enum(
    EmailSendingStrategy, env("EMAIL_SENDING_STRATEGY", default="local")
)

# Failure simulation settings for email sending (useful in testing)
EMAIL_SENDING_FAILURE_TRIGGER = env.bool("EMAIL_SENDING_FAILURE_TRIGGER", default=False)
EMAIL_SENDING_FAILURE_RATE = env.float("EMAIL_SENDING_FAILURE_RATE", default=0.2)

# Default email templates for user actions
DEFAULT_RESET_EMAIL_SUBJECT = "Password Reset Request"
DEFAULT_RESET_EMAIL_TEMPLATE_TXT = "emails/password_reset_email.txt"
DEFAULT_RESET_EMAIL_TEMPLATE_HTML = "emails/password_reset_email.html"

DEFAULT_REGISTRATION_EMAIL_SUBJECT = "Welcome to Our Service!"
DEFAULT_REGISTRATION_EMAIL_TEMPLATE_TXT = "emails/registration_email.txt"
DEFAULT_REGISTRATION_EMAIL_TEMPLATE_HTML = "emails/registration_email.html"

# Email backend configurations based on the chosen strategy
if EMAIL_SENDING_STRATEGY == EmailSendingStrategy.LOCAL:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if EMAIL_SENDING_STRATEGY == EmailSendingStrategy.MAILTRAP:
    EMAIL_BACKEND = env("EMAIL_BACKEND")
    EMAIL_HOST = env("MAILTRAP_EMAIL_HOST")
    EMAIL_HOST_USER = env("MAILTRAP_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("MAILTRAP_EMAIL_HOST_PASSWORD")
    EMAIL_PORT = env("MAILTRAP_EMAIL_PORT")

if EMAIL_SENDING_STRATEGY == EmailSendingStrategy.SMTP4DEV:
    EMAIL_BACKEND = env("EMAIL_BACKEND")
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = env('EMAIL_PORT')
