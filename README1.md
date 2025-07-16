
# ⚡ BESS Priority Engine | מנוע קבלת החלטות לטעינה

A bilingual (English + Hebrew) interactive Streamlit app for deciding whether to charge a BESS (Battery Energy Storage System), based on SOC, power availability, time, and month.

---

## 🧠 What does the app do?

- Accepts SOC, available BESS charging power, hour, and month
- Calculates required energy, required charging quarters, and compares to available time
- Predicts whether to charge the BESS using a trained ML model
- Includes two modes: real-time automatic mode and manual demo mode
- Validates feature input to match model expectations
- Detects off-hour use (outside 09:00–16:30) and warns the user

---

## 🔬 Project Background & Methodology

This project started by extracting operational data from a SCADA system. The raw data included 16 features related to site performance, energy flows, battery SOC, and availability.

Steps performed:

1. **Data Cleaning & Preparation**
   - Removed invalid rows and handled missing values
   - Filtered time intervals to include only 09:00–16:30 (operational hours)
   - Interpolated and corrected noisy measurements

2. **Feature Engineering**
   - Created derived features such as:
     - `energy_needed_kwh`
     - `required_quarters` to fully charge the BESS
     - `quarters_left` until end of day
     - Priority indicator: whether enough time remains

3. **Feature Selection**
   - Used a Random Forest model to rank feature importance
   - Selected only the most influential features to avoid overfitting

4. **Model Training**
   - Trained a classification model to predict whether charging should occur
   - Tuned hyperparameters and validated on a held-out test set
   - Ensured model generalization and avoided overfitting

5. **Deployment**
   - Built a Streamlit app to serve real-time decisions
   - App includes manual override for demo/testing, feature validation, and fallback messaging outside operating hours

The result: a lightweight, reliable decision support tool based on real operational data.

---


---

## 🤖 Model Selection and Justification

The main model used throughout the project was a **Random Forest Classifier**, due to its robustness, interpretability, and strong performance on tabular operational data.

### Why Random Forest?

- Handles nonlinear relationships well without requiring feature scaling
- Naturally resistant to overfitting due to averaging over many trees
- Supports feature importance ranking, which was critical for:
  - **Feature selection** – identifying which SCADA-derived parameters had the most influence on the charging decision
  - **Interpretability** – understanding which conditions most impact system recommendations

### Workflow:

1. **Initial Feature Selection**  
   A full set of 16 features was extracted from SCADA data.  
   Using a Random Forest model, feature importance was computed to identify the top contributors.

2. **Model Training**  
   A new Random Forest Classifier was trained on the selected subset of features.  
   Hyperparameters were tuned to balance accuracy and generalization, and the model was validated to ensure no overfitting.

The final model was then deployed inside the Streamlit decision support tool.


## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run bess_decision_app_clean.py
```

Make sure the file `bess_priority_model2.pkl` (trained model) is in the same folder.

---

## 🕒 Operating hours

- Recommendations are provided only between **09:00–16:30**
- Outside this window, a warning will be displayed instead of a decision

---

## 📂 Files

| File | Description |
|------|-------------|
| `bess_decision_app_clean.py` | Streamlit app |
| `bess_priority_model2.pkl` | Trained model (add manually) |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

---

## 🌐 מצב בעברית (Hebrew Summary)

מערכת אינטראקטיבית לקבלת החלטות חכמה בנוגע לטעינת מערכת אגירת אנרגיה (BESS):

- מאפשרת קלט של מצב טעינה (SOC), הספק טעינה, שעה וחודש
- מחשבת אנרגיה חסרה ומספר רבעי שעה דרושים
- מתבססת על מודל למידת מכונה
- כוללת מצב הדגמה ידני + מצב אוטומטי בזמן אמת
- מספקת התראה מחוץ לשעות הפעילות (09:00–16:30)
- מציגה את כל הפיצ'רים שנשלחו למודל

---

## 👩‍💻 Created by:

**Nili Golan**  
Senior Data Analyst – Solar Performance & BESS Optimization  
📧 [LinkedIn](https://www.linkedin.com) (replace with your link)
