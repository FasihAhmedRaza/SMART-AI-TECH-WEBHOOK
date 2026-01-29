import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import (
    GOOGLE_SHEETS_WEBAPP_URL,
    EMAIL_NOTIFICATIONS_ENABLED,
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_FROM,
    EMAIL_PASSWORD,
    EMAIL_TO
)

def send_consultation_lead_to_webhook(lead_data):
    """
    Sends consultation lead data to Google Sheets via Zapier webhook.
    
    Args:
        lead_data (dict): Contains name, email, objective, processes_to_automate, 
                         current_tools, main_challenge, language
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"Debug: Sending consultation lead -> {lead_data}")
    
    try:
        if "YOUR_ID" in GOOGLE_SHEETS_WEBAPP_URL or "YOUR_HOOK" in GOOGLE_SHEETS_WEBAPP_URL:
            print("WARNING: GOOGLE_SHEETS_WEBHOOK_URL is not configured. Logging data locally.")
            print(f"Lead Data: {lead_data}")
            return True  # Graceful fallback
        
        response = requests.post(GOOGLE_SHEETS_WEBAPP_URL, json=lead_data, timeout=10)
        response.raise_for_status()
        print(f"SUCCESS: Consultation lead sent. Response: {response.text}")
        return True
    except requests.exceptions.Timeout:
        print("ERROR: Request timeout while sending consultation lead.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to send consultation lead -> {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error -> {e}")
        return False


def send_email_notification(lead_data):
    """
    Sends an email notification via Gmail SMTP when a new consultation lead is received.
    
    NOTE: This works locally but may be blocked on Railway (use in background task to prevent timeout)
    
    Args:
        lead_data (dict): Contains lead information
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    if not EMAIL_NOTIFICATIONS_ENABLED:
        print("ℹ️ Email notifications are disabled (set EMAIL_NOTIFICATIONS_ENABLED=true to enable).")
        return True
    
    if not EMAIL_FROM or not EMAIL_PASSWORD or not EMAIL_TO:
        print("⚠️ WARNING: Email credentials not configured in .env file. Skipping email notification.")
        print("   Required: EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO")
        return False
    
    try:
        print(f"📧 Sending email notification via SMTP to {EMAIL_TO}...")
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🔔 New Lead: {lead_data.get('name', 'Unknown')} - The Smart AI Tech"
        msg['From'] = f"The Smart AI Tech <{EMAIL_FROM}>"
        msg['To'] = EMAIL_TO
        return True
    
    if not EMAIL_FROM or not EMAIL_PASSWORD or not EMAIL_TO:
        print("⚠️ WARNING: Email credentials not configured in .env file. Skipping email notification.")
        print("   Required: EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO")
        return False
    
    try:
        print(f"📧 Sending email notification to {EMAIL_TO}...")
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🔔 New Lead: {lead_data.get('name', 'Unknown')} - The Smart AI Tech"
        msg['From'] = f"The Smart AI Tech <{EMAIL_FROM}>"
        msg['To'] = EMAIL_TO
        
        # Create HTML email body
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}
                .container {{ max-width: 650px; margin: 30px auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 600; }}
                .header p {{ margin: 10px 0 0 0; font-size: 14px; opacity: 0.9; }}
                .content {{ padding: 30px; background-color: #ffffff; }}
                .lead-info {{ background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                .field {{ margin: 18px 0; padding: 15px; background-color: white; border-left: 4px solid #667eea; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
                .field-label {{ font-weight: 600; color: #2d3748; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
                .field-value {{ color: #4a5568; font-size: 15px; line-height: 1.6; }}
                .highlight {{ background-color: #fef3c7; padding: 2px 6px; border-radius: 3px; }}
                .footer {{ background-color: #f7fafc; padding: 25px; text-align: center; border-top: 1px solid #e2e8f0; }}
                .footer p {{ margin: 5px 0; color: #718096; font-size: 13px; }}
                .cta-button {{ display: inline-block; margin: 20px 0; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 6px; font-weight: 600; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-box {{ text-align: center; padding: 15px; background: white; border-radius: 8px; flex: 1; margin: 0 5px; }}
                .stat-number {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                .stat-label {{ font-size: 12px; color: #718096; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 New Consultation Lead!</h1>
                    <p>The Smart AI Tech - Automation Consultancy</p>
                </div>
                
                <div class="content">
                    <div class="lead-info">
                        <h2 style="margin-top: 0; color: #2d3748; font-size: 20px;">Lead Information</h2>
                        
                        <div class="field">
                            <div class="field-label">👤 Contact Name</div>
                            <div class="field-value"><strong>{lead_data.get('name', 'N/A')}</strong></div>
                        </div>
                        
                        <div class="field">
                            <div class="field-label">📧 Email Address</div>
                            <div class="field-value"><a href="mailto:{lead_data.get('email', '')}" style="color: #667eea; text-decoration: none;">{lead_data.get('email', 'N/A')}</a></div>
                        </div>
                        
                        <div class="field">
                            <div class="field-label">🎯 Business Objective</div>
                            <div class="field-value"><span class="highlight">{lead_data.get('objective', 'N/A')}</span></div>
                        </div>
                        
                        <div class="field">
                            <div class="field-label">⚙️ Processes to Automate</div>
                            <div class="field-value">{lead_data.get('processes_to_automate', 'N/A')}</div>
                        </div>
                        
                        <div class="field">
                            <div class="field-label">🔧 Current Tools & Systems</div>
                            <div class="field-value">{lead_data.get('current_tools', 'N/A')}</div>
                        </div>
                        
                        <div class="field">
                            <div class="field-label">⚡ Main Challenge</div>
                            <div class="field-value"><strong style="color: #e53e3e;">{lead_data.get('main_challenge', 'N/A')}</strong></div>
                        </div>
                        
                        <div class="stats">
                            <div class="stat-box">
                                <div class="stat-number">🌐</div>
                                <div class="stat-label">Language: {lead_data.get('language', 'en').upper()}</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-number">🕒</div>
                                <div class="stat-label">{lead_data.get('timestamp', 'N/A').split('T')[0]}</div>
                            </div>
                        </div>
                    </div>
                    
                    <p style="text-align: center; color: #4a5568; margin: 25px 0;">
                        <strong>Next Step:</strong> Review the lead details and prepare a custom automation proposal.
                    </p>
                </div>
                
                <div class="footer">
                    <p style="margin-bottom: 15px;"><strong>✅ Lead automatically saved to Google Sheet</strong></p>
                    <a href="https://docs.google.com/spreadsheets/d/1gWUilIZBU5IQ4cGtNpfcQx8gaa8uf4fCAP7i5L-uviQ/edit?gid=0#gid=0" class="cta-button" style="color: white;">View All Leads →</a>
                    <p style="margin-top: 20px;">This is an automated notification from The Smart AI Tech consultation bot.</p>
                    <p>© 2026 The Smart AI Tech. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send email via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email notification sent successfully to {EMAIL_TO}")
        print(f"   Subject: New Consultation Lead: {lead_data.get('name', 'Unknown')}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ ERROR: Email authentication failed.")
        print("   Check your EMAIL_FROM and EMAIL_PASSWORD in .env file.")
        print("   For Gmail: Use App Password (https://myaccount.google.com/apppasswords)")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ ERROR: SMTP error - {e}")
        print("   This usually means SMTP is blocked (Railway) or wrong credentials.")
        return False
    except ConnectionRefusedError:
        print(f"❌ ERROR: Cannot connect to SMTP server (connection refused)")
        print(f"   This is normal on Railway - SMTP port {SMTP_PORT} is blocked for security.")
        print("   Your lead is still saved to Google Sheet! Check there for all leads.")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to send email notification - {e}")
        print("   Your lead is still saved to Google Sheet! Email failed but data is safe.")
        return False
