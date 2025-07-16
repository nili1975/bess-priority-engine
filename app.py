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
st.title("⚡ מערכת קבלת החלטות לטעינה ל־BESS (לפי מודל חכם)")

# זיהוי השעה והחודש לפי זמן ישראל
israel_tz = pytz.timezone('Asia/Jerusalem')
now = datetime.now(israel_tz)
hour = now.hour
minute = now.minute
month = now.month

# הצגת שעה וחודש (למעלה)
st.markdown(f"🕒 שעה נוכחית: **{hour:02d}:{minute:02d}**  &nbsp;&nbsp;&nbsp; 📅 חודש נוכחי: **{month}**")

# תנאי זמן: חסימת המלצה מחוץ לשעות 09:00–16:30
if hour < 9:
    st.warning("⌛ ההמלצה תינתן רק לאחר השעה 09:00")
elif hour > 16 or (hour == 16 and minute > 30):
    st.warning("📴 חלון ההמלצות הסתיים ליום זה (אחרי 16:30)")
else:
    # קלטים מהמשתמש
    soc = st.slider("SOC [%]", min_value=0, max_value=100, value=50)
    BESS_Power = st.slider("הספק טעינה ל־BESS [kW]", min_value=0, max_value=6000, value=3000)
    interactive_decision(soc, BESS_Power, hour, month)

# הצגת שעה וחודש (למטה)
st.markdown("---")
st.markdown(f"🕒 שעה מעודכנת כעת: **{hour:02d}:{minute:02d}**, חודש: **{month}** לפי שעון ישראל.")
