import pandas as pd

def load_cash_flow_data(file_path):
    """Load cash flow data from CSV."""
    df = pd.read_csv(file_path, parse_dates=['Date'])
    return df

if __name__ == "__main__":
    cash_flow_data = load_cash_flow_data('cash_flows.csv')
    print("Cash Flow Data:\n", cash_flow_data)
