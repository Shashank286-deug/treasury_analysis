import pandas as pd
from io import BytesIO

def export_to_excel(forecast, sensitivity, output_buffer):
    """Export data to Excel using an in-memory buffer with openpyxl."""
    if forecast.empty or sensitivity.empty:
        raise ValueError("Cannot export empty forecast or sensitivity data")
    with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
        forecast.to_excel(writer, sheet_name='Cash Flow Forecast', index=False)
        sensitivity.to_excel(writer, sheet_name='Sensitivity Analysis', index=False)
