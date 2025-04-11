import pandas as pd
import yfinance as yf
from datetime import datetime

def generate_financial_report(cash_flows_file):
    """Generate U.S. GAAP-compliant financial reports for renewable energy projects."""
    try:
        df = pd.read_csv(cash_flows_file)
        required_cols = ['Date', 'Inflow', 'Outflow', 'Budget']
        if not all(col in df.columns for col in required_cols):
            raise ValueError("Missing required columns in CSV")

        # Calculate EBITDA (simplified: Revenue - Operating Expenses)
        df['Net_Cash'] = df['Inflow'] - df['Outflow']
        ebitda = df['Net_Cash'].sum()

        # Budget vs. Actual Analysis
        actual_inflow = df['Inflow'].sum()
        budget_inflow = df['Budget'].sum()
        variance = actual_inflow - budget_inflow
        variance_pct = (variance / budget_inflow * 100) if budget_inflow else 0

        # Fetch Treasury yield for discount rate
        treasury = yf.Ticker("^TNX")
        discount_rate = treasury.history(period="1d")['Close'].iloc[-1] / 100

        # Simplified Balance Sheet
        balance_sheet = {
            'Assets': {'Cash': actual_inflow},
            'Liabilities': {'Accounts Payable': df['Outflow'].sum()},
            'Equity': {'Retained Earnings': ebitda}
        }

        report = {
            'EBITDA': ebitda,
            'Discount_Rate': discount_rate,
            'Budget_vs_Actual': variance,
            'Variance_Percent': variance_pct,
            'Balance_Sheet': balance_sheet
        }

        # Export to CSV
        report_df = pd.DataFrame({
            'Metric': ['EBITDA', 'Variance', 'Variance %'],
            'Value': [ebitda, variance, f"{variance_pct:.2f}%"]
        })
        report_df.to_csv('outputs/financial_report.csv', index=False)

        return report
    except Exception as e:
        print(f"Error generating report: {e}")
        return None

def validate_trial_balance(trial_file):
    """Validate trial balance for audit readiness."""
    try:
        df = pd.read_csv(trial_file)
        if 'Debit' not in df.columns or 'Credit' not in df.columns:
            raise ValueError("Missing Debit or Credit columns")
        
        total_debit = df['Debit'].sum()
        total_credit = df['Credit'].sum()
        
        if abs(total_debit - total_credit) < 0.01:
            return True, "Trial balance is valid"
        else:
            return False, f"Trial balance mismatch: Debit={total_debit}, Credit={total_credit}"
    except Exception as e:
        print(f"Error validating trial balance: {e}")
        return False, str(e)

if __name__ == "__main__":
    report = generate_financial_report("data/cash_flows.csv")
    if report:
        print("Financial Report Summary:")
        for key, value in report.items():
            print(f"{key}: {value}")
    
    valid, message = validate_trial_balance("data/trial_balance.csv")
    print(f"Trial Balance Validation: {message}")
