import streamlit as st
import pandas as pd
import joblib

# טען את המודל המאומן
model = joblib.load("bess_priority_model1.pkl")

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
    st.write("📥 קלט למודל:")
    st.dataframe(input_data)
    st.write("📤 תחזית המודל:")
    st.success(f"החלטה: {decision}")
    if prediction_proba is not None:
        st.info(f"סבירות לטעינה נדרשת: {prediction_proba:.2%}")

st.title("⚡ מערכת קבלת החלטות לטעינה ל־BESS (לפי מודל חכם)")
soc = st.slider("SOC [%]", min_value=0, max_value=100, value=50)
BESS_Power = st.slider("הספק טעינה ל־BESS [kW]", min_value=0, max_value=6000, value=3000)
hour = st.slider("שעה", min_value=0, max_value=23, value=13)
month = st.slider("חודש", min_value=1, max_value=12, value=7)
interactive_decision(soc, BESS_Power, hour, month)
