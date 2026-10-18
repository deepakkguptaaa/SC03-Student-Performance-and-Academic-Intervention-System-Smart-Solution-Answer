#!/usr/bin/env python3
"""
SC03 Step 3: Train an Artificial Neural Network (ANN) for Academic Intervention.
Meets Student Master Guide Step 3 Requirements.
Trains on data/processed/train.csv, evaluates on validation.csv and test.csv,
saves loss curve, confusion matrices, prediction CSVs, and model artifacts.
"""

from pathlib import Path
import json
import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
)
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "data" / "reports"
MODEL_DIR = PROJECT_ROOT / "models"
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
RANDOM_SEED = 42


def load_split(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv"
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. Complete Step 2 first.")
    frame = pd.read_csv(path)
    required = FEATURES + [TARGET]
    missing = [c for c in required if c not in frame.columns]
    if missing:
        raise ValueError(f"{name}.csv is missing required columns: {missing}")
    if frame[required].isna().any().any():
        raise ValueError(f"{name}.csv contains blank required values.")
    return frame


def metric_row(y_true, y_pred, split_name: str) -> dict:
    return {
        "split": split_name,
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, average="macro", zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, average="macro", zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred, average="macro", zero_division=0)), 4),
    }


def save_confusion_matrix(y_true, y_pred, split_name: str) -> None:
    matrix = confusion_matrix(y_true, y_pred, labels=CLASSES)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matrix, cmap="Blues")
    fig.colorbar(im, ax=ax)
    ax.set(
        title=f"SC03 ANN Confusion Matrix ({split_name.title()} Split)",
        xlabel="Predicted Label",
        ylabel="Actual Label",
        xticks=[0, 1, 2],
        yticks=[0, 1, 2],
        xticklabels=CLASSES,
        yticklabels=CLASSES,
    )
    for r in range(len(CLASSES)):
        for c in range(len(CLASSES)):
            ax.text(
                c, r, str(matrix[r, c]),
                ha="center", va="center",
                color="white" if matrix[r, c] > matrix.max() / 2 else "black",
                fontweight="bold"
            )
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / f"step3_ann_{split_name}_confusion_matrix.png", dpi=180)
    plt.close(fig)


def train_and_evaluate():
    for d in [REPORT_DIR, MODEL_DIR, RESULTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    print("SC03 STEP 3 - BUILD AND TRAIN ANN MODEL")
    print("-" * 50)
    train_data = load_split("train")
    validation_data = load_split("validation")
    test_data = load_split("test")

    print(f"Training rows: {len(train_data)}")
    print(f"Validation rows: {len(validation_data)}")
    print(f"Test rows: {len(test_data)}")

    X_train, y_train = train_data[FEATURES], train_data[TARGET]
    X_val, y_val = validation_data[FEATURES], validation_data[TARGET]
    X_test, y_test = test_data[FEATURES], test_data[TARGET]

    # Build Pipeline: StandardScaler + Multi-Layer Perceptron Classifier
    ann_model = Pipeline([
        ("scaler", StandardScaler()),
        ("ann", MLPClassifier(
            hidden_layer_sizes=(16, 8),
            activation="relu",
            solver="adam",
            learning_rate_init=0.001,
            max_iter=400,
            early_stopping=True,
            validation_fraction=0.15,
            n_iter_no_change=25,
            random_state=RANDOM_SEED,
        )),
    ])

    print("\nFitting ANN model...")
    ann_model.fit(X_train, y_train)
    trained_ann = ann_model.named_steps["ann"]
    print(f"Training completed in {trained_ann.n_iter_} iterations.")
    print(f"Final training loss: {round(trained_ann.loss_, 5)}")

    # Plot & save loss curve
    losses = trained_ann.loss_curve_
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(range(1, len(losses) + 1), losses, marker="o", markersize=2, color="#1f77b4")
    ax.set_title("ANN Training Loss Curve — SC03 Academic Intervention")
    ax.set_xlabel("Training Iteration (Epoch)")
    ax.set_ylabel("Loss")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "step3_ann_loss_curve.png", dpi=180)
    plt.close(fig)

    # Evaluate validation
    val_preds = ann_model.predict(X_val)
    val_metrics = metric_row(y_val, val_preds, "validation")
    save_confusion_matrix(y_val, val_preds, "validation")

    # Evaluate test
    test_preds = ann_model.predict(X_test)
    test_metrics = metric_row(y_test, test_preds, "test")
    save_confusion_matrix(y_test, test_preds, "test")

    metrics_df = pd.DataFrame([val_metrics, test_metrics])
    metrics_path = REPORT_DIR / "step3_ann_metrics.csv"
    metrics_df.to_csv(metrics_path, index=False)

    print("\nModel Evaluation Summary:")
    print(metrics_df.to_string(index=False))

    # Save detailed classification reports
    cls_reports = {
        "validation": classification_report(y_val, val_preds, output_dict=True, zero_division=0),
        "test": classification_report(y_test, test_preds, output_dict=True, zero_division=0),
    }
    (REPORT_DIR / "step3_classification_reports.json").write_text(
        json.dumps(cls_reports, indent=2), encoding="utf-8"
    )

    # Save prediction CSVs
    for split_name, split_df, preds in [
        ("validation", validation_data, val_preds),
        ("test", test_data, test_preds),
    ]:
        out_df = split_df.copy()
        out_df["ann_prediction"] = preds
        probs = ann_model.predict_proba(split_df[FEATURES])
        for idx, cls in enumerate(ann_model.classes_):
            out_df[f"ann_prob_{cls}"] = probs[:, idx].round(4)
        out_df.to_csv(REPORT_DIR / f"step3_{split_name}_predictions.csv", index=False)

    # Save model and metadata
    model_file = MODEL_DIR / "ann_student_performance.pkl"
    with open(model_file, "wb") as f:
        pickle.dump(ann_model, f)

    metadata = {
        "technique": "Feed-forward Neural Network (ANN) / MLPClassifier",
        "architecture": "5 inputs -> 16 hidden -> 8 hidden -> 3 output classes",
        "features": FEATURES,
        "target": TARGET,
        "classes": list(ann_model.classes_),
        "random_seed": RANDOM_SEED,
        "iterations": int(trained_ann.n_iter_),
        "final_loss": round(float(trained_ann.loss_), 5),
        "metrics": {
            "validation": val_metrics,
            "test": test_metrics,
        },
    }
    (MODEL_DIR / "ann_model_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    print("\nSaved Step 3 evidence files:")
    print(f"  - Model: {model_file.relative_to(PROJECT_ROOT)}")
    print(f"  - Metrics: {metrics_path.relative_to(PROJECT_ROOT)}")
    print(f"  - Predictions: data/reports/step3_validation_predictions.csv and step3_test_predictions.csv")
    print(f"  - Plots: results/step3_ann_loss_curve.png and confusion matrices")
    print("STEP 3 COMPLETED SUCCESSFULLY")
    return ann_model, metrics_df


if __name__ == "__main__":
    train_and_evaluate()
