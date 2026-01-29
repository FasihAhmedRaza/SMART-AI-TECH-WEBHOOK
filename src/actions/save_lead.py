from fastapi import BackgroundTasks
from src import logging
from src.schemas import (
    FulfillmentResponse,
    Message,
    WebhookResponse,
    WebhookRequest,
    Text,
    SessionInfo,
)
from src.utils import send_consultation_lead_to_webhook, send_email_notification
from src.config import RESPONSES

logger = logging.getLogger(__name__)

async def save_lead(webhook_request: WebhookRequest) -> WebhookResponse:
    """
    LEGACY: Handles old pricing calculator leads (if needed).
    Now redirects to save_consultation_lead.
    """
    parameters = webhook_request.sessionInfo.parameters or {}
    language_code = webhook_request.languageCode or "en"
    
    response_text = RESPONSES.get(language_code, RESPONSES["en"])["consultation_saved"]
    
    return WebhookResponse(
        fulfillmentResponse=FulfillmentResponse(
            messages=[Message(text=Text(text=[response_text]))]
        ),
        sessionInfo=SessionInfo(
            session=webhook_request.sessionInfo.session,
            parameters={**parameters}
        )
    )


async def send_email_in_background(lead_data: dict):
    """
    Background task to send email without blocking webhook response
    NOTE: Railway blocks SMTP connections by default
    This task will fail silently if network is blocked
    """
    logger.info(f"📧 [BACKGROUND] Starting email send for lead: {lead_data.get('name')}")
    try:
        email_sent = send_email_notification(lead_data)
        if email_sent:
            logger.info("✅ [BACKGROUND] Email notification sent successfully!")
        else:
            logger.warning("⚠️ [BACKGROUND] Email notification failed, but lead was saved to Google Sheet.")
    except Exception as e:
        logger.error(f"❌ [BACKGROUND] Email notification error: {str(e)} (lead still saved to Google Sheet)")


async def save_consultation_lead(webhook_request: WebhookRequest, background_tasks: BackgroundTasks = None) -> WebhookResponse:
    """
    NEW: Handles the consultation qualification flow.
    Captures business objectives, processes, tools, and challenges.
    Sends structured data to Google Sheets for manual proposal creation.
    
    OPTIMIZED: Email sending is now a background task (non-blocking)
    This prevents webhook timeouts on Railway where SMTP is slow.
    
    Parameters expected from Dialogflow CX:
    - user_name: Contact name
    - user_email: Contact email
    - objective: Business objective (from @BusinessObjective entity)
    - processes_text: Processes to automate (free text)
    - current_tools: Current tools in use (free text)
    - main_challenge: Main challenge (from @MainChallenge entity)
    """
    parameters = webhook_request.sessionInfo.parameters or {}
    language_code = webhook_request.languageCode or "en"
    
    # Extract consultation data from parameters
    lead_data = {
        "name": parameters.get("user_name"),
        "email": parameters.get("user_email"),
        "objective": parameters.get("objective"),
        "processes_to_automate": parameters.get("processes_text"),
        "current_tools": parameters.get("current_tools"),
        "main_challenge": parameters.get("main_challenge"),
        "language": language_code,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }
    
    logger.info(f"💾 Saving consultation lead: {lead_data.get('name')} ({lead_data.get('email')})")
    
    # Send to Google Apps Script (SYNCHRONOUS - fast)
    success = send_consultation_lead_to_webhook(lead_data)
    
    # Send email notification in BACKGROUND (non-blocking)
    # This prevents Dialogflow timeouts on Railway
    if success and background_tasks:
        background_tasks.add_task(send_email_in_background, lead_data)
        logger.info("📧 Email notification scheduled in background (non-blocking)")
    
    # Select bilingual response
    response_key = "consultation_saved" if success else "consultation_error"
    response_text = RESPONSES.get(language_code, RESPONSES["en"])[response_key]
    
    return WebhookResponse(
        fulfillmentResponse=FulfillmentResponse(
            messages=[Message(text=Text(text=[response_text]))]
        ),
        sessionInfo=SessionInfo(
            session=webhook_request.sessionInfo.session,
            parameters={**parameters}
        )
    )
