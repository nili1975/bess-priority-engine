
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# טעינת המודל
model = joblib.load("bess_priority_model2.pkl")

# קיבולת סוללה לצורך חישוב
bess_capacity_kwh = 24000

# פונקציה לחישוב הפיצ'רים הדרושים
def prepare_features(input_dict):
    soc = input_dict['soc']
    hour = datetime.now().hour
    month = datetime.now().month
    BESS_Power = input_dict.get('abs_POC_BESS_Power', 0)
    if BESS_Power == 0:
        BESS_Power = 1

    energy_needed_kwh = bess_capacity_kwh * (1 - soc / 100)
    required_quarters = np.ceil((energy_needed_kwh / BESS_Power) * 4)
    quarters_left = max(0, (16 - hour) * 4)

    input_dict_full = {
        'soc': soc,
        'hour': hour,
        'month': month,
        'required_quarters': required_quarters,
        'quarters_left': quarters_left,
        'abs_POC_BESS_Power': BESS_Power
    }

    selected_features = list(model.feature_names_in_)
    features = {key: input_dict_full[key] for key in selected_features}
    return pd.DataFrame([features])

# כותרת האפליקציה
st.title("⚡ החלטת טעינה ל־BESS רק על בסיס SOC ו־BESS Power")

# טופס קלט מהמשתמש
soc = st.slider("SOC [%]", min_value=0, max_value=100, value=50)
bess_power = st.slider("הספק אפשרי להזנת BESS [kW]", min_value=0, max_value=6000, value=3000)

# הצגת זמן
now = datetime.now()
st.write(f"⏰ שעה: {now.hour} | חודש: {now.month}")

# הרצת המודל והצגת תוצאה
input_dict = {
    'soc': soc,
    'abs_POC_BESS_Power': bess_power
}
input_df = prepare_features(input_dict)
prediction = model.predict(input_df)[0]

if prediction == 1:
    st.success("✅ החלטה: יש להטעין את ה־BESS")
else:
    st.info("ℹ️ החלטה: אין צורך להטעין את ה־BESS כרגע")
