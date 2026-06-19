# from fastapi import FastAPI
# from pydantic import BaseModel
# import joblib

# from graph_workflow.workflow import graph

# app = FastAPI()

# model = joblib.load("ticket_classifier.pkl")
# vectorizer = joblib.load("tfidf_vectorizer.pkl")

# dept_dict = {
#     0: 'Billing and Payments',
#     1: 'Customer Service',
#     2: 'General Inquiry',
#     3: 'Human Resources',
#     4: 'IT Support',
#     5: 'Product Support',
#     6: 'Returns and Exchanges',
#     7: 'Sales and Pre-Sales',
#     8: 'Service Outages and Maintenance',
#     9: 'Technical Support'
# }

# priority_dict = {
#     0: 'high',
#     1: 'low',
#     2: 'medium'
# }

# class Ticket(BaseModel):
#     text: str

# @app.post("/predict")
# def predict(ticket: Ticket):

#     X = vectorizer.transform([ticket.text])
#     pred = model.predict(X)

#     department = dept_dict[int(pred[0][0])]
#     priority = priority_dict[int(pred[0][1])]

#     result = graph.invoke(
#         {
#             "ticket": ticket.text,
#             "department": department,
#             "priority": priority
#         }
#     )

#     return result

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uuid

from graph_workflow.workflow import graph
from email_service import send_email

app = FastAPI()

model = joblib.load("ticket_classifier.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")


dept_dict = {
    0: 'Billing and Payments',
    1: 'Customer Service',
    2: 'General Inquiry',
    3: 'Human Resources',
    4: 'IT Support',
    5: 'Product Support',
    6: 'Returns and Exchanges',
    7: 'Sales and Pre-Sales',
    8: 'Service Outages and Maintenance',
    9: 'Technical Support'
}

priority_dict = {
    0: 'high',
    1: 'low',
    2: 'medium'
}


class Ticket(BaseModel):
    text: str
    email: str


@app.post("/predict")
def predict(ticket: Ticket):

    X = vectorizer.transform([ticket.text])

    pred = model.predict(X)

    department = dept_dict[int(pred[0][0])]
    priority = priority_dict[int(pred[0][1])]

    result = graph.invoke(
        {
            "ticket": ticket.text,
            "department": department,
            "priority": priority
        }
    )
    
    ticket_id = str(uuid.uuid4())[:8]

    send_email(
        ticket.email,
        ticket_id,
        department,
        priority,
        ticket.text,
        result["response"]
    )

    result["ticket_id"] = ticket_id

    return result
