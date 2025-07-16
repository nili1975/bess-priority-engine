import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
import pytz

# נתוני אתר קבועים
site_capacity_kwp = 15200
grid_connection_limit_kw = 6000
bess_capacity_kwh = 0.99 * 30000  # SOC יעד
bess_charge_limit_kw = 6000

# פונקציית יצירת פיצ'רים
def prepare_features(input_dict):
    soc = input_dict['soc']
    hour = input_dict['hour']
    month = input_dict['month']
    BESS_Power = input_dict.get('abs_POC_BESS_Power', 0)
    if BESS_Power == 0:
        BESS_Power = 1

    energy_needed_kwh = bess_capacity_kwh * (1 - soc / 100)
    required_quarters = np.ceil((energy_needed_kwh / BESS_Power) * 4)
    quarters_left = max(0, (16 - hour) * 4)
    bess_first = int(required_quarters > quarters_left)

    input_dict_full = {
        'soc': soc,
        'hour': hour,
        'month': month,
        'energy_needed_kwh': energy_needed_kwh,
        'required_quarters': required_quarters,
        'quarters_left': quarters_left,
        'abs_POC_BESS_Power': BESS_Power,
        'BESS First': bess_first
    }

    selected_features = ['soc', 'hour', 'month', 'energy_needed_kwh',
                         'required_quarters', 'quarters_left',
                         'abs_POC_BESS_Power', 'BESS First']
    return pd.DataFrame([{key: input_dict_full[key] for key in selected_features}])

# טען את המודל המאומן
model = joblib.load("bess_priority_model2.pkl")

def interactive_decision(soc, BESS_Power, hour, month):
    input_dict = {
        'soc': soc,
        'hour': hour,
        'month': month,
        'abs_POC_BESS_Power': BESS_Power
    }

    features_df = prepare_features(input_dict)
    prediction = model.predict(features_df)[0]
    prediction_proba = model.predict_proba(features_df)[0][1] if hasattr(model, "predict_proba") else None

    decision = "🔋 טעינה נדרשת ל־BESS" if prediction == 1 else "✅ אין צורך בטעינה"

    st.write("📥 קלט לאחר חישוב פיצ'רים:")
    st.dataframe(features_df)

    st.write("📤 פלט מהמודל:")
    st.success(f"החלטה: {decision}")
    if prediction_proba is not None:
        st.info(f"סבירות לטעינה נדרשת: {prediction_proba:.2%}")

# כותרת ראשית
st.title("⚡ מערכת קבלת החלטות לטעינה ל־BESS (כולל יצירת פיצ'רים)")

# זיהוי השעה והחודש לפי זמן ישראל
israel_tz = pytz.timezone('Asia/Jerusalem')
now = datetime.now(israel_tz)
default_hour = now.hour
default_minute = now.minute
default_month = now.month

# מצב דמו לעומת זמן אמיתי
demo_mode = st.radio("בחר מצב:", options=["זיהוי אוטומטי", "מצב הדגמה ידני"])

if demo_mode == "מצב הדגמה ידני":
    hour = st.slider("בחר שעה (0–23)", min_value=0, max_value=23, value=default_hour)
    month = st.slider("בחר חודש (1–12)", min_value=1, max_value=12, value=default_month)
else:
    hour = default_hour
    month = default_month
    st.markdown(f"🕒 שעה נוכחית לפי המחשב: **{hour:02d}:{default_minute:02d}**  &nbsp;&nbsp;&nbsp; 📅 חודש נוכחי: **{month}**")

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
mode_display = "מצב הדגמה" if demo_mode == "מצב הדגמה ידני" else "זיהוי אוטומטי"
st.markdown(f"🕒 שעה: **{hour:02d}**, חודש: **{month}** ({mode_display})")
