import streamlit as st

# Add this right after other imports and before st.title
st.markdown('<button class="open-btn" onclick="openSidebar()">Guidance</button><div id="sidebar" class="sidebar"></div>', unsafe_allow_html=True)
with open('User_Guidance_Sidebar.html', 'r', encoding='utf-8') as file:
    manual_content = file.read().replace('<button class="open-btn" onclick="openSidebar()">Guidance</button>', '')
st.markdown(f'<script>{manual_content.split("<script>")[1].split("</script>")[0]}</script>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import logging
import numpy as np
from io import BytesIO
import zipfile
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    logger.warning("yfinance not available; Treasury yield feature disabled.")
from data_input import load_cash_flow_data
from analysis import forecast_cash_flows, dcf_valuation, sensitivity_analysis
from reporting import export_to_excel

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.title("Treasury & Investment Analysis")

# Add CSS for background images with transparency and curve
st.markdown(
    """
    <style>
    .upload-section {
        background-image: url('solar_icon.jpg');
        background-size: cover;
        background-position: center;
        position: relative;
        padding: 20px;
        border-radius: 100%;
        opacity: 0.6;
    }
    .later-sections {
        background-image: url('wind_turbine_icon.jpg');
        background-size: cover;
        background-position: center;
        position: relative;
        padding: 20px;
        opacity: 0.6;
    }
    .content {
        position: relative;
        z-index: 1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Upload section with solar_icon background
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
use_sample = st.checkbox("Use Sample Data (if no CSV uploaded)", value=False)
uploaded_file = st.file_uploader("Upload Cash Flow Data (CSV)", type='csv')
st.markdown('</div>', unsafe_allow_html=True)

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
    raw_df = pd.DataFrame({
        'Date': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01'],
        'Inflow': [100000, 120000, 110000, 130000, 115000, 125000],
        'Outflow': [80000, 90000, 85000, 95000, 87000, 92000]
    })
    raw_df['Date'] = pd.to_datetime(raw_df['Date'])
    st.write("Using sample data:")
    st.write(raw_df.head())
else:
    st.write("Please upload a cash_flows.csv file or check 'Use Sample Data' to begin.")
    st.stop()

# Later sections with wind_turbine_icon background
st.markdown('<div class="later-sections">', unsafe_allow_html=True)
st.markdown('<div class="content">', unsafe_allow_html=True)
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

# Valuation with yfinance integration
st.subheader("DCF Valuation")
if YFINANCE_AVAILABLE:
    use_treasury_yield = st.checkbox("Use Current 10-Year Treasury Yield as Discount Rate", value=False)
else:
    st.warning("Real-time Treasury yield feature unavailable due to missing yfinance library.")
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
        st.write(f"Current 10-Year Treasury Yield: {treasury_yield*100:.2f}% (used as discount rate)")
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

# Renewable Energy Risk-Adjusted Return Metric (RARM)
st.subheader("Renewable Energy Risk-Adjusted Return Metric (RARM)")
initial_investment = st.number_input("Initial Investment ($)", min_value=1.0, value=1000000.0, step=10000.0)
st.write("Estimate risks affecting renewable energy projects (0 = no risk, 1 = extreme risk):")
policy_risk = st.slider("Policy Risk (e.g., subsidy changes)", 0.0, 1.0, 0.2, 0.05)
intermittency_risk = st.slider("Intermittency Risk (e.g., weather variability)", 0.0, 1.0, 0.2, 0.05)
market_risk = st.slider("Market Risk (e.g., price volatility)", 0.0, 1.0, 0.2, 0.05)
operational_risk = st.slider("Operational Risk (e.g., maintenance issues)", 0.0, 1.0, 0.2, 0.05)

try:
    # Equal weights for simplicity; can be customized
    total_risk_score = (policy_risk + intermittency_risk + market_risk + operational_risk) / 4
    rarm = (valuation / initial_investment) * (1 - total_risk_score)
    st.write(f"**RARM**: {rarm*100:.2f}%")
    st.write(f"(Expected return adjusted for {total_risk_score*100:.1f}% total risk)")
except Exception as e:
    logger.error(f"Error calculating RARM: {e}")
    st.error(f"Error calculating RARM: {e}")

# Sensitivity Analysis
st.subheader("Sensitivity Analysis")
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
    fig1 = plt.figure(figsize=(10, 6))
    plt.plot(forecast['Date'], forecast['Net Cash Flow'], label='Net Cash Flow')
    plt.title('Cash Flow Forecast')
    plt.xlabel('Date')
    plt.ylabel('Cash Flow ($)')
    plt.legend()
    plt.grid(True)
    # Display forecast chart
    st.pyplot(fig1)
    # Save forecast chart to buffer
    forecast_buf = io.BytesIO()
    fig1.savefig(forecast_buf, format='png', bbox_inches='tight')
    plt.close(fig1)  # Close specific figure
except Exception as e:
    logger.error(f"Error plotting forecast: {e}")
    st.error(f"Error plotting forecast: {e}")
    forecast_buf = None

try:
    logger.debug("Plotting sensitivity heatmap")
    fig2 = plt.figure(figsize=(10, 6))
    pivot = sensitivity.pivot(index='Growth Rate', columns='Discount Rate', values='Valuation')
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title('Sensitivity Analysis: Valuation ($)')
    # Display sensitivity chart
    st.pyplot(fig2)
    # Save sensitivity chart to buffer
    sensitivity_buf = io.BytesIO()
    fig2.savefig(sensitivity_buf, format='png', bbox_inches='tight')
    plt.close(fig2)  # Close specific figure
except Exception as e:
    logger.error(f"Error plotting sensitivity: {e}")
    st.error(f"Error plotting sensitivity: {e}")
    sensitivity_buf = None

# Download Excel report using BytesIO
st.subheader("Download Report")
try:
    logger.debug("Generating Excel report in memory")
    output = BytesIO()
    export_to_excel(forecast, sensitivity, output)
    output.seek(0)

    # Create ZIP file with Excel and chart images
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add Excel file
        zip_file.writestr("treasury_report.xlsx", output.getvalue())
        # Add forecast chart if available
        if forecast_buf:
            forecast_buf.seek(0)
            zip_file.writestr("cash_flow_forecast.png", forecast_buf.getvalue())
        # Add sensitivity chart if available
        if sensitivity_buf:
            sensitivity_buf.seek(0)
            zip_file.writestr("sensitivity_analysis.png", sensitivity_buf.getvalue())

    zip_buffer.seek(0)
    st.download_button(
        label="Download All Data (ZIP)",
        data=zip_buffer,
        file_name="treasury_analysis_report.zip",
        mime="application/zip"
    )
    # Keep the original Excel download option
    st.download_button(
        label="Download Report (Excel Only)",
        data=output,
        file_name="treasury_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except Exception as e:
    logger.error(f"Error generating report: {e}")
    st.error(f"Error generating report: {e}")
st.markdown('</div>', unsafe_allow_html=True)  # Close content div
st.markdown('</div>', unsafe_allow_html=True)  # Close later-sections div
