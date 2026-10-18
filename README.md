# Student Performance and Academic Intervention System (SC03)

> A role-based academic decision-support system that evaluates anonymous student academic indicators, estimates an academic risk band, suggests supportive educational interventions, and benchmarks simple rules against transparent neural classifiers.

---

## 1. Project Overview & Governance

- **Project ID:** SC03
- **Title:** Student Performance and Academic Intervention System
- **Faculty Domain:** Soft Computing Decision-Support System
- **One-Sentence Problem:** *Given anonymous academic indicators, estimate an academic risk band and suggest a supportive intervention.*

### Core Principles
1. **Decision Support, Not Automation:** Mentors and counselors make all final educational decisions; the software never automates disciplinary actions, ranking, or penalties.
2. **Privacy by Design:** Data is completely anonymized (`STU-001`, `STU-002`, ...); no student names, emails, or personal identifiers are collected or processed.
3. **Transparent Soft Computing:** Neural models are evaluated transparently against crisp baseline rules on identical held-out partitions.

---

## 2. Team Members & Roles

| Member Name | Role & Responsibility | GitHub Profile |
| :--- | :--- | :--- |
| **Deepak Gupta** | Team Lead / Repository & Backend Lead | [@deepakkguptaaa](https://github.com/deepakkguptaaa) |
| **Himanshu Rai** | Data & Machine Learning Lead | Team Member |
| **Anish Kumar Singh** | Baseline & Soft Computing Lead | Team Member |
| **Arvant Deshwal** | Testing & User Interface Lead | Team Member |

---

## 3. Data Dictionary

The system processes the following 7 core fields:

| Field Name | Simple Meaning | Type / Unit | Starter Rule / Allowed Range |
| :--- | :--- | :--- | :--- |
| `record_id` | Unique anonymous identifier | text | `STU-001`, `STU-002`, ... (unique) |
| `attendance_pct` | Classroom lecture and lab attendance | number (%) | 0.0 to 100.0 |
| `assessment_pct` | Continuous internal assessment marks | number (%) | 0.0 to 100.0 |
| `assignment_pct` | Practical assignment & homework marks | number (%) | 0.0 to 100.0 |
| `engagement_score` | Course participation & LMS activity | number (score) | 0.0 to 10.0 |
| `prior_performance_pct` | Prior semester / qualifying academic score | number (%) | 0.0 to 100.0 |
| `risk_label` | Target category for academic assistance | category | `low`, `medium`, `high` |

*Missing values are not permitted; incomplete rows are strictly rejected by the input validation suite.*

---

## 4. System Outputs & Interventions

The system outputs a risk classification and recommends a tailored, supportive action:
- **`low` Risk:** Student is performing consistently well $\rightarrow$ **Standard Academic Monitoring**.
- **`medium` Risk:** Warning indicators in one or more subjects $\rightarrow$ **Peer Mentoring & Structured Study Plan**.
- **`high` Risk:** Multiple indicators show academic distress $\rightarrow$ **One-on-One Faculty Mentor Consultation**.

---

## 5. Repository Structure (Step 1 State)

```text
SC03-Student-Performance-and-Academic-Intervention-System/
├── README.md                      # Project overview and Data Dictionary (this file)
├── requirements.txt               # Pinned Python package dependencies
├── .gitignore                     # Git ignore rules for virtualenvs, caches, and system files
├── data/
│   ├── README.md                  # Data specification, citations, and constraints
│   ├── sample_input.csv           # 20-row verified starter dataset
│   └── invalid_cases.csv          # Corrupted test case for validation failure checks
├── docs/
│   ├── STEP-1.md                  # Step 1 Project Contract
│   ├── baseline-pseudocode.md     # Linear baseline algorithm and threshold rules
│   └── product-v1-sketch.png      # Product V1 UI screen sketch
└── src/
    └── validate_data.py           # Automated input validation script
```

---

## 6. How to Run (Step 1 Verification)

### Prerequisites
Python 3.10+ installed.

### Setup and Validation
```bash
# 1. Clone repository
git clone https://github.com/deepakkguptaaa/SC03-Student-Performance-and-Academic-Intervention-System-Smart-Solution-Answer.git
cd SC03-Student-Performance-and-Academic-Intervention-System-Smart-Solution-Answer

# 2. Run data validation on starter dataset (Expect: STEP 1 DATA CHECK PASSED)
python src/validate_data.py data/sample_input.csv

# 3. Test validator failure detection on corrupted test case
python src/validate_data.py data/invalid_cases.csv
```

---

## 7. Next Steps
- **Step 2:** Ingest and generate 10,000+ benchmark dataset (`data/raw/`), build data pipeline (`src/prepare_data.py`), generate testing scenarios (`src/generate_test_scenarios.py`), and execute inspection notebook (`notebooks/01_data_inspection.ipynb`) on branch `step-2-data-pipeline`.
- **Step 3:** Train and evaluate transparent Soft Computing neural model (ADALINE / ANN) on branch `step-3-ann-model`.
- **Step 4:** Conduct fair baseline comparison and metrics analysis on branch `step-4-baseline`.
