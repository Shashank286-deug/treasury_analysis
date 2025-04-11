import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import logging
from data_input import load_cash_flow_data
from analysis import forecast_cash_flows, dcf_valuation, sensitivity_analysis
from reporting import export_to_excel

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.title("Treasury & Investment Analysis")

# File upload
uploaded_file = st.file_uploader("Upload Cash Flow Data (CSV)", type='csv')
if uploaded_file:
    # Save uploaded file temporarily
    try:
        logger.debug("Saving uploaded CSV to temp_cash_flows.csv")
        with open("temp_cash_flows.csv", "wb") as f:
            f.write(uploaded_file.read())
        
        # Load raw data to inspect columns
        logger.debug("Loading raw CSV")
        raw_df = pd.read_csv("temp_cash_flows.csv")
        st.write("Detected Columns:", list(raw_df.columns))
        
        # Let user map columns
        st.subheader("Map Your CSV Columns")
        date_col = st.selectbox("Select Date Column", raw_df.columns)
        inflow_col = st.selectbox("Select Inflow Column", raw_df.columns)
        outflow_col = st.selectbox("Select Outflow Column", raw_df.columns)
        
        # Create standardized DataFrame
        try:
            logger.debug(f"Mapping columns: {date_col} -> Date, {inflow_col} -> Inflow, {outflow_col} -> Outflow")
            cash_flow_data = raw_df[[date_col, inflow_col, outflow_col]].copy()
            cash_flow_data.columns = ['Date', 'Inflow', 'Outflow']
            
            # Convert Date to datetime
            cash_flow_data['Date'] = pd.to_datetime(cash_flow_data['Date'], errors='coerce')
            if cash_flow_data['Date'].isnull().any():
                raise ValueError("Some dates could not be parsed. Please ensure the date column is in a valid format (e.g., YYYY-MM-DD).")
            
            # Ensure Inflow and Outflow are numeric
            cash_flow_data['Inflow'] = pd.to_numeric(cash_flow_data['Inflow'], errors='coerce')
            cash_flow_data['Outflow'] = pd.to_numeric(cash_flow_data['Outflow'], errors='coerce')
            if cash_flow_data['Inflow'].isnull().any() or cash_flow_data['Outflow'].isnull().any():
                raise ValueError("Inflow or Outflow contains non-numeric values. Please ensure these columns contain numbers.")
            
            # Ensure at least one row
            if len(cash_flow_data) == 0:
                raise ValueError("CSV is empty. Please upload a valid CSV with data.")
            
            st.write("Standardized Data:", cash_flow_data.head())
            logger.debug(f"Standardized Data columns: {list(cash_flow_data.columns)}")
        except Exception as e:
            logger.error(f"Error standardizing data: {e}")
            st.error(f"Error standardizing data: {e}")
            st.stop()
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        st.error(f"Error processing CSV: {e}")
        st.stop()

    # Forecast parameters
    periods = st.slider("Forecast Periods (Months)", 1, 24, 12)
    growth_rate = st.slider("Growth Rate", 0.0, 0.1, 0.02, 0.01)
    
    try:
        logger.debug("Running forecast_cash_flows")
        forecast = forecast_cash_flows(cash_flow_data, periods, growth_rate)
        st.write("Cash Flow Forecast:", forecast)
    except Exception as e:
        logger.error(f"Error in forecasting: {e}")
        st.error(f"Error in forecasting: {e}")
        st.stop()

    # Valuation
    discount_rate = st.slider("Discount Rate", 0.05, 0.15, 0.1, 0.01)
    try:
        logger.debug("Running dcf_valuation")
        valuation = dcf_valuation(forecast, discount_rate)
        st.write(f"DCF Valuation: ${valuation:,.2f}")
    except Exception as e:
        logger.error(f"Error in valuation: {e}")
        st.error(f"Error in valuation: {e}")
        st.stop()

    # Sensitivity Analysis
    try:
        logger.debug("Running sensitivity_analysis")
        sensitivity = sensitivity_analysis(cash_flow_data, growth_rate, discount_rate)
        st.write("Sensitivity Analysis:", sensitivity)
    except Exception as e:
        logger.error(f"Error in sensitivity analysis: {e}")
        st.error(f"Error in sensitivity analysis: {e}")
        st.stop()

    # Visualizations
    st.subheader("Visualizations")
    
    try:
        logger.debug("Plotting forecast chart")
        plt.figure(figsize=(10, 6))
        plt.plot(forecast['Date'], forecast['Net Cash Flow'], label='Net Cash Flow')
        plt.title('Cash Flow Forecast')
        plt.xlabel('Date')
        plt.ylabel('Cash Flow ($)')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
        plt.close()
    except Exception as e:
        logger.error(f"Error plotting forecast: {e}")
        st.error(f"Error plotting forecast: {e}")

    try:
        logger.debug("Plotting sensitivity heatmap")
        pivot = sensitivity.pivot(index='Growth Rate', columns='Discount Rate', values='Valuation')
        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
        plt.title('Sensitivity Analysis: Valuation ($)')
        st.pyplot(plt)
        plt.close()
    except Exception as e:
        logger.error(f"Error plotting sensitivity: {e}")
        st.error(f"Error plotting sensitivity: {e}")

    # Download Excel report
    try:
        logger.debug("Generating Excel report")
        export_to_excel(forecast, sensitivity, filename="treasury_report.xlsx")
        with open("treasury_report.xlsx", "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="treasury_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        st.error(f"Error generating report: {e}")
else:
    st.write("Please upload a cash_flows.csv file to begin.")
