# Step 4 — Fair Comparison Report

## Team and Project

- **Project:** SC03: Student Performance and Academic Intervention System
- **Team Name:** Smart Solution Answer
- **Team Members:**
  - Deepak Gupta (Team Lead / Repository & Backend Lead)
  - Himanshu Rai (Data & Machine Learning Lead)
  - Anish Kumar Singh (Baseline & Soft Computing Lead)
  - Arvant Deshwal (Testing & UI Lead)
- **Repository Branch:** `step-4-baseline`

---

## Question

*On the same held-out validation and test rows, does the Step 3 ANN predict student academic risk categories (`low`, `medium`, `high`) better than a simple training-majority baseline?*

This question was formulated before inspecting the held-out evaluation splits to preserve objective comparison integrity.

---

## Data and Scenarios

- **Source and Citation:** Higher-education learning analytics patterns (12,000 unique records; non-circular latent aptitude generation model).
- **Training Data:** 8,400 records in `data/processed/train.csv` (70% partition).
- **Validation Data:** 1,800 records in `data/processed/validation.csv` (15% partition).
- **Test Data:** 1,800 records in `data/processed/test.csv` (15% held-out partition).
- **Input Features:** `attendance_pct`, `assessment_pct`, `assignment_pct`, `engagement_score`, `prior_performance_pct`.
- **Target Feature:** `risk_label` (`low`, `medium`, `high`).
- **Generated Scenarios:** 1,200 separate testing scenarios in `data/generated/generated_student_performance_test_scenarios.csv`, strictly reserved for stress testing and excluded from model splits.

---

## Baseline Rule

Count `risk_label` frequencies in `data/processed/train.csv` only:
- Class counts in training: `low` = 3,737 (44.49%), `high` = 2,468 (29.38%), `medium` = 2,195 (26.13%).
- Rule: Always predict the most common training class: `'low'`.
- Strict constraint: The rule was determined strictly from training data and never accessed validation or test labels.

---

## Fair-Comparison Checks

- [x] **Same Question and Units:** Both baseline and ANN output discrete risk categories (`low`, `medium`, `high`) from the same 5 input indicators.
- [x] **Identical Held-Out Rows:** Both methods are evaluated on the exact same 1,800 validation rows and 1,800 test rows.
- [x] **Row-Level Verification:** `src/compare_baseline.py` programmatically verifies row count, feature columns, and true labels using `pd.testing.assert_frame_equal`.
- [x] **No Test Leakage:** The baseline rule and ANN hyperparameter settings were determined before evaluating the test set.
- [x] **Pre-Selected Multi-Class Metrics:** Accuracy, Macro Precision, Macro Recall, and Macro F1 were defined prior to score comparison.

---

## Results

The table below reports measured values from `data/reports/step4_baseline_metrics.csv`. Precision, recall, and F1 use macro-averaging across all three classes (`low`, `medium`, `high`):

| Split | Method | Rows | Accuracy | Precision (Macro) | Recall (Macro) | F1 Score (Macro) |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| **Validation** | Majority baseline | 1,800 | 0.4450 | 0.1483 | 0.3333 | 0.2053 |
| **Validation** | Step 3 ANN | 1,800 | 0.8378 | 0.8241 | 0.8206 | 0.8223 |
| **Test** | Majority baseline | 1,800 | 0.4450 | 0.1483 | 0.3333 | 0.2053 |
| **Test** | Step 3 ANN | 1,800 | 0.8383 | 0.8238 | 0.8218 | 0.8227 |

### Metric Differences (`ANN - Baseline` from `data/reports/step4_comparison.csv`):

| Split | Metric | Baseline Score | ANN Score | Difference (Score Points) |
| :--- | :--- | ---: | ---: | ---: |
| **Validation** | Accuracy | 0.4450 | 0.8378 | **+0.3928** |
| **Validation** | Macro Precision | 0.1483 | 0.8241 | **+0.6758** |
| **Validation** | Macro Recall | 0.3333 | 0.8206 | **+0.4873** |
| **Validation** | Macro F1 | 0.2053 | 0.8223 | **+0.6170** |
| **Test** | Accuracy | 0.4450 | 0.8383 | **+0.3933** |
| **Test** | Macro Precision | 0.1483 | 0.8238 | **+0.6755** |
| **Test** | Macro Recall | 0.3333 | 0.8218 | **+0.4885** |
| **Test** | Macro F1 | 0.2053 | 0.8227 | **+0.6174** |

---

## Interpretation

1. **Failure of Majority Baseline:**
   - Because the majority baseline predicts `'low'` for every student, it achieves 44.50% accuracy solely due to class distribution.
   - Crucially, its recall for `medium` risk students is **0.00%** and for `high` risk students is **0.00%**. A faculty mentor using this heuristic would fail to detect **100% of students needing tutoring or urgent counseling**.
2. **ANN Substantial Improvement:**
   - On the held-out test split, the Step 3 ANN achieves **83.83% accuracy** (+0.3933 points) and **0.8227 macro F1** (+0.6174 points).
   - The neural network successfully detects multi-dimensional combinations of disengagement (e.g., student with high attendance but failing assessments, or low attendance with strong prior marks) that fixed single-rule heuristics cannot capture.
3. **No Metric Degradation:**
   - The ANN improves upon the baseline across every single measured metric on both validation and test sets without trade-offs.

---

## Limitations and Responsible Use

- **Educational Decision-Support Prototype:** The system's predictions are decision aids for faculty mentors and counselors. They must never automate student punishment, academic sanctions, or public ranking.
- **Model Disagreements:** On boundary cases (e.g., students near 50% or 70% composite boundaries), human mentor context (health, personal background, non-academic hardships) takes precedence over algorithmic outputs.
- **Data Scope:** Current evaluations are benchmarked on the 12,000-record cohort dataset; deployment in a live institution requires ongoing calibration with real course rosters.

---

## Reproducibility and Evidence

- **Repeatable Comparison Script:** `src/compare_baseline.py`
- **Executed Notebook:** `notebooks/03_baseline_comparison.ipynb`
- **Metrics Table:** `data/reports/step4_baseline_metrics.csv`
- **Difference Table:** `data/reports/step4_comparison.csv`
- **Paired Predictions:**
  - `data/reports/step4_validation_paired_predictions.csv`
  - `data/reports/step4_test_paired_predictions.csv`
- **Comparison Visualizer:** `results/step4_baseline_vs_ann.png`

### Reproduction Command
```bash
python src/compare_baseline.py
```

---

## Team Contributions

- **Deepak Gupta:** Repository Lead & System Architecture. Initialized Git branches, configured reproducible virtual environment, managed remote GitHub sync, and integrated `compare_baseline.py` validation assertions.
- **Himanshu Rai:** Data & Machine Learning Lead. Managed the 12,000-record dataset ingestion, verified 70/15/15 stratified partitioning, and maintained manifest checksums.
- **Anish Kumar Singh:** Baseline & Soft Computing Lead. Formulated baseline rules and tie-breaking logic, verified multi-class macro metric evaluations, and authored the baseline pseudocode.
- **Arvant Deshwal:** Testing & UI Lead. Designed automated data assertions, conducted row-by-row prediction alignment testing, and validated confusion matrix visualizations.
