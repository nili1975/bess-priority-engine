
import streamlit as st
from datetime import datetime
import joblib
import pandas as pd
import numpy as np

# טוען את המודל
model = joblib.load('bess_priority_model2.pkl')

# כותרת ראשית
st.title("⚡ החלטת טעינה ל־BESS על בסיס SOC ו־BESS Power")

# קלט מהמשתמש
soc = st.slider("SOC [%]", 0, 100, 50)
bess_power = st.slider("הספק אפשרי להזנת BESS [kW]\n(הספק טעינת הסוללות [kW])", 0, 6000, 3000)

# זיהוי זמן נוכחי
now = datetime.now()
hour = now.hour
month = now.month

# הודעה לפי השעה
if hour >= 16:
    st.warning("⛔ עברו השעות המומלצות לטעינה – המערכת לא ממליצה על טעינה לאחר 16:30")
elif hour < 9:
    st.info("⌛ מוקדם מדי – ההמלצה תתעדכן לאחר 09:00 בבוקר")

# קיבולת הסוללה
bess_capacity_kwh = 34650

# חישובים
energy_needed_kwh = bess_capacity_kwh * (1 - soc / 100)
required_quarters = np.ceil((energy_needed_kwh / bess_power) * 4)
quarters_left = max(0, (16 - hour) * 4)

# קלט למודל
input_dict = {
    'SOC': soc,
    'hour': hour,
    'month': month,
    'required_quarters': required_quarters,
    'quarters_left': quarters_left,
    'energy_needed_kwh': energy_needed_kwh,
    'abs_POC_BESS_Power': bess_power
}

# יצירת DataFrame עם הפיצ'רים שהמודל דורש
selected_features = list(model.feature_names_in_)
input_df = pd.DataFrame([{key: input_dict[key] for key in selected_features}])

# הפעלת המודל
prediction = model.predict(input_df)[0]

# תוצאה
if prediction == 1:
    st.success("✅ המלצה: לטעון את הסוללה כעת.")
else:
    st.info("ℹ️ אין המלצה לטעינה בשלב זה.")
