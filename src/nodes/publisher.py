import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown

from state import NewsletterState

def publisher_node(state: NewsletterState):
    # Fetching environment variables set in GitHub Secrets
    sender = os.getenv("SENDER_EMAIL")
    pw = os.getenv("SENDER_PASSWORD")
    
    html = markdown.markdown(state['newsletter_draft'])
    msg = MIMEMultipart()
    msg['Subject'] = f"📊 DS Pulse: {state['topic']}"
    msg['From'] = sender
    msg['To'] = sender # Sending to yourself
    msg.attach(MIMEText(f"<html><body>{html}</body></html>", 'html'))