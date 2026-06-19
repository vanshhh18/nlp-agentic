def hr_agent(state):

    state["assigned_team"] = "HR Team"

    state["response"] = (
        "Your request has been sent to Human Resources."
    )

    return state