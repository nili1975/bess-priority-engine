# 🔋 BESS Priority Engine

A Streamlit-based machine learning app for deciding whether to charge a BESS (Battery Energy Storage System), based on SOC, time, and power availability.

## Features
- Input: SOC, BESS Power, Hour, and Month
- ML model predicts whether charging is recommended
- Displays decision and probability

## Getting Started

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the app:
```bash
streamlit run app.py
```

## Files
- `app.py` — Streamlit app
- `bess_priority_model1.pkl` — Your trained model (add it manually)
- `requirements.txt` — Required Python packages
