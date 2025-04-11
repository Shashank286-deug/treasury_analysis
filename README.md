# Treasury & Investment Analysis

## Overview
A Python-based tool for cash flow forecasting, DCF valuation, and sensitivity analysis, enhanced for renewable energy financial reporting. Generates U.S. GAAP-compliant reports (EBITDA, budget vs. actual) for solar and wind projects, with audit-ready trial balance validation and simulated RPA automation.

## Features
- **Cash Flow Forecasting**: Projects future cash flows with user-defined growth rates.
- **DCF Valuation**: Uses real-time 10-year Treasury yields via yfinance or manual discount rates.
- **Sensitivity Analysis**: Evaluates valuation across growth and discount rate scenarios.
- **U.S. GAAP Reporting**: Computes EBITDA, budget vs. actual variance, and simplified balance sheets.
- **Audit Support**: Validates trial balances for renewable energy transactions.
- **Automation**: Simulated UiPath RPA for journal entry posting.
- **Visualization**: Streamlit dashboard with matplotlib/seaborn charts.

## Tech Stack
- Python (pandas, numpy, yfinance)
- Streamlit for dashboards
- Matplotlib/Seaborn for visualizations
- Xlsxwriter for Excel exports
- UiPath for RPA (simulated)

## How to Run
1. Clone the repo: `git clone [your-repo-url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Run Streamlit app: `streamlit run main.py`
4. View at `http://localhost:8501`.

## Sample Output
![Dashboard](screenshots/dashboard.png) *(Add after running app)*

## Project Structure
- `data/`: Cash flows and trial balance CSVs
- `outputs/`: U.S. GAAP reports
- `scripts/`: RPA scripts
- `data_input.py`: Loads CSV data
- `analysis.py`: Handles forecasting and valuation
- `reporting.py`: Generates reports
- `main.py`: Streamlit app

## Notes
- Originally built on April 11, 2025, with enhancements for renewable energy financial controlling.
- Live demo: [Add Streamlit URL after deployment]

---

By Shashank Singh, demonstrating financial analytics for renewable energy portfolios.
