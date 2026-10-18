#!/usr/bin/env python3
"""
Step 1 Data Validation Script — SC03 Academic Intervention
Validates starter data structure, data types, value ranges, and target categories.
Prints 'STEP 1 DATA CHECK PASSED' upon successful verification.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = PROJECT_ROOT / "data" / "sample_input.csv"

REQUIRED_COLUMNS = [
    "record_id",
    "attendance_pct",
    "assessment_pct",
    "assignment_pct",
    "engagement_score",
    "prior_performance_pct",
    "risk_label",
]

NUMERIC_COLUMNS = [
    "attendance_pct",
    "assessment_pct",
    "assignment_pct",
    "engagement_score",
    "prior_performance_pct",
]

VALID_RISK_LABELS = {"low", "medium", "high"}


def validate_dataset(filepath: Path) -> pd.DataFrame:
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    df = pd.read_csv(filepath)
    print(f"Loaded: {filepath.name}")
    print(f"shape: {df.shape}")
    print(f"columns: {list(df.columns)}")

    # 1. Check required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    assert not missing_cols, f"VALIDATION FAILED: Missing required columns: {missing_cols}"

    # 2. Check for missing values in required columns
    null_counts = df[REQUIRED_COLUMNS].isna().sum()
    if null_counts.any():
        failing_cols = null_counts[null_counts > 0].to_dict()
        assert False, f"VALIDATION FAILED: Missing values found in columns: {failing_cols}"

    # 3. Check data types for numeric columns
    for col in NUMERIC_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df[col]):
            assert False, f"VALIDATION FAILED: Column '{col}' must be numeric"

    # 4. Check domain range constraints
    assert (
        (df["attendance_pct"] >= 0.0) & (df["attendance_pct"] <= 100.0)
    ).all(), "VALIDATION FAILED: attendance_pct values must be between 0 and 100"

    assert (
        (df["assessment_pct"] >= 0.0) & (df["assessment_pct"] <= 100.0)
    ).all(), "VALIDATION FAILED: assessment_pct values must be between 0 and 100"

    assert (
        (df["assignment_pct"] >= 0.0) & (df["assignment_pct"] <= 100.0)
    ).all(), "VALIDATION FAILED: assignment_pct values must be between 0 and 100"

    assert (
        (df["engagement_score"] >= 0.0) & (df["engagement_score"] <= 10.0)
    ).all(), "VALIDATION FAILED: engagement_score values must be between 0 and 10"

    assert (
        (df["prior_performance_pct"] >= 0.0) & (df["prior_performance_pct"] <= 100.0)
    ).all(), "VALIDATION FAILED: prior_performance_pct values must be between 0 and 100"

    # 5. Check valid target labels
    unique_labels = set(df["risk_label"].unique())
    invalid_labels = unique_labels - VALID_RISK_LABELS
    assert not invalid_labels, f"VALIDATION FAILED: Invalid risk labels found: {invalid_labels}"

    # 6. Check unique record IDs
    assert (
        df["record_id"].nunique() == len(df)
    ), "VALIDATION FAILED: Duplicate record_id values detected"

    print("STEP 1 DATA CHECK PASSED")
    return df


if __name__ == "__main__":
    target_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    try:
        validate_dataset(target_path)
    except AssertionError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during validation: {e}", file=sys.stderr)
        sys.exit(1)
