import streamlit as st
import pandas as pd
import plotly.express as px
from reporting import generate_financial_report, validate_trial_balance

st.set_page_config(page_title="Renewable Energy Financial Dashboard", layout="wide")

st.title("Renewable Energy Financial Dashboard")
st.markdown("U.S. GAAP-compliant reporting for solar and wind projects, with cash flow analysis.")

# Generate and display report
report = generate_financial_report("data/cash_flows.csv")
if report:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Metrics")
        st.metric("Total Cash Flow", f"${report['Total_Cash_Flow']:,.2f}")  # Original
        st.metric("EBITDA", f"${report['EBITDA']:,.2f}")                    # New
        st.metric("Budget vs. Actual Variance", f"${report['Budget_vs_Actual']:,.2f}")
        st.metric("Variance %", f"{report['Variance_Percent']:.2f}%")
        st.metric("Discount Rate", f"{report['Discount_Rate']:.2%}")        # Original
    
    with col2:
        st.subheader("Balance Sheet (Simplified)")
        balance = report['Balance_Sheet']
        st.write(f"**Assets**: Cash = ${balance['Assets']['Cash']:,.2f}")
        st.write(f"**Liabilities**: Accounts Payable = ${balance['Liabilities']['Accounts Payable']:,.2f}")
        st.write(f"**Equity**: Retained Earnings = ${balance['Equity']['Retained Earnings']:,.2f}")

    # Original: Cash Flow Chart, updated with Budget
    df = pd.read_csv("data/cash_flows.csv")
    fig = px.line(df, x="Date", y=["Inflow", "Outflow", "Budget"], 
                  title="Cash Flow and Budget Comparison")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Failed to generate financial report. Check data files.")

# Audit Readiness
st.subheader("Audit Readiness")
valid, message = validate_trial_balance("data/trial_balance.csv")
if valid:
    st.success(message)
else:
    st.warning(message)

# Download Report
st.subheader("Download Reports")
import os
report_path = "outputs/financial_report.csv"
if os.path.exists(report_path):
    with open(report_path, "rb") as file:
        st.download_button("Download Financial Report", file, "financial_report.csv")
else:
    st.info("Generating report... Refresh in a moment.")

# Note about automation
st.subheader("Process Automation")
st.markdown("Journal entries automated via RPA (simulated). See `scripts/journal_entry_bot.py`.")
