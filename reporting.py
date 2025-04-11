import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_cash_flow_forecast(forecast):
    """Plot cash flow forecast."""
    plt.figure(figsize=(10, 6))
    plt.plot(forecast['Date'], forecast['Net Cash Flow'], label='Net Cash Flow')
    plt.title('Cash Flow Forecast')
    plt.xlabel('Date')
    plt.ylabel('Cash Flow ($)')
    plt.legend()
    plt.grid(True)
    plt.savefig('cash_flow_forecast.png')
    plt.close()

def plot_sensitivity_analysis(sensitivity):
    """Plot sensitivity analysis as a heatmap."""
    pivot = sensitivity.pivot(index='Growth Rate', columns='Discount Rate', values='Valuation')
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title('Sensitivity Analysis: Valuation ($)')
    plt.savefig('sensitivity_analysis.png')
    plt.close()

def export_to_excel(forecast, sensitivity, filename='treasury_report.xlsx'):
    """Export data to Excel."""
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        forecast.to_excel(writer, sheet_name='Cash Flow Forecast', index=False)
        sensitivity.to_excel(writer, sheet_name='Sensitivity Analysis', index=False)

if __name__ == "__main__":
    import analysis
    cash_flow_data = pd.read_csv('cash_flows.csv', parse_dates=['Date'])
    forecast = analysis.forecast_cash_flows(cash_flow_data)
    sensitivity = analysis.sensitivity_analysis(cash_flow_data)
    
    plot_cash_flow_forecast(forecast)
    plot_sensitivity_analysis(sensitivity)
    export_to_excel(forecast, sensitivity)
    print("Reports generated: cash_flow_forecast.png, sensitivity_analysis.png, treasury_report.xlsx")
