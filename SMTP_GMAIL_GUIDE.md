# 📧 SMTP Email Setup (Gmail Only)

## Current Configuration

✅ **Your system uses Gmail SMTP:**
- SMTP Server: `smtp.gmail.com:587`
- Email From: `developer.fasih@gmail.com`
- Email To: `thisfasih@gmail.com, alex.gerardy@thesmartai.tech`

---

## Important: Railway Limitation

### Works ✅
- **Local development** (your computer)
- **ngrok testing** (your computer)
- **Any hosting that allows SMTP** (paid plans)

### Blocked ❌
- **Railway.app free tier** (blocks SMTP ports for security)
- Connection error: `[Errno 101] Network is unreachable`

**Why blocked?** Railway blocks outgoing SMTP to prevent spam/abuse.

---

## Your Current Setup

### What Happens:
```
1. Dialogflow conversation complete ✅
2. Webhook receives data (fast) ✅
3. Data saved to Google Sheet ✅
4. Background task tries to send email:
   
   LOCAL:   Email sent via Gmail ✅
   RAILWAY: Email blocked, error logged ❌ (but lead still saved!)
```

---

## Solution: Email Works Locally

### For Local Testing:
```bash
# Start your webhook locally
cd "C:\Users\thisf\OneDrive\Documents\Dialogflow CX\Python-dialogflow-CX--Webhook"
python run.py

# In another terminal, start ngrok
ngrok http 5000

# Update Dialogflow webhook URL to ngrok URL
# Test conversation - emails WILL work!
```

**Result:** Emails send perfectly! ✅

---

## On Railway (Production)

### Current Behavior:
1. ✅ Webhook responds fast (no timeout)
2. ✅ Lead saved to Google Sheet
3. ❌ Email fails (SMTP blocked)
4. ✅ Error logged: "connection refused"
5. ✅ Lead data is safe in Google Sheet

### What You See in Logs:
```
INFO: 💾 Saving consultation lead: John Doe (john@example.com)
INFO: 📧 Email notification scheduled in background (non-blocking)
❌ ERROR: Cannot connect to SMTP server (connection refused)
   This is normal on Railway - SMTP port 587 is blocked for security.
   Your lead is still saved to Google Sheet! Check there for all leads.
```

---

## Recommended Workflow

### Option 1: Use Google Sheet Notifications (Free) ⭐
1. All leads saved to Google Sheet automatically ✅
2. Check sheet daily for new leads
3. Use Google Sheets email alerts:
   - Extensions → Add-ons → Get add-ons
   - Search "Email Notifications"
   - Set up alert when new row added

### Option 2: Local Webhook + ngrok (Development)
- Run webhook on your computer
- Use ngrok for public URL
- Emails work perfectly!
- Good for testing/demos

### Option 3: Paid Railway Plan
- Railway Pro: ~$5/month
- May unblock SMTP (check their docs)
- Or use a different hosting platform

---

## Files Configuration

### .env (Already Configured) ✅
```env
EMAIL_NOTIFICATIONS_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=developer.fasih@gmail.com
EMAIL_PASSWORD=cwyolorbytntpflj
EMAIL_TO=thisfasih@gmail.com,alex.gerardy@thesmartai.tech
```

### Railway Variables (Same as .env)
All variables copied to Railway Dashboard → Variables

---

## Testing Email Locally

```bash
# Test webhook with email
cd "C:\Users\thisf\OneDrive\Documents\Dialogflow CX\Python-dialogflow-CX--Webhook"
python test_email.py

# Expected output:
Debug: Sending consultation lead → {...}
SUCCESS: Consultation lead sent.
📧 Sending email notification to thisfasih@gmail.com...
✅ Email notification sent successfully
```

---

## Current Code Structure

### Background Email Task ✅
**File:** [src/actions/save_lead.py](src/actions/save_lead.py)

```python
# Email sends in background (doesn't block webhook)
if success and background_tasks:
    background_tasks.add_task(send_email_in_background, lead_data)
    logger.info("📧 Email notification scheduled in background")
```

### SMTP Email Function ✅
**File:** [src/utils.py](src/utils.py)

```python
def send_email_notification(lead_data):
    # Try to send via Gmail SMTP
    # If blocked (Railway), logs error but doesn't crash
    # Lead data is always saved regardless
```

---

## Summary

| Environment | Webhook | Sheet Save | Email | Recommendation |
|-------------|---------|------------|-------|----------------|
| **Local + ngrok** | ✅ Fast | ✅ Works | ✅ Works | Use for testing |
| **Railway** | ✅ Fast | ✅ Works | ❌ Blocked | Use Sheet notifications |

---

## What To Do Now

### ✅ Your system is production-ready!

**All leads are captured and saved.**

For email notifications, choose one:

1. **Use Google Sheet** (free, reliable)
   - Set up Google Sheets email alerts
   - Check sheet daily

2. **Run locally for demos** (emails work)
   - Use ngrok for public URL
   - Perfect for client demos

3. **Switch hosting** (if emails critical)
   - Heroku, AWS, Google Cloud
   - Check if they allow SMTP

---

**The important part (lead capture) works perfectly! 🎉**

Email is just a notification - the data is safe in Google Sheets.
