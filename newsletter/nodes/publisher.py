import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
import smtplib
from langchain_core.runnables import RunnableConfig

from state import NewsletterState

def publisher_node(state: NewsletterState, config: RunnableConfig):
    """
    """
    logging.info("Starting publisher node ...")
    # Fetching environment variables set in GitHub Secrets
    configurable = config.get("configurable", {})
    sender = configurable.get("SENDER_EMAIL", None)
    pw = configurable.get("SENDER_PASSWORD", None)
    receiver = configurable.get("RECEIVER_EMAIL", None)
    html = markdown.markdown(state['newsletter_draft'])
    msg = MIMEMultipart()
    msg['Subject'] = f"📊 DS Pulse: {state['topic']} - {state['subtopic']}"
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText(f"<html><body>{html}</body></html>", 'html'))
    logging.info("Sending email via SMTP ...")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, pw)
        server.send_message(msg)
    return {"steps_taken": ["publisher_complete"]}