def route_ticket(state):

    department = state["department"]

    if department == "IT Support":
        return "it_agent"

    elif department == "Billing and Payments":
        return "billing_agent"

    elif department == "Human Resources":
        return "hr_agent"

    else:
        return "technical_agent"