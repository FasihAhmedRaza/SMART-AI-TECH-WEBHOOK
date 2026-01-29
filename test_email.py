"""
Complete test including email notification
"""
import asyncio
from src.actions.save_lead import save_consultation_lead
from src.schemas import WebhookRequest, FulfillmentInfo, SessionInfo

async def test_with_email():
    print("=" * 60)
    print("TESTING: Full Webhook Flow + Email Notification")
    print("=" * 60)
    
    # Create mock webhook request
    webhook_request = WebhookRequest(
        detectIntentResponseId="test-123",
        languageCode="en",
        fulfillmentInfo=FulfillmentInfo(tag="save_consultation_lead"),
        sessionInfo=SessionInfo(
            session="test-session",
            parameters={
                "user_name": "Fasih Test User",
                "user_email": "thisfasih@gmail.com",
                "objective": "Reduce operational workload",
                "processes_text": "Customer support, Internal approvals",
                "current_tools": "Gmail, Slack, Salesforce",
                "main_challenge": "Scalability"
            }
        )
    )
    
    print("\n1. Calling webhook handler...")
    response = await save_consultation_lead(webhook_request)
    
    print("\n2. Webhook response:")
    print(f"   Message: {response.fulfillmentResponse.messages[0].text.text[0]}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE!")
    print("Check:")
    print("  1. Google Sheet for new row")
    print("  2. Email inbox at thisfasih@gmail.com")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_with_email())
