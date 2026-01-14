from llama_index.core.prompts import PromptTemplate

RAG_CONTEXT_PROMPT = PromptTemplate(
    """
You are an AI assistant answering user questions using retrieved document context.

Conversation Summary:
{conversation_summary}

Recent Conversation:
{recent_messages}

Retrieved Document Context:
{retrieved_context}

User Question:
{user_query}

Answer the question using ONLY the information provided above.
If the answer is not contained in the context, say so explicitly.
"""
)
