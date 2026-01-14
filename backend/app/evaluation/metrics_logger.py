import pandas as pd
from pathlib import Path

from backend.app.evaluation.ragas_runner import run_ragas_evaluation


RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def main():
    results = run_ragas_evaluation()
    df = results.to_pandas()

    output_path = RESULTS_DIR / "ragas_results.csv"
    df.to_csv(output_path, index=False)

    print(f"Evaluation results saved to: {output_path}")


if __name__ == "__main__":
    main()
