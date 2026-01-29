from src.schemas import (
    FulfillmentResponse,
    Message,
    WebhookResponse,
    WebhookRequest,
    Text,
    SessionInfo,
)

async def calculate_price(webhook_request: WebhookRequest) -> WebhookResponse:
    parameters = webhook_request.sessionInfo.parameters or {}
    
    # LEGACY: This function is no longer used in the new consultation flow
    # It's kept for backward compatibility only
    
    response_text = "The pricing calculator is no longer available. Please proceed with the consultation flow to get a custom quote."
    
    return WebhookResponse(
        fulfillmentResponse=FulfillmentResponse(
            messages=[
                Message(text=Text(text=[response_text]))
            ]
        ),
        sessionInfo=SessionInfo(
            session=webhook_request.sessionInfo.session,
            parameters={**parameters}
        ),
    )
