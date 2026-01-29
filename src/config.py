import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Apps Script Web App URL for Google Sheets integration
GOOGLE_SHEETS_WEBAPP_URL = os.getenv(
    "GOOGLE_SHEET_URL",
    "https://script.google.com/macros/s/AKfycbw9M29dtemVGCjRjCsejBZrIbUgBb3VQycjHMytB9jFr_ktnrt3Ty4Ioz3BHzoGQzdD2g/exec"
)

# Email notification settings
EMAIL_NOTIFICATIONS_ENABLED = os.getenv("EMAIL_NOTIFICATIONS_ENABLED", "false").lower() == "true"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_FROM = os.getenv("EMAIL_FROM", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # App password for Gmail
EMAIL_TO = os.getenv("EMAIL_TO", "")  # Where to send notifications

# Consultation qualification responses (Bilingual)
RESPONSES = {
    "en": {
        "consultation_saved": "Thank you. Your details are saved. An expert will analyze your needs and contact you for a custom quote.",
        "consultation_error": "Your information has been noted. We'll contact you shortly to discuss your custom solution."
    },
    "fr": {
        "consultation_saved": "Merci. Vos informations sont enregistrées. Un expert analysera vos besoins et vous contactera pour un devis personnalisé.",
        "consultation_error": "Vos informations ont été notées. Nous vous contacterons bientôt pour discuter de votre solution personnalisée."
    }
}
