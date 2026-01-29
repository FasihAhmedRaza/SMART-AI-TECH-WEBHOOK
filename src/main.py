from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src import logging
from src.schemas import (
    WebhookRequest,
    WebhookResponse,
    FulfillmentResponse,
    Message,
    Text,
)
from src.actions.default_welcome_intent import default_welcome_intent
from src.actions.save_lead import save_lead, save_consultation_lead

logger = logging.getLogger(__name__)

app = FastAPI(title="Dialogflow CX Webhook API")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()}")
    logger.error(f"Body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.post("/webhook", response_model=WebhookResponse)
async def dialogflow_webhook(
    webhook_request: WebhookRequest
):
    logger.info("A new request came from Dialogflow.")
    # logger.info(webhook_request) # Commented out to reduce noise, enable if debugging needed
    try:
        tag = webhook_request.fulfillmentInfo.tag
        
        if tag == "defaultWelcomeIntent":
            return await default_welcome_intent(webhook_request=webhook_request)
        elif tag == "save_lead":
            return await save_lead(webhook_request=webhook_request)
        elif tag == "save_consultation_lead":
            return await save_consultation_lead(webhook_request=webhook_request)
        else:
            return WebhookResponse(
                fulfillmentResponse=FulfillmentResponse(
                    messages=[
                        Message(text=Text(text=[f"No handler for the tag: {tag}"]))
                    ]
                )
            )
    except Exception as e:
        logger.error(f"Error at /webhook {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Webhook processing error: {str(e)}"
        )
