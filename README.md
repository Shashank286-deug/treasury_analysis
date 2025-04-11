# Treasury & Investment Analysis

## Overview
A Python-based tool for cash flow analysis and financial reporting, now enhanced for renewable energy projects (solar and wind). Generates U.S. GAAP-compliant reports, including EBITDA and budget vs. actual analysis, with audit-ready trial balance validation and simulated RPA automation.

## Features
- **Cash Flow Analysis**: Forecasts cash flows using real-time Treasury yields via yfinance (original feature).
- **Financial Reporting**: U.S. GAAP-compliant EBITDA, variance analysis, and simplified balance sheet.
- **Audit Support**: Validates trial balances for renewable energy transactions.
- **Visualization**: Streamlit dashboard with cash flow and budget comparison charts.
- **Automation**: Simulated UiPath RPA for journal entry posting.

## Tech Stack
- Python (pandas, numpy, yfinance)
- Streamlit for dashboards
- Plotly for charts
- UiPath for RPA (simulated)
- CSV for data

## How to Run
1. Clone the repo: `git clone [your-repo-url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Run Streamlit app: `streamlit run main.py`
4. View at `http://localhost:8501` or check `outputs/` folder.

## Sample Output
![Dashboard](screenshots/dashboard.png) *(Add after running app)*

## Project Structure
- `data/`: Cash flows and trial balance CSVs
- `outputs/`: Exported reports
- `scripts/`: RPA scripts
- `data_input.py`: Loads data
- `analysis.py`: Calculates cash flows
- `reporting.py`: Generates reports
- `main.py`: Streamlit app

## Notes
- Built on April 11, 2025, with enhancements for renewable energy financial controlling.
- Live demo: [Add Streamlit URL after deployment]

---

By Shashank Singh, showcasing financial analytics for renewable energy.
