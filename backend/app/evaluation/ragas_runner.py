from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    context_precision,
    context_recall,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.app.evaluation.evaluation_dataset import build_evaluation_dataset
import os


def run_ragas_evaluation():
    dataset = build_evaluation_dataset()

    # Gemini LLM (judge)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.environ["GEMINI_API_KEY"],
        temperature=0,
    )

    # Local embeddings (NO OpenAI)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    results = evaluate(
        dataset,
        metrics=[
            faithfulness,
            context_precision,
            context_recall,
        ],
        llm=llm,
        embeddings=embeddings, 
    )

    return results
