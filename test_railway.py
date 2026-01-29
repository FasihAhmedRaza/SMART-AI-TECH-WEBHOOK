"""
Test Railway Deployment
Check if the webhook is live and responding
"""
import requests
import json

RAILWAY_URL = "https://smart-ai-dialogflow-cx-production.up.railway.app/webhook"

def test_railway_deployment():
    print("=" * 70)
    print("🚂 TESTING RAILWAY DEPLOYMENT")
    print("=" * 70)
    print(f"\nURL: {RAILWAY_URL}\n")
    
    # Test 1: Check if server is responding
    print("Test 1: Server Health Check...")
    try:
        response = requests.get(RAILWAY_URL.replace('/webhook', '/'), timeout=10)
        print(f"✅ Server is UP! Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server Error: {e}")
        return
    
    print("\n" + "-" * 70)
    
    # Test 2: Send webhook request
    print("\nTest 2: Webhook Endpoint Test...")
    
    test_payload = {
        "detectIntentResponseId": "railway-test-123",
        "languageCode": "en",
        "fulfillmentInfo": {"tag": "save_consultation_lead"},
        "sessionInfo": {
            "session": "railway-test-session",
            "parameters": {
                "user_name": "Railway Test User",
                "user_email": "railway@test.com",
                "objective": "Test Railway deployment",
                "processes_text": "Testing webhook integration",
                "current_tools": "Railway, Dialogflow CX",
                "main_challenge": "Deployment validation"
            }
        }
    }
    
    try:
        print("\nSending test webhook request...")
        response = requests.post(
            RAILWAY_URL,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Webhook is working!\n")
            
            # Parse response
            try:
                data = response.json()
                print("Response Data:")
                print(json.dumps(data, indent=2))
                
                # Check if response has expected structure
                if "fulfillmentResponse" in data:
                    messages = data.get("fulfillmentResponse", {}).get("messages", [])
                    if messages:
                        bot_response = messages[0].get("text", {}).get("text", [""])[0]
                        print(f"\n🤖 Bot Response: {bot_response}")
                
            except json.JSONDecodeError:
                print("Response (text):", response.text[:500])
        else:
            print(f"⚠️ WARNING: Unexpected status code {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Request took too long (>15s)")
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 NEXT STEPS:")
    print("  1. Check if lead appeared in Google Sheet")
    print("  2. Check if email notification was sent")
    print("  3. Update Dialogflow webhook URL if working")
    print("=" * 70)

if __name__ == "__main__":
    test_railway_deployment()
