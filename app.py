
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from pytz import timezone

st.set_page_config(page_title="טעינת BESS", page_icon="⚡")

st.title("⚡ מערכת קבלת החלטות לטעינה ל־BESS (כולל דמו וניתוח זמן)")

model = joblib.load("bess_priority_model2.pkl")
expected_features = list(model.feature_names_in_)

# --- בחירת מצב ---
mode = st.radio("בחר מצב", ["זיהוי אוטומטי", "מצב הדגמה ידני"])

# קלטים משותפים
soc = st.slider("SOC [%]", 0, 100, 50)
bess_power = st.slider("הספק טעינה ל־BESS [kW]", 0, 6000, 3000)

# שעה וחודש
if mode == "מצב הדגמה ידני":
    hour = st.slider("בחר שעה (0–23)", 0, 23, 13)
    month = st.slider("בחר חודש (1–12)", 1, 12, 6)
    now = datetime.now()
else:
    now = datetime.now(timezone('Asia/Jerusalem'))
    hour = now.hour
    month = now.month
    st.write(f"🕒 שעה נוכחית לפי שעון ישראל: {hour:02d}:{now.minute:02d}, חודש: {month}")

# קלט כולל
input_dict = {
    'SOC': soc,
    'abs_POC_BESS_Power': bess_power,
    'hour': hour,
    'month': month
}

def prepare_features(input_dict):
    soc = input_dict['SOC']
    hour = input_dict['hour']
    month = input_dict['month']
    BESS_Power = input_dict['abs_POC_BESS_Power']

    if BESS_Power == 0:
        BESS_Power = 1

    bess_capacity_kwh = 34650
    energy_needed_kwh = bess_capacity_kwh * (1 - soc / 100)
    required_quarters = np.ceil((energy_needed_kwh / BESS_Power) * 4)
    quarters_left = max(0, (16 - hour) * 4)

    data = {
        'SOC': soc,
        'hour': hour,
        'month': month,
        'required_quarters': required_quarters,
        'quarters_left': quarters_left,
        'energy_needed_kwh': energy_needed_kwh,
        'abs_POC_BESS_Power': BESS_Power
    }

    return pd.DataFrame([{key: data[key] for key in expected_features}])

features_df = prepare_features(input_dict)

# בדיקה
actual_features = list(features_df.columns)
if expected_features != actual_features:
    st.error("⚠️ הפיצ'רים לא תואמים את דרישות המודל.")
    st.write("מצופה:", expected_features)
    st.write("קיים בפועל:", actual_features)
    st.stop()

# הצגת המלצה או אזהרה
if mode == "זיהוי אוטומטי" and (hour < 9 or (hour == 16 and now.minute > 30) or hour > 16):
    st.warning("⏳ מחוץ לשעות הפעילות (09:00–16:30) – לא מוצגת המלצה.")
else:
    prediction = model.predict(features_df)[0]
    st.subheader("📊 החלטת המודל:")
    if prediction == 1:
        st.success("✅ החלטה: יש לטעון את הסוללה")
    else:
        st.info("ℹ️ החלטה: אין צורך בטעינה כעת")

with st.expander("📄 פיצ'רים שחושבו"):
    st.dataframe(features_df)
