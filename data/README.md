# SC03 Academic Intervention — Data Documentation & Pipeline Plan

## Project Purpose
This project designs and evaluates an academic decision-support system that converts continuous student learning indicators into an academic risk category (`low`, `medium`, `high`) and recommends tailored educational interventions.

---

## 1. Primary Benchmark Dataset Pipeline (10,000+ Records)

- **Dataset Code & Name:** SC03 Student Performance Benchmark
- **Original Source & Citation:** Modeled from higher-education learning analytics patterns (Kaggle / Open University Learning Analytics Dataset OULAD standard features)
- **Licence:** MIT License
- **Storage Location (Raw):** `data/raw/student_performance_raw.csv`
- **Cleaned Dataset:** `data/processed/student_performance_clean.csv`
- **Total Raw Records:** 12,005 (contains 60 deliberate test missing values and 5 duplicates to verify pipeline repair)
- **Total Cleaned Records:** 12,000 unique records

### Target Definition (`risk_label`)
- `low`: Student demonstrates strong academic standing and progress $\rightarrow$ Action: *Standard Academic Monitoring*
- `medium`: Student demonstrates borderline indicators or partial struggle $\rightarrow$ Action: *Peer Mentoring or Structured Study Plan*
- `high`: Student exhibits multiple compounding learning deficits $\rightarrow$ Action: *Direct Faculty Mentor Intervention*

---

## 2. Non-Circular Ground Truth Model
To avoid circular evaluation (where a model simply learns the baseline's linear formula), ground truth is generated via a latent factor model:
1. **Latent Factors:**
   - Academic Aptitude $A \sim \mathcal{N}(0, 1)$
   - Work Ethic & Diligence $W \sim \mathcal{N}(0, 1)$
2. **Non-Linear Domain Penalties:**
   - *Cramming Illusion Penalty:* High LMS activity with low assessment score ($-14$ pts).
   - *Disengagement Spiral:* Attendance $< 50\%$ causes severe unrecorded quiz loss ($-16$ pts).
   - *Prior Strength Breakdown:* High prior GPA failing to prevent collapse when attendance drops below $55\%$ ($-12$ pts).
   - *Dual Coursework Deficit:* Severe failure in both exams and assignments ($-15$ pts).
   - *Life Disruption Noise:* External non-academic shock $\eta \sim \mathcal{N}(0, 6.0)$.

---

## 3. Data Dictionary

| Field | Description | Type / Unit | Valid Domain Range |
| :--- | :--- | :--- | :--- |
| `record_id` | Anonymous row identifier | Text | `STU-00001`, `STU-00002`, ... |
| `attendance_pct` | Classroom attendance percentage | Float (%) | $0.0 \le \text{attendance} \le 100.0$ |
| `assessment_pct` | Midterm / internal exam marks | Float (%) | $0.0 \le \text{assessment} \le 100.0$ |
| `assignment_pct` | Assignment and coursework score | Float (%) | $0.0 \le \text{assignment} \le 100.0$ |
| `engagement_score` | Course LMS participation & engagement | Float (score) | $0.0 \le \text{engagement} \le 10.0$ |
| `prior_performance_pct` | Cumulative prior GPA / score | Float (%) | $0.0 \le \text{prior} \le 100.0$ |
| `risk_label` | Target category for academic assistance | Categorical | `low`, `medium`, `high` |

---

## 4. Stratified Data Partitions

The dataset is partitioned with a fixed random seed `42` using stratified sampling:

| Split File | Purpose | Rows | Proportion |
| :--- | :--- | ---: | ---: |
| `data/processed/train.csv` | Model training | 8,400 | 70% |
| `data/processed/validation.csv` | Hyperparameter selection & validation | 1,800 | 15% |
| `data/processed/test.csv` | Unseen final evaluation | 1,800 | 15% |

---

## 5. Generated Testing Scenarios (Separate Benchmark)
- **File:** `data/generated/generated_student_performance_test_scenarios.csv`
- **Count:** 1,200 testing scenarios (10% ratio)
- **Purpose:** Stress testing, edge cases, and product demonstration.
- **Rule of Academic Honesty:** These generated scenarios are **never** mixed into `train.csv`, `validation.csv`, or `test.csv`.
