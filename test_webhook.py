"""
Manual test script to verify the entire webhook flow
"""
import requests
import json
from src.config import GOOGLE_SHEETS_WEBAPP_URL

print("=" * 60)
print("MANUAL TEST: Webhook → Google Apps Script → Google Sheet")
print("=" * 60)

# Test data
test_lead = {
    "name": "Manual Test User",
    "email": "thisfasih@gmail.com",
    "objective": "Reduce operational workload",
    "processes_to_automate": "Customer support, Internal approvals",
    "current_tools": "Gmail, Slack, Salesforce",
    "main_challenge": "Scalability",
    "language": "en"
}

print("\n1. Testing Google Apps Script URL...")
print(f"   URL: {GOOGLE_SHEETS_WEBAPP_URL}")

try:
    print("\n2. Sending POST request with test data...")
    print(f"   Data: {json.dumps(test_lead, indent=2)}")
    
    response = requests.post(
        GOOGLE_SHEETS_WEBAPP_URL, 
        json=test_lead, 
        timeout=10,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\n3. Response received:")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Check your Google Sheet - there should be a new row!")
    else:
        print(f"\n❌ FAILED! Status code: {response.status_code}")
        
except requests.exceptions.Timeout:
    print("\n❌ ERROR: Request timed out after 10 seconds")
except requests.exceptions.RequestException as e:
    print(f"\n❌ ERROR: Network error - {e}")
except Exception as e:
    print(f"\n❌ ERROR: Unexpected error - {e}")

print("\n" + "=" * 60)
