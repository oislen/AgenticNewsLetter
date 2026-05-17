import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
import smtplib
from langchain_core.runnables import RunnableConfig

from state import NewsletterState

def publisher_node(state: NewsletterState, config: RunnableConfig):
    # Fetching environment variables set in GitHub Secrets
    sender = config["SENDER_EMAIL"]
    pw = config["SENDER_PASSWORD"]
    receiver = config["RECEIVER_EMAIL"]
    html = markdown.markdown(state['newsletter_draft'])
    msg = MIMEMultipart()
    msg['Subject'] = f"📊 DS Pulse: {state['topic']} - {state['subtopic']}"
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText(f"<html><body>{html}</body></html>", 'html'))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, pw)
        server.send_message(msg)
    return {"steps_taken": ["publisher_complete"]}