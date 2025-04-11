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
    try:
        with open("temp_cash_flows.csv", "wb") as f:
            f.write(uploaded_file.read())
        
        # Load raw data to inspect columns
        raw_df = pd.read_csv("temp_cash_flows.csv")
        st.write("Detected Columns:", list(raw_df.columns))
        
        # Let user map columns
        st.subheader("Map Your CSV Columns")
        date_col = st.selectbox("Select Date Column", raw_df.columns)
        inflow_col = st.selectbox("Select Inflow Column", raw_df.columns)
        outflow_col = st.selectbox("Select Outflow Column", raw_df.columns)
        
        # Rename columns to standard names
        cash_flow_data = raw_df[[date_col, inflow_col, outflow_col]].copy()
        cash_flow_data.columns = ['Date', 'Inflow', 'Outflow']
        cash_flow_data['Date'] = pd.to_datetime(cash_flow_data['Date'])
        
        st.write("Standardized Data Columns:", list(cash_flow_data.columns))
        st.write("Standardized Data:", cash_flow_data.head())
    except Exception as e:
        st.error(f"Error processing CSV: {e}")
        st.stop()

    # Forecast parameters
    periods = st.slider("Forecast Periods (Months)", 1, 24, 12)
    growth_rate = st.slider("Growth Rate", 0.0, 0.1, 0.02, 0.01)
    
    # Debug: Verify columns before forecasting
    st.write("Columns before forecasting:", list(cash_flow_data.columns))
    try:
        forecast = forecast_cash_flows(cash_flow_data, periods, growth_rate)
        st.write("Cash Flow Forecast:", forecast)
    except Exception as e:
        st.error(f"Error in forecasting: {e}")
        st.stop()

    # Valuation
    discount_rate = st.slider("Discount Rate", 0.05, 0.15, 0.1, 0.01)
    valuation = dcf_valuation(forecast, discount_rate)
    st.write(f"DCF Valuation: ${valuation:,.2f}")

    # Sensitivity Analysis
    sensitivity = sensitivity_analysis(cash_flow_data, growth_rate, discount_rate)
    st.write("Sensitivity Analysis:", sensitivity)

    # Visualizations
    st.subheader("Visualizations")
    
    plt.figure(figsize=(10, 6))
    plt.plot(forecast['Date'], forecast['Net Cash Flow'], label='Net Cash Flow')
    plt.title('Cash Flow Forecast')
    plt.xlabel('Date')
    plt.ylabel('Cash Flow ($)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    plt.close()

    pivot = sensitivity.pivot(index='Growth Rate', columns='Discount Rate', values='Valuation')
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title('Sensitivity Analysis: Valuation ($)')
    st.pyplot(plt)
    plt.close()

    # Download Excel report
    try:
        export_to_excel(forecast, sensitivity, filename="treasury_report.xlsx")
        with open("treasury_report.xlsx", "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="treasury_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Error generating report: {e}")
else:
    st.write("Please upload a cash_flows.csv file to begin.")
