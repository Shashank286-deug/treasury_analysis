import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import logging
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    st.warning("yfinance not available; Treasury yield feature disabled.")
from data_input import load_cash_flow_data
from analysis import forecast_cash_flows, dcf_valuation, sensitivity_analysis
from reporting import export_to_excel, generate_financial_report, validate_trial_balance

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.title("Renewable Energy Financial Dashboard")
st.markdown("U.S. GAAP-compliant reporting and cash flow analysis for solar and wind projects.")

# Sample data as fallback
sample_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01'],
    'Inflow': [100000, 120000, 110000, 130000, 115000, 125000],
    'Outflow': [80000, 90000, 85000, 95000, 87000, 92000],
    'Budget': [95000, 115000, 105000, 125000, 110000, 120000],
    'Description': ['Solar Energy Sales vs. Maintenance', 'Wind Turbine Revenue vs. Repairs', 
                    'Solar Panel Lease vs. Depreciation', 'Wind Energy Sales vs. Operations',
                    'Solar Energy Sales vs. Maintenance', 'Wind Turbine Revenue vs. Repairs']
})
sample_data['Date'] = pd.to_datetime(sample_data['Date'])

# File upload or use sample
use_sample = st.checkbox("Use Sample Data (if no CSV uploaded)", value=False)
uploaded_file = st.file_uploader("Upload Cash Flow Data (CSV)", type='csv')

if uploaded_file:
    try:
        logger.debug("Saving uploaded CSV to temp_cash_flows.csv")
        with open("temp_cash_flows.csv", "wb") as f:
            f.write(uploaded_file.read())
        
        logger.debug("Loading raw CSV")
        raw_df = pd.read_csv("temp_cash_flows.csv")
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        st.error(f"Error processing CSV: {e}")
        st.stop()
elif use_sample:
    raw_df = sample_data.copy()
    st.write("Using sample data:")
    st.write(raw_df.head())
else:
    st.write("Please upload a cash_flows.csv file or check 'Use Sample Data' to begin.")
    st.stop()

# Column mapping
st.write("Detected Columns:", list(raw_df.columns))
st.subheader("Map Your CSV Columns")
date_col = st.selectbox("Select Date Column", raw_df.columns)
inflow_col = st.selectbox("Select Inflow Column", raw_df.columns)
outflow_col = st.selectbox("Select Outflow Column", raw_df.columns)

# Create standardized DataFrame
try:
    logger.debug(f"Mapping columns: {date_col} -> Date, {inflow_col} -> Inflow, {outflow_col} -> Outflow")
    cash_flow_data = raw_df[[date_col, inflow_col, outflow_col]].copy()
    cash_flow_data.columns = ['Date', 'Inflow', 'Outflow']
    
    cash_flow_data['Date'] = pd.to_datetime(cash_flow_data['Date'], errors='coerce')
    if cash_flow_data['Date'].isnull().any():
        raise ValueError("Some dates could not be parsed. Please ensure the date column is in a valid format (e.g., YYYY-MM-DD).")
    
    cash_flow_data['Inflow'] = pd.to_numeric(cash_flow_data['Inflow'], errors='coerce')
    cash_flow_data['Outflow'] = pd.to_numeric(cash_flow_data['Outflow'], errors='coerce')
    if cash_flow_data['Inflow'].isnull().any() or cash_flow_data['Outflow'].isnull().any():
        raise ValueError("Inflow or Outflow contains non-numeric values. Please ensure these columns contain numbers.")
    
    if len(cash_flow_data) == 0:
        raise ValueError("CSV is empty. Please ensure the CSV contains data.")
    
    st.write("Standardized Data:", cash_flow_data.head())
    logger.debug(f"Standardized Data columns: {list(cash_flow_data.columns)}")
except Exception as e:
    logger.error(f"Error standardizing data: {e}")
    st.error(f"Error standardizing data: {e}")
    st.stop()

# U.S. GAAP Financial Report
st.subheader("U.S. GAAP Financial Metrics")
report = generate_financial_report(cash_flow_data)
if report:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("EBITDA", f"${report['EBITDA']:,.2f}")
        st.metric("Total Cash Flow", f"${report['Total_Cash_Flow']:,.2f}")
        st.metric("Budget vs. Actual Variance", f"${report['Budget_vs_Actual']:,.2f}")
        st.metric("Variance %", f"{report['Variance_Percent']:.2f}%")
    with col2:
        st.write("**Simplified Balance Sheet**")
        balance = report['Balance_Sheet']
        st.write(f"Assets: Cash = ${balance['Assets']['Cash']:,.2f}")
        st.write(f"Liabilities: Accounts Payable = ${balance['Liabilities']['Accounts Payable']:,.2f}")
        st.write(f"Equity: Retained Earnings = ${balance['Equity']['Retained Earnings']:,.2f}")
else:
    st.warning("Failed to generate financial report.")

# Audit Readiness
st.subheader("Audit Readiness")
valid, message = validate_trial_balance()
if valid:
    st.success(message)
else:
    st.warning(message)

# Original Forecast and Valuation
st.subheader("Cash Flow Forecast and Valuation")
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

# Valuation with yfinance
if YFINANCE_AVAILABLE:
    use_treasury_yield = st.checkbox("Use Current 10-Year Treasury Yield as Discount Rate", value=False)
else:
    use_treasury_yield = False

if use_treasury_yield:
    try:
        logger.debug("Fetching 10-year Treasury yield from yfinance")
        treasury = yf.Ticker("^TNX")
        treasury_data = treasury.history(period="1d")
        if treasury_data.empty:
            raise ValueError("Could not fetch Treasury yield data.")
        treasury_yield = treasury_data['Close'].iloc[-1] / 100
        discount_rate = treasury_yield
        st.write(f"Current 10-Year Treasury Yield: {treasury_yield*100:.2f}%")
    except Exception as e:
        logger.error(f"Error fetching Treasury yield: {e}")
        st.error(f"Error fetching Treasury yield: {e}. Falling back to manual input.")
        discount_rate = st.slider("Discount Rate (Manual Fallback)", 0.05, 0.15, 0.1, 0.01)
else:
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

# Download Reports
st.subheader("Download Reports")
# Original Excel Report
try:
    logger.debug("Generating Excel report")
    excel_data = export_to_excel(forecast, sensitivity)
    st.download_button(
        label="Download Forecast Report (Excel)",
        data=excel_data,
        file_name="treasury_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except Exception as e:
    logger.error(f"Error generating Excel report: {e}")
    st.error(f"Error generating Excel report: {e}")

# New U.S. GAAP Report
import os
report_path = "outputs/financial_report.csv"
if os.path.exists(report_path):
    with open(report_path, "rb") as file:
        st.download_button(
            label="Download U.S. GAAP Financial Report (CSV)",
            data=file,
            file_name="financial_report.csv",
            mime="text/csv"
        )
else:
    st.info("Financial report not yet generated. Displaying metrics above.")
