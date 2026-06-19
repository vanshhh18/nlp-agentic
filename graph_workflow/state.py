from typing_extensions import TypedDict

class TicketState(TypedDict):
    ticket: str
    department: str
    priority: str
    assigned_team: str
    response: str