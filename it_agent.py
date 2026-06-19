from rag.retriever import retriever
from llm.groq_llm import llm


def it_agent(state):

    question = state["ticket"]

    docs = retriever.invoke(question)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an IT support assistant.

Question:
{question}

Context:
{context}

Give a professional answer.
"""

    response = llm.invoke(prompt)

    state["assigned_team"] = "IT Team"

    state["response"] = response.content

    return state