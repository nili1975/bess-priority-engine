import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# טען את המודל
model = joblib.load("bess_priority_model2.pkl")

# קבועים
bess_capacity_kwh = 0.99 * 35000
target_soc = 0.99

def prepare_features(soc, BESS_Power):
    now = datetime.now()
    hour = now.hour + now.minute / 60  # שעה מדויקת
    month = now.month

    energy_needed_kwh = bess_capacity_kwh * (target_soc - soc / 100)
    BESS_Power = max(BESS_Power, 1)  # מניעת חלוקה באפס
    required_quarters = np.ceil((energy_needed_kwh / BESS_Power) * 4)
    quarters_left = max(0, (16.5 - hour) * 4)

    return pd.DataFrame([{
        'SOC': soc,
        'hour': hour,
        'month': month,
        'energy_needed_kwh': energy_needed_kwh,
        'required_quarters': required_quarters,
        'quarters_left': quarters_left,
        'abs_POC_BESS_Power': BESS_Power
    }])

# כותרת
st.title("⚡ החלטת טעינה ל־BESS (רק SOC ו־BESS Power)")

# קלט מהמשתמש
soc = st.slider("SOC [%]", 0, 100, 50)
BESS_Power = st.slider("הספק אפשרי להזנת BESS [kW]", 0, 6000, 3000)

# יצירת הקלט והצגת תאריך/שעה
st.write(f"🕒 שעה: {datetime.now().strftime('%H:%M')} | חודש: {datetime.now().month}")

input_df = prepare_features(soc, BESS_Power)

# תחזית
prediction = model.predict(input_df)[0]
probability = model.predict_proba(input_df)[0][1]

# תצוגה
st.write("📥 קלט שהוזן למודל:")
st.dataframe(input_df)

st.success("✅ טעינה נדרשת ל־BESS" if prediction == 1 else "🟡 אין צורך בטעינה")
st.info(f"סבירות לטעינה נדרשת: {probability:.2%}")
