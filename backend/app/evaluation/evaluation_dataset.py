from datasets import Dataset

from backend.app.utils.document_loader import load_parsed_documents
from backend.app.evaluation.question_generator import (
    generate_questions,
    generate_reference_answer,
)
from backend.app.services.retriever import retrieve_similar_chunks
from backend.app.services.context_assembler import assemble_context
from backend.app.services.llm import generate_answer  # non-stream version


def build_evaluation_dataset(max_docs: int = 3, questions_per_doc: int = 3):
    """
    Dynamically build RAGAS evaluation dataset from ingested documents.
    """
    questions = []
    answers = []
    contexts = []
    ground_truths = []

    documents = load_parsed_documents()[:max_docs]

    for doc_context in documents:
        doc_questions = generate_questions(
            context=doc_context,
            n=questions_per_doc
        )

        for q in doc_questions:
            # Ground-truth answer
            gt = generate_reference_answer(q, doc_context)

            # RAG pipeline answer
            retrieved_nodes = retrieve_similar_chunks(q)
            rag_prompt = assemble_context(
                user_query=q,
                retrieved_nodes=retrieved_nodes,
                conversation_messages=[]
            )
            rag_answer = generate_answer(rag_prompt)

            questions.append(q)
            answers.append(rag_answer)
            contexts.append([doc_context])
            ground_truths.append(gt)

    return Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })
