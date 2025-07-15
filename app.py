import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import numpy as np

def prepare_features(input_dict):
    soc = input_dict['SOC']
    BESS_Power = input_dict.get('abs_POC_BESS_Power', 0)
    if BESS_Power == 0:
        BESS_Power = 1

    now = datetime.now()
    hour = now.hour
    month = now.month

    bess_capacity_kwh = 34650
    energy_needed_kwh = bess_capacity_kwh * (1 - soc / 100)
    required_quarters = np.ceil((energy_needed_kwh / BESS_Power) * 4)
    quarters_left = max(0, (16 - hour) * 4)
    bess_first = int(required_quarters > quarters_left)

    input_dict_full = {
        'SOC': soc,
        'hour': hour,
        'month': month,
        'required_quarters': required_quarters,
        'quarters_left': quarters_left,
        'abs_POC_BESS_Power': BESS_Power,
        'BESS First': bess_first
    }

    model = joblib.load('bess_priority_model2.pkl')
    model_features = list(model.feature_names_in_)
    selected_features = [key for key in model_features if key in input_dict_full]
    features = {key: input_dict_full[key] for key in selected_features}
    return pd.DataFrame([features])

st.title("🔋 החלטת טעינה ל־BESS על בסיס SOC ו־BESS Power בלבד")

soc = st.slider("SOC [%]", 0, 100, 50)
bess_power = st.slider("הספק אפשרי להזרמה BESS [kW]", 0, 6000, 3000)
st.write("🕐 שעה:", datetime.now().strftime("%H:%M"), "| 🗓️ חודש:", datetime.now().month)

input_dict = {
    'SOC': soc,
    'abs_POC_BESS_Power': bess_power
}

input_df = prepare_features(input_dict)

model = joblib.load('bess_priority_model2.pkl')
prediction = model.predict(input_df)[0]

if prediction == 1:
    st.success("✅ החלטה: יש לטעון את ה־BESS.")
else:
    st.warning("⛔ החלטה: אין לטעון את ה־BESS.")
