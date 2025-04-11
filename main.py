import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from data_input import load_cash_flow_data
from analysis import forecast_cash_flows, dcf_valuation, sensitivity_analysis
from reporting import export_to_excel

st.title("Treasury & Investment Analysis")

# File upload
uploaded_file = st.file_uploader("Upload Cash Flow Data (CSV)", type='csv')
if uploaded_file:
    # Save uploaded file temporarily
    with open("temp_cash_flows.csv", "wb") as f:
        f.write(uploaded_file.read())
    cash_flow_data = load_cash_flow_data("temp_cash_flows.csv")
    st.write("Uploaded Data:", cash_flow_data)

    # Forecast parameters
    periods = st.slider("Forecast Periods (Months)", 1, 24, 12)
    growth_rate = st.slider("Growth Rate", 0.0, 0.1, 0.02, 0.01)
    forecast = forecast_cash_flows(cash_flow_data, periods, growth_rate)
    st.write("Cash Flow Forecast:", forecast)

    # Valuation
    discount_rate = st.slider("Discount Rate", 0.05, 0.15, 0.1, 0.01)
    valuation = dcf_valuation(forecast, discount_rate)
    st.write(f"DCF Valuation: ${valuation:,.2f}")

    # Sensitivity Analysis
    sensitivity = sensitivity_analysis(cash_flow_data, growth_rate, discount_rate)
    st.write("Sensitivity Analysis:", sensitivity)

    # Visualizations
    st.subheader("Visualizations")
    
    # Cash Flow Forecast Plot
    plt.figure(figsize=(10, 6))
    plt.plot(forecast['Date'], forecast['Net Cash Flow'], label='Net Cash Flow')
    plt.title('Cash Flow Forecast')
    plt.xlabel('Date')
    plt.ylabel('Cash Flow ($)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    plt.close()

    # Sensitivity Analysis Heatmap
    pivot = sensitivity.pivot(index='Growth Rate', columns='Discount Rate', values='Valuation')
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title('Sensitivity Analysis: Valuation ($)')
    st.pyplot(plt)
    plt.close()

    # Download Excel report
    export_to_excel(forecast, sensitivity, filename="treasury_report.xlsx")
    with open("treasury_report.xlsx", "rb") as f:
        st.download_button(
            label="Download Report",
            data=f,
            file_name="treasury_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.write("Please upload a cash_flows.csv file to begin.")
