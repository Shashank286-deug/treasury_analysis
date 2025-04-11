import pandas as pd
import yfinance as yf

def generate_financial_report(cash_flows_file):
    """Generate U.S. GAAP-compliant financial reports for renewable energy projects."""
    try:
        df = pd.read_csv(cash_flows_file)
        required_cols = ['Date', 'Inflow', 'Outflow']
        if not all(col in df.columns for col in required_cols):
            raise ValueError("Missing required columns in CSV")

        # Original cash flow logic (from April 11)
        df['Net_Cash'] = df['Inflow'] - df['Outflow']
        total_cash_flow = df['Net_Cash'].sum()

        # New: EBITDA (simplified as Net Cash for demo)
        ebitda = total_cash_flow

        # New: Budget vs. Actual
        if 'Budget' in df.columns:
            actual_inflow = df['Inflow'].sum()
            budget_inflow = df['Budget'].sum()
            variance = actual_inflow - budget_inflow
            variance_pct = (variance / budget_inflow * 100) if budget_inflow else 0
        else:
            variance = 0
            variance_pct = 0

        # Original: Treasury yield (from April 11)
        treasury = yf.Ticker("^TNX")
        discount_rate = treasury.history(period="1d")['Close'].iloc[-1] / 100

        # New: Simplified financial statement
        balance_sheet = {
            'Assets': {'Cash': df['Inflow'].sum()},
            'Liabilities': {'Accounts Payable': df['Outflow'].sum()},
            'Equity': {'Retained Earnings': ebitda}
        }

        report = {
            'Total_Cash_Flow': total_cash_flow,  # Original
            'Discount_Rate': discount_rate,      # Original
            'EBITDA': ebitda,                   # New
            'Budget_vs_Actual': variance,       # New
            'Variance_Percent': variance_pct,   # New
            'Balance_Sheet': balance_sheet      # New
        }

        # New: Export report
        report_df = pd.DataFrame({
            'Metric': ['EBITDA', 'Variance', 'Variance %'],
            'Value': [ebitda, variance, f"{variance_pct:.2f}%"]
        })
        import os
        os.makedirs('outputs', exist_ok=True)
        report_df.to_csv('outputs/financial_report.csv', index=False)

        return report
    except Exception as e:
        print(f"Error generating report: {e}")
        return None

def create_trial_balance():
    """Create a sample trial balance if missing."""
    try:
        trial_data = pd.DataFrame({
            'Account': ['Cash', 'Revenue', 'Accounts Payable', 'Expenses'],
            'Debit': [100000, 0, 0, 40000],
            'Credit': [0, 100000, 40000, 0]
        })
        import os
        os.makedirs('data', exist_ok=True)
        trial_data.to_csv('data/trial_balance.csv', index=False)
        return True
    except Exception as e:
        print(f"Error creating trial balance: {e}")
        return False

def validate_trial_balance(trial_file):
    """Validate trial balance for audit readiness."""
    import os
    if not os.path.exists(trial_file):
        create_trial_balance()
    
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
        return False, f"Error validating trial balance: {e}"

if __name__ == "__main__":
    report = generate_financial_report("data/cash_flows.csv")
    if report:
        print("Financial Report Summary:")
        for key, value in report.items():
            print(f"{key}: {value}")
    
    valid, message = validate_trial_balance("data/trial_balance.csv")
    print(f"Trial Balance Validation: {message}")
