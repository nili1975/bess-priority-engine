
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

st.set_page_config(page_title="טעינת BESS", page_icon="⚡")

st.title("⚡ החלטת טעינה ל־BESS על בסיס SOC ו־BESS Power")

# קלט מהמשתמש
soc = st.slider("SOC [%]", 0, 100, 50)
bess_power = st.slider("הספק אפשרי להזנת BESS [kW]", 0, 6000, 3000)

# טעינת המודל
model = joblib.load("bess_priority_model2.pkl")

def prepare_features(input_dict):
    soc = input_dict['SOC']
    BESS_Power = input_dict['abs_POC_BESS_Power']

    if BESS_Power == 0:
        BESS_Power = 1

    now = datetime.now()
    hour = now.hour
    month = now.month

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

    features_order = ['SOC', 'hour', 'month', 'required_quarters', 'quarters_left', 'energy_needed_kwh', 'abs_POC_BESS_Power']
    return pd.DataFrame([{key: data[key] for key in features_order}])

# יצירת DataFrame והצגת החלטה
input_dict = {'SOC': soc, 'abs_POC_BESS_Power': bess_power}
input_df = prepare_features(input_dict)
prediction = model.predict(input_df)[0]

st.subheader("📊 החלטת המודל:")
if prediction == 1:
    st.success("החלטה: יש לטעון את הסוללה ✅")
else:
    st.info("החלטה: אין צורך בטעינה כעת ℹ️")
