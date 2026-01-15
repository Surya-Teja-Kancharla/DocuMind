from datasets import Dataset
from pathlib import Path
from backend.app.evaluation.qa_generator import generate_qa_pairs_for_document
from backend.app.services.retriever import retrieve_similar_chunks
from backend.app.services.context_assembler import assemble_context
from backend.app.services.llm import generate_answer


PARSED_DIR = Path("data/parsed")


def build_evaluation_dataset(
    max_docs: int = 3,
    questions_per_doc: int = 3
):
    """
    Build RAGAS-compatible evaluation dataset from ingested documents.
    """

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    document_ids = [
        file.stem for file in PARSED_DIR.glob("*.txt")
    ][:max_docs]

    for doc_id in document_ids:
        qa_pairs = generate_qa_pairs_for_document(
            document_id=doc_id,
            num_questions=questions_per_doc
        )

        for sample in qa_pairs:
            question = sample["question"]
            ground_truth = sample["answer"]
            doc_contexts = sample["contexts"]

            # Run RAG pipeline
            retrieved_nodes = retrieve_similar_chunks(question)

            rag_prompt = assemble_context(
                user_query=question,
                retrieved_nodes=retrieved_nodes,
                conversation_messages=[]
            )

            rag_answer = generate_answer(rag_prompt)

            questions.append(question)
            answers.append(rag_answer)
            contexts.append(doc_contexts)
            ground_truths.append(ground_truth)

    return Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })
