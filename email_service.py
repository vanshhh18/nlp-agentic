import os
import requests
from dotenv import load_dotenv
from llm.groq_llm import llm

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")


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

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": FROM_EMAIL,
                "to": [receiver_email],
                "subject": f"Support Ticket Created - #{ticket_id}",
                "text": body,
            },
            timeout=15,
        )

        if response.status_code in (200, 201):
            print(f"Email sent successfully. ID: {response.json().get('id')}")
        else:
            print(f"Email sending failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Email sending failed: {e}")
