import pandas as pd
import numpy as np

def forecast_cash_flows(cash_flow_data, periods=12, growth_rate=0.02):
    """Forecast future cash flows based on historical data."""
    last_cash_flow = cash_flow_data[['Inflow', 'Outflow']].iloc[-1]
    forecast = []
    
    for i in range(periods):
        date = pd.to_datetime(cash_flow_data['Date'].iloc[-1]) + pd.offsets.MonthEnd(i+1)
        inflow = last_cash_flow['Inflow'] * (1 + growth_rate) ** (i+1)
        outflow = last_cash_flow['Outflow'] * (1 + growth_rate) ** (i+1)
        forecast.append([date, inflow, outflow])
    
    forecast_df = pd.DataFrame(forecast, columns=['Date', 'Inflow', 'Outflow'])
    forecast_df['Net Cash Flow'] = forecast_df['Inflow'] - forecast_df['Outflow']
    return forecast_df

def dcf_valuation(cash_flows, discount_rate=0.1, terminal_growth=0.02):
    """Calculate DCF valuation."""
    cash_flows = cash_flows['Net Cash Flow'].values
    periods = len(cash_flows)
    
    discounted_cf = [cf / (1 + discount_rate) ** (i+1) for i, cf in enumerate(cash_flows)]
    terminal_value = cash_flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    discounted_terminal = terminal_value / (1 + discount_rate) ** periods
    
    valuation = sum(discounted_cf) + discounted_terminal
    return valuation

def sensitivity_analysis(cash_flow_data, base_growth=0.02, base_discount=0.1):
    """Perform sensitivity analysis on growth rate and discount rate."""
    growth_rates = np.arange(base_growth - 0.02, base_growth + 0.03, 0.01)
    discount_rates = np.arange(base_discount - 0.02, base_discount + 0.03, 0.01)
    
    results = []
    for g in growth_rates:
        for d in discount_rates:
            forecast = forecast_cash_flows(cash_flow_data, growth_rate=g)
            valuation = dcf_valuation(forecast, discount_rate=d)
            results.append([g, d, valuation])
    
    return pd.DataFrame(results, columns=['Growth Rate', 'Discount Rate', 'Valuation'])

if __name__ == "__main__":
    cash_flow_data = pd.read_csv('cash_flows.csv', parse_dates=['Date'])
    forecast = forecast_cash_flows(cash_flow_data)
    print("Cash Flow Forecast:\n", forecast.head())
    
    valuation = dcf_valuation(forecast)
    print(f"DCF Valuation: ${valuation:,.2f}")
    
    sensitivity = sensitivity_analysis(cash_flow_data)
    print("Sensitivity Analysis:\n", sensitivity.head())
