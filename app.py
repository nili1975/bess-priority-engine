import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import pytz

# טען את המודל המאומן
model = joblib.load("bess_priority_model2.pkl")

def interactive_decision(soc, BESS_Power, hour, month):
    input_data = pd.DataFrame([{
        'soc': soc,
        'hour': hour,
        'month': month,
        'abs_POC_BESS_Power': BESS_Power
    }])

    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0][1] if hasattr(model, "predict_proba") else None

    decision = "🔋 טעינה נדרשת ל־BESS" if prediction == 1 else "✅ אין צורך בטעינה"

    st.write("📥 קלט שהוזן למודל:")
    st.dataframe(input_data)

    st.write("📤 פלט מהמודל:")
    st.success(f"החלטה: {decision}")
    if prediction_proba is not None:
        st.info(f"סבירות לטעינה נדרשת: {prediction_proba:.2%}")

# כותרת ראשית
st.title("⚡ מערכת קבלת החלטות לטעינה ל־BESS (מוד דינמי עם אפשרות הדגמה)")

# זיהוי השעה והחודש לפי זמן ישראל
israel_tz = pytz.timezone('Asia/Jerusalem')
now = datetime.now(israel_tz)
default_hour = now.hour
default_minute = now.minute
default_month = now.month

# אפשרות למצב הדגמה
demo_mode = st.checkbox("הפעל מצב הדגמה (שנה ידנית את השעה והחודש)", value=False)

# בחירת שעה וחודש (אוטומטי או ידני)
if demo_mode:
    hour = st.slider("בחר שעה (0–23)", min_value=0, max_value=23, value=default_hour)
    month = st.slider("בחר חודש (1–12)", min_value=1, max_value=12, value=default_month)
else:
    hour = default_hour
    month = default_month
    st.markdown(f"🕒 שעה נוכחית לפי המחשב: **{hour:02d}:{default_minute:02d}** &nbsp;&nbsp;&nbsp; 📅 חודש נוכחי: **{month}**")

# תנאי זמן
if hour < 9:
    st.warning("⌛ ההמלצה תינתן רק לאחר השעה 09:00")
elif hour > 16 or (hour == 16 and default_minute > 30):
    st.warning("📴 חלון ההמלצות הסתיים ליום זה (אחרי 16:30)")
else:
    soc = st.slider("SOC [%]", min_value=0, max_value=100, value=50)
    BESS_Power = st.slider("הספק טעינה ל־BESS [kW]", min_value=0, max_value=6000, value=3000)
    interactive_decision(soc, BESS_Power, hour, month)

# הצגה גם בתחתית
st.markdown("---")
st.markdown(f"🕒 שעה: **{hour:02d}**, חודש: **{month}** {'(מצב הדגמה)' if demo_mode else '(זיהוי אוטומטי)'}")
