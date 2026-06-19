from rag.retriever import retriever
from llm.groq_llm import llm


def billing_agent(state):

    question = state["ticket"]

    docs = retriever.invoke(question)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a billing support assistant.

Question:
{question}

Context:
{context}

Answer professionally.
"""

    response = llm.invoke(prompt)

    state["assigned_team"] = "Billing Team"

    state["response"] = response.content

    return state