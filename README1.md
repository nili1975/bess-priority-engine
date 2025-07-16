
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
