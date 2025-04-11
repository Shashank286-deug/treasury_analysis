import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def export_to_excel(forecast, sensitivity, filename='treasury_report.xlsx'):
    """Export data to Excel."""
    if forecast.empty or sensitivity.empty:
        raise ValueError("Cannot export empty forecast or sensitivity data")
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        forecast.to_excel(writer, sheet_name='Cash Flow Forecast', index=False)
        sensitivity.to_excel(writer, sheet_name='Sensitivity Analysis', index=False)
