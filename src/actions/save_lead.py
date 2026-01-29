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


async def save_consultation_lead(webhook_request: WebhookRequest) -> WebhookResponse:
    """
    NEW: Handles the consultation qualification flow.
    Captures business objectives, processes, tools, and challenges.
    Sends structured data to Google Sheets for manual proposal creation.
    
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
    
    # Send to Google Apps Script
    success = send_consultation_lead_to_webhook(lead_data)
    
    # Send email notification (optional - won't crash if it fails)
    if success:
        try:
            email_sent = send_email_notification(lead_data)
            if email_sent:
                print("✅ SUCCESS: Email notification sent successfully!")
            else:
                print("⚠️ WARNING: Email notification failed, but lead was saved to Google Sheet.")
        except Exception as e:
            print(f"⚠️ WARNING: Email notification error (lead still saved): {e}")
    
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
