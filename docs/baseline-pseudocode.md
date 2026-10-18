# Baseline Logic & Pseudocode — SC03 Academic Intervention

## Purpose
The baseline serves as a simple, transparent, non-Soft-Computing benchmark to compare against later neural networks (ADALINE, Perceptron, Backpropagation).

## Inputs
- `attendance_pct` (0 to 100)
- `assessment_pct` (0 to 100)
- `assignment_pct` (0 to 100)
- `engagement_score` (0 to 10)
- `prior_performance_pct` (0 to 100)

## Calculation Rules
1. Normalize engagement to a percentage scale:
   $$\text{engagement\_pct} = \text{engagement\_score} \times 10.0$$
2. Compute composite academic score using illustrative classroom weights:
   $$\text{score} = 0.30 \times \text{attendance\_pct} + 0.30 \times \text{assessment\_pct} + 0.20 \times \text{assignment\_pct} + 0.10 \times \text{engagement\_pct} + 0.10 \times \text{prior\_performance\_pct}$$
3. Assign risk category and supportive intervention:
   - If $\text{score} < 50.0$:
     - Category: `high`
     - Intervention: **Faculty follow-up & counseling**
   - Else if $50.0 \le \text{score} < 70.0$:
     - Category: `medium`
     - Intervention: **Peer mentoring or structured study plan**
   - Else ($\text{score} \ge 70.0$):
     - Category: `low`
     - Intervention: **Standard academic monitoring**

## Pseudocode

```text
FUNCTION evaluate_baseline(student_record):
    IF any input in student_record is MISSING OR NULL THEN
        RETURN ERROR("Missing required indicators")
    ENDIF

    IF attendance < 0 OR attendance > 100 THEN RETURN ERROR("Invalid attendance")
    IF assessment < 0 OR assessment > 100 THEN RETURN ERROR("Invalid assessment")
    IF assignment < 0 OR assignment > 100 THEN RETURN ERROR("Invalid assignment")
    IF engagement < 0 OR engagement > 10  THEN RETURN ERROR("Invalid engagement")
    IF prior < 0 OR prior > 100           THEN RETURN ERROR("Invalid prior performance")

    eng_pct = student_record.engagement_score * 10.0
    
    composite_score = (0.30 * student_record.attendance_pct) + \
                      (0.30 * student_record.assessment_pct) + \
                      (0.20 * student_record.assignment_pct) + \
                      (0.10 * eng_pct) + \
                      (0.10 * student_record.prior_performance_pct)

    IF composite_score < 50.0 THEN
        risk = "high"
        action = "Faculty follow-up"
    ELSE IF composite_score < 70.0 THEN
        risk = "medium"
        action = "Mentoring or study plan"
    ELSE
        risk = "low"
        action = "Monitor"
    ENDIF

    RETURN {
        "score": composite_score,
        "risk_label": risk,
        "recommended_intervention": action
    }
END FUNCTION
```

## Important Limitation Notice
This linear weighted rule is purely a comparative baseline. It assumes linear compensability between attendance and exam marks and cannot model complex interaction effects or non-linear academic disengagement patterns.
