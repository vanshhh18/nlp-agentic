def technical_agent(state):

    state["assigned_team"] = "Technical Team"

    state["response"] = (
        "Your software issue has been forwarded "
        "to Technical Support."
    )

    return state