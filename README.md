# Treasury & Investment Analysis

## Overview
A Python-based tool for U.S. GAAP-compliant financial reporting and cash flow analysis, tailored for renewable energy projects (solar and wind). Generates management reports (EBITDA, budget vs. actual), validates trial balances for audits, and automates journal entries using RPA.

## Features
- **Financial Reporting**: EBITDA, balance sheet, and budget vs. actual variance for renewable energy assets.
- **Real-Time Data**: Integrates Treasury yields via yfinance for discount rate calculations.
- **Audit Support**: Validates trial balances to ensure U.S. GAAP compliance.
- **Automation**: UiPath RPA for journal entry posting and Streamlit for interactive dashboards.
- **Visualization**: Plotly charts for cash flow and budget comparisons.

## Tech Stack
- Python (pandas, numpy, yfinance)
- Streamlit for web dashboards
- Plotly for data visualization
- UiPath for RPA (simulated)
- CSV/Excel for data handling

## How to Run
1. Clone the repo: `git clone [your-repo-url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Run Streamlit app: `streamlit run main.py`
4. View reports at `http://localhost:8501` or check `outputs/` folder.

## Sample Output
![Financial Dashboard](screenshots/dashboard.png)

## Project Structure
- `data/`: Sample cash flows and trial balance CSVs
- `outputs/`: Exported reports (CSV)
- `scripts/`: RPA automation scripts
- `data_input.py`: Loads and validates data
- `analysis.py`: Performs financial calculations
- `reporting.py`: Generates U.S. GAAP reports
- `main.py`: Streamlit app for visualization

## Future Enhancements
- Add tax reporting for renewable energy incentives
- Export reports in XBRL for regulatory compliance
- Integrate cloud-based audit logs

## Live Demo
[Streamlit App URL - Update after deployment]

---

Built by Shashank Singh to demonstrate financial controlling skills for renewable energy portfolios.
