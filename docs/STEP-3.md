# Step 3 — Build and Train an Artificial Neural Network (ANN)

## 1. Goal
Train a feed-forward Artificial Neural Network (ANN) using backpropagation and Adam optimization to predict multi-class academic risk bands (`low`, `medium`, `high`) from continuous student learning indicators, enabling early supportive educational interventions.

---

## 2. Inputs and Output

### 5 Continuous Input Features:
1. `attendance_pct` (0 to 100%): Classroom lecture and laboratory attendance.
2. `assessment_pct` (0 to 100%): Continuous internal assessment examination score.
3. `assignment_pct` (0 to 100%): Homework and coursework submission quality.
4. `engagement_score` (0 to 10): LMS interaction and participation index.
5. `prior_performance_pct` (0 to 100%): Preceding semester GPA converted to percentage.

### Multi-Class Target:
`risk_label` with three discrete categories:
- `low`: Stable academic progress $\rightarrow$ Action: *Standard Academic Monitoring*
- `medium`: Warning signs in exams/engagement $\rightarrow$ Action: *Peer Mentoring or Structured Study Plan*
- `high`: Critical deficits across multiple areas $\rightarrow$ Action: *Direct Faculty Mentor Intervention*

---

## 3. ANN Architecture & Configuration

- **Preprocessing:** `StandardScaler` fitted strictly on training data ($z = \frac{x - \mu}{\sigma}$).
- **Network Topology:** $5 \text{ inputs} \rightarrow 16 \text{ hidden neurons (ReLU)} \rightarrow 8 \text{ hidden neurons (ReLU)} \rightarrow 3 \text{ output neurons (Softmax/Log-Loss)}$.
- **Optimizer:** Adam ($\beta_1=0.9, \beta_2=0.999$, initial learning rate $\eta = 0.001$).
- **Regularization & Early Stopping:** L2 penalty $\alpha = 0.0001$, internal validation fraction $15\%$, $n_{\text{iter\_no\_change}} = 25$.
- **Random Seed:** 42 for complete experimental reproducibility.

---

## 4. Training Convergence & Results

The network reached convergence in **83 iterations** with a final training loss of **0.35431**.

### Performance Metrics Table

| Split | Rows | Accuracy | Macro Precision | Macro Recall | Macro F1 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **Validation** | 1,800 | 0.8378 | 0.8241 | 0.8206 | 0.8223 |
| **Test (Held-out)** | 1,800 | 0.8383 | 0.8238 | 0.8218 | 0.8227 |

*Note: Precision, recall, and F1 use macro averaging to treat each risk category with equal weight.*

---

## 5. Evidence Files Produced

1. **Executed Notebook:** `notebooks/02_ann_model.ipynb` with fresh-kernel visible outputs and plots.
2. **Repeatable Training Script:** `src/train_ann.py`.
3. **Serialized Pipeline & Model:** `models/ann_student_performance.pkl`.
4. **Model Metadata JSON:** `models/ann_model_metadata.json` (architecture, seed, parameters, metrics).
5. **Loss Curve Plot:** `results/step3_ann_loss_curve.png`.
6. **Confusion Matrices:** `results/step3_ann_validation_confusion_matrix.png` and `results/step3_ann_test_confusion_matrix.png`.
7. **Metrics CSV:** `data/reports/step3_ann_metrics.csv`.
8. **Row-Aligned Predictions:** `data/reports/step3_validation_predictions.csv` and `step3_test_predictions.csv`.

---

## 6. Limitations & Responsible Use

1. **Decision Support Only:** This model provides recommendations to assist human faculty mentors. It must never automate student punishment, public ranking, or administrative penalties.
2. **Benchmark Data:** The current dataset models educational patterns derived from synthetic and simulated cohort benchmarks. Predictions do not substitute for in-person faculty discussions.
3. **No Test Leakage:** The held-out test split was evaluated once with frozen parameters; hyperparameters were selected using validation data only.
