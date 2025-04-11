import streamlit as st
import pandas as pd
import plotly.express as px
from reporting import generate_financial_report, validate_trial_balance

st.set_page_config(page_title="Renewable Energy Financial Dashboard", layout="wide")

st.title("Renewable Energy Financial Dashboard")
st.markdown("U.S. GAAP-compliant reporting for solar and wind projects.")

# Load and display report
report = generate_financial_report("data/cash_flows.csv")
if report:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Metrics")
        st.metric("EBITDA", f"${report['EBITDA']:,.2f}")
        st.metric("Budget vs. Actual Variance", f"${report['Budget_vs_Actual']:,.2f}")
        st.metric("Variance %", f"{report['Variance_Percent']:.2f}%")
        st.metric("Discount Rate", f"{report['Discount_Rate']:.2%}")
    
    with col2:
        st.subheader("Balance Sheet")
        balance = report['Balance_Sheet']
        st.write(f"**Assets**: Cash = ${balance['Assets']['Cash']:,.2f}")
        st.write(f"**Liabilities**: Accounts Payable = ${balance['Liabilities']['Accounts Payable']:,.2f}")
        st.write(f"**Equity**: Retained Earnings = ${balance['Equity']['Retained Earnings']:,.2f}")

    # Cash Flow Chart
    df = pd.read_csv("data/cash_flows.csv")
    fig = px.line(df, x="Date", y=["Inflow", "Outflow", "Budget"], 
                  title="Cash Flow and Budget Comparison")
    st.plotly_chart(fig, use_container_width=True)

# Trial Balance Validation
st.subheader("Audit Readiness")
valid, message = validate_trial_balance("data/trial_balance.csv")
if valid:
    st.success(message)
else:
    st.error(message)

# Download Report
st.subheader("Download Reports")
with open("outputs/financial_report.csv", "rb") as file:
    st.download_button("Download Financial Report", file, "financial_report.csv")
