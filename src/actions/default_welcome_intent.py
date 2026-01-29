from src.schemas import (
    FulfillmentResponse,
    Message,
    WebhookResponse,
    WebhookRequest,
    Text,
    SessionInfo,
)


async def default_welcome_intent(webhook_request: WebhookRequest) -> WebhookResponse:
    # Safely get parameters and count
    parameters = webhook_request.sessionInfo.parameters or {}
    count = parameters.get("count", 0)
    return WebhookResponse(
        fulfillmentResponse=FulfillmentResponse(
            messages=[
                Message(text=Text(text=["Added a variable in session."])),
            ]
        ),
        sessionInfo=SessionInfo(
            session=webhook_request.sessionInfo.session,
            parameters={
                "someKey": "somevalue",
                "count": count + 1,
            },
        ),
    )
