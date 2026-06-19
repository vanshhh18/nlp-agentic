from langgraph.graph import StateGraph, START, END

from graph_workflow.state import TicketState
from graph_workflow.router import route_ticket

from agents.it_agent import it_agent
from agents.billing_agent import billing_agent
from agents.hr_agent import hr_agent
from agents.tech_agent import technical_agent

workflow = StateGraph(TicketState)

# Add nodes
workflow.add_node("it_agent", it_agent)
workflow.add_node("billing_agent", billing_agent)
workflow.add_node("hr_agent", hr_agent)
workflow.add_node("technical_agent", technical_agent)

# Conditional routing
workflow.add_conditional_edges(
    START,
    route_ticket,
    {
        "it_agent": "it_agent",
        "billing_agent": "billing_agent",
        "hr_agent": "hr_agent",
        "technical_agent": "technical_agent"
    }
)

# End edges
workflow.add_edge("it_agent", END)
workflow.add_edge("billing_agent", END)
workflow.add_edge("hr_agent", END)
workflow.add_edge("technical_agent", END)

# Compile
graph = workflow.compile()