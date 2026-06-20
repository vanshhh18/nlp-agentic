import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

from llm.groq_llm import llm

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(
        receiver_email,
        ticket_id,
        department,
        priority,
        user_ticket,
        ai_response):

    prompt = f"""
Write a professional customer support email.

Include:

1. Thank the customer for contacting us.
2. Mention Ticket ID: {ticket_id}
3. Mention Department: {department}
4. Mention Priority: {priority}
5. Briefly summarize the issue:
{user_ticket}

6. Mention the initial AI analysis:
{ai_response}

7. Assure the customer that our support team will investigate.

Keep the tone professional and friendly.
"""

    body = llm.invoke(prompt).content

    subject = f"Support Ticket Created - #{ticket_id}"

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.send_message(msg)

        print("Email sent successfully.")

    except Exception as e:

        print("Email sending failed:", e)
