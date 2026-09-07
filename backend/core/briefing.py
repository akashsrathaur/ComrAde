import os
import imaplib
import email
import requests
from dotenv import load_dotenv

load_dotenv()

def get_unread_emails() -> str:
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
    
    if not gmail_user or not gmail_pass or gmail_user == "your_email@gmail.com":
        return ""
        
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(gmail_user, gmail_pass)
        mail.select('inbox')
        
        # Search for UNSEEN emails
        status, messages = mail.search(None, 'UNSEEN')
        if status == 'OK':
            email_ids = messages[0].split()
            count = len(email_ids)
            if count == 0:
                return ""
            elif count == 1:
                return "You have 1 new unread email."
            else:
                return f"You have {count} new unread emails."
        return ""
    except Exception as e:
        print(f"Gmail Briefing Error: {e}")
        return ""

def get_github_notifications() -> str:
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token or github_token == "your_github_personal_access_token":
        return ""
        
    try:
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get("https://api.github.com/notifications", headers=headers)
        if response.status_code == 200:
            notifications = response.json()
            count = len(notifications)
            if count == 0:
                return ""
            elif count == 1:
                return "You have 1 unread GitHub notification."
            else:
                return f"You have {count} unread GitHub notifications."
        return ""
    except Exception as e:
        print(f"GitHub Briefing Error: {e}")
        return ""

def get_morning_briefing() -> str:
    """Returns a string summarizing the user's unread notifications across platforms."""
    briefing_parts = []
    
    emails = get_unread_emails()
    if emails:
        briefing_parts.append(emails)
        
    github = get_github_notifications()
    if github:
        briefing_parts.append(github)
        
    if briefing_parts:
        return " By the way, " + " ".join(briefing_parts)
    
    return ""
