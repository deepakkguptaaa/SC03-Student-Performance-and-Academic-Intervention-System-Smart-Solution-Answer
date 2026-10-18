# Data Documentation — SC03 Academic Intervention

## Overview
This folder contains datasets and data documentation for **SC03: Student Performance and Academic Intervention System**.

## Data Dictionary (Starter Set)

| Field Name | Meaning | Type / Unit | Constraints & Validation Rule |
| :--- | :--- | :--- | :--- |
| `record_id` | Anonymous student identifier | Text | Unique format `STU-001`, `STU-002`, ... |
| `attendance_pct` | Lecture/lab attendance percentage | Float (%) | $0.0 \le \text{attendance\_pct} \le 100.0$ |
| `assessment_pct` | Continuous assessment / internal exam marks | Float (%) | $0.0 \le \text{assessment\_pct} \le 100.0$ |
| `assignment_pct` | Assignment submission score | Float (%) | $0.0 \le \text{assignment\_pct} \le 100.0$ |
| `engagement_score` | Course LMS participation & engagement | Float (score) | $0.0 \le \text{engagement\_score} \le 10.0$ |
| `prior_performance_pct` | Prior semester / qualifying GPA converted to % | Float (%) | $0.0 \le \text{prior\_performance\_pct} \le 100.0$ |
| `risk_label` | Target risk category for academic support | Categorical | `low`, `medium`, `high` |

## Target Classes and Supportive Interventions
The objective of this decision-support system is **early academic assistance**, not punitive action:
- **`low`**: Student is performing solidly. Recommended action: *Routine monitoring*.
- **`medium`**: Student demonstrates warning signs in one or more areas. Recommended action: *Peer mentoring or customized study plan*.
- **`high`**: Student is in urgent need of academic assistance. Recommended action: *Direct faculty mentor follow-up & intervention session*.

## Missing Values Policy
In Step 1, data integrity is strictly enforced. Any row containing missing, null, or out-of-range values is rejected by `src/validate_data.py`.

## Files
- `sample_input.csv`: 20 valid starter records covering typical student academic profiles.
- `invalid_cases.csv`: Deliberately corrupted test cases used to test validator failure modes.
