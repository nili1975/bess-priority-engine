
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# פרמטרים קבועים
bess_capacity_kwh = 34650  # עודכן לפי בקשתך
grid_connection_limit_kw = 6000

# טעינת המודל המאומן
model = joblib.load("bess_priority_model2.pkl")

# פונקציה לחישוב פיצ'רים
def prepare_features(input_dict):
    soc = input_dict['soc']
    BESS_Power = input_dict.get('abs_POC_BESS_Power', 0)
    if BESS_Power == 0:
        BESS_Power = 1

    now = datetime.now()
    hour = now.hour
    month = now.month

    energy_needed_kwh = bess_capacity_kwh * (1 - soc / 100)
    required_quarters = np.ceil((energy_needed_kwh / BESS_Power) * 4)
    quarters_left = max(0, (16 - hour) * 4)

    input_dict_full = {
        'SOC': soc,
        'hour': hour,
        'month': month,
        'energy_needed_kwh': energy_needed_kwh,
        'required_quarters': required_quarters,
        'quarters_left': quarters_left,
        'abs_POC_BESS_Power': BESS_Power,
    }

    selected_features = list(model.feature_names_in_)
    return pd.DataFrame([{key: input_dict_full[key] for key in selected_features}])

# ממשק משתמש
st.title("⚡ החלטת טעינה ל־BESS (רק SOC ו־BESS Power)")

soc = st.slider("SOC [%]", 0, 100, 50)
bess_power = st.slider("הספק אפשרי להזנת BESS [kW]", 0, 6000, 3000)

if st.button("חשב החלטה"):
    input_dict = {
        'soc': soc,
        'abs_POC_BESS_Power': bess_power
    }

    input_df = prepare_features(input_dict)
    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.success("✅ יש להעדיף טעינה ל־BESS ברבע שעה הקרובה")
    else:
        st.info("ℹ️ אין צורך מיידי לטעינה ל־BESS")
