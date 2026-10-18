#!/usr/bin/env python3
"""
SC03 Step 4: Compare a training-only majority baseline with Step 3 ANN.
Run this file with VS Code's 'Run Python File' button or terminal.
Meets Student Master Guide Step 4 Requirements (Actions 5, 6, 7 & Appendix C).
The comparison uses the saved Step 3 predictions; it does not retrain or tune the ANN.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "data" / "reports"
RESULTS_DIR = PROJECT_ROOT / "results"

FEATURES = [
    "attendance_pct",
    "assessment_pct",
    "assignment_pct",
    "engagement_score",
    "prior_performance_pct",
]
TARGET = "risk_label"
CLASSES = ["low", "medium", "high"]
METRICS = ("accuracy", "precision", "recall", "f1_score")


def read_checked_csv(path: Path, required_columns: list) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. Finish Step 2 and Step 3 first.")
    frame = pd.read_csv(path)
    missing = [name for name in required_columns if name not in frame.columns]
    if missing:
        raise ValueError(f"{path.name} is missing columns: {missing}")
    if frame[required_columns].isna().any().any():
        raise ValueError(f"{path.name} contains blank required values.")
    return frame


def check_valid_labels(values, description: str):
    labels = set(pd.Series(values).unique())
    if not labels.issubset(set(CLASSES)):
        raise ValueError(f"{description} must contain only labels {CLASSES}: {labels}")


def score(actual, predicted, split: str, method: str) -> dict:
    return {
        "split": split,
        "method": method,
        "rows": len(actual),
        "accuracy": round(float(accuracy_score(actual, predicted)), 4),
        "precision": round(float(precision_score(actual, predicted, average="macro", zero_division=0)), 4),
        "recall": round(float(recall_score(actual, predicted, average="macro", zero_division=0)), 4),
        "f1_score": round(float(f1_score(actual, predicted, average="macro", zero_division=0)), 4),
    }


def make_chart(metric_rows: pd.DataFrame) -> Path:
    figure, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for axis, split in zip(axes, ("validation", "test")):
        section = metric_rows.set_index(["split", "method"])
        baseline = section.loc[(split, "Majority baseline"), list(METRICS)].astype(float)
        ann = section.loc[(split, "Step 3 ANN"), list(METRICS)].astype(float)
        positions = range(len(METRICS))
        axis.bar(
            [x - 0.18 for x in positions],
            baseline,
            width=0.36,
            label="Baseline",
            color="#777777",
        )
        axis.bar(
            [x + 0.18 for x in positions],
            ann,
            width=0.36,
            label="ANN",
            color="#1f77b4",
        )
        axis.set_xticks(list(positions))
        axis.set_xticklabels(["Accuracy", "Precision", "Recall", "F1"])
        axis.set_ylim(0, 1.05)
        axis.set_title(f"{split.title()} Split", fontweight="bold")
        axis.grid(axis="y", alpha=0.25)
    axes[0].set_ylabel("Score (higher is better)")
    axes[1].legend(loc="upper right")
    figure.suptitle("SC03 Step 4: Academic Intervention — Same Data, Two Methods", fontsize=13, fontweight="bold")
    figure.tight_layout()
    chart_path = RESULTS_DIR / "step4_baseline_vs_ann.png"
    figure.savefig(chart_path, dpi=180)
    plt.close(figure)
    return chart_path


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    train = read_checked_csv(DATA_DIR / "train.csv", FEATURES + [TARGET])
    check_valid_labels(train[TARGET], "Training target")
    counts = train[TARGET].value_counts()
    
    # Majority class chosen strictly from training labels only
    majority_label = counts.idxmax()

    print("SC03 STEP 4 - FAIR BASELINE COMPARISON")
    print(f"Training rows: {len(train)}; class counts: {counts.to_dict()}")
    print(f"Majority baseline always predicts: '{majority_label}'")

    metric_rows = []
    comparison_rows = []

    for split in ("validation", "test"):
        actual = read_checked_csv(DATA_DIR / f"{split}.csv", FEATURES + [TARGET])
        saved = read_checked_csv(
            REPORT_DIR / f"step3_{split}_predictions.csv",
            FEATURES + [TARGET, "ann_prediction"],
        )
        if len(saved) != len(actual):
            raise ValueError(f"{split}: Step 3 predictions have a different row count.")
        
        try:
            pd.testing.assert_frame_equal(
                actual[FEATURES + [TARGET]].reset_index(drop=True),
                saved[FEATURES + [TARGET]].reset_index(drop=True),
                check_dtype=False,
                check_exact=False,
                rtol=1e-8,
                atol=1e-10,
            )
        except AssertionError as error:
            raise ValueError(
                f"{split}: Step 3 predictions do not match the Step 2 split. "
                "Do not compare different rows or reorder the CSV files."
            ) from error

        check_valid_labels(actual[TARGET], f"{split} target")
        check_valid_labels(saved["ann_prediction"], f"{split} ANN predictions")

        baseline_predictions = pd.Series(majority_label, index=actual.index)
        baseline_result = score(
            actual[TARGET], baseline_predictions, split, "Majority baseline"
        )
        ann_result = score(
            actual[TARGET], saved["ann_prediction"], split, "Step 3 ANN"
        )
        metric_rows.extend((baseline_result, ann_result))

        for metric in METRICS:
            comparison_rows.append({
                "split": split,
                "metric": metric,
                "baseline": baseline_result[metric],
                "ann": ann_result[metric],
                "ann_minus_baseline": round(
                    ann_result[metric] - baseline_result[metric], 4
                ),
            })

        # Save paired predictions
        paired = actual[FEATURES + [TARGET]].copy()
        paired["baseline_prediction"] = majority_label
        paired["ann_prediction"] = saved["ann_prediction"].to_numpy()
        paired.to_csv(REPORT_DIR / f"step4_{split}_paired_predictions.csv", index=False)

    metrics = pd.DataFrame(metric_rows)
    comparison = pd.DataFrame(comparison_rows)

    metrics.to_csv(REPORT_DIR / "step4_baseline_metrics.csv", index=False)
    comparison.to_csv(REPORT_DIR / "step4_comparison.csv", index=False)
    chart_path = make_chart(metrics)

    print("\nBoth methods use exactly the same validation/test rows.")
    print(metrics.to_string(index=False))
    print("\nANN minus baseline (positive means ANN is higher):")
    print(comparison.to_string(index=False))
    print(f"\nSaved chart: {chart_path}")
    print(f"Saved CSV evidence: {REPORT_DIR}")
    print("STEP 4 COMPLETED")
    return metrics, comparison


if __name__ == "__main__":
    main()
