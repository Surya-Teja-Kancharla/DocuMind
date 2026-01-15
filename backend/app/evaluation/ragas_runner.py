from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    context_precision,
    context_recall,
)
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from backend.app.evaluation.evaluation_dataset import build_evaluation_dataset
import os
os.environ["RAGAS_MAX_WORKERS"] = "1"


def run_ragas_evaluation():
    dataset = build_evaluation_dataset()

    # Groq LLM (OpenAI-compatible)
    llm = ChatOpenAI(
        model="openai/gpt-oss-20b",
        openai_api_key=os.environ["GROQ_API_KEY"],
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0,
    )

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
