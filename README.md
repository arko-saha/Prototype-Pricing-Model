# Prototype Pricing Model (Natural Gas)

A production-grade implementation of a natural gas contract evaluation tool. This project transforms a prototype Jupyter notebook into a modular Python package with price forecasting and a web interface.

## 🚀 Overview

This tool calculates the net value of a natural gas storage contract. It considers:
- **Injection/Withdrawal Schedules**: Dates when gas is purchased/sold.
- **Price Forecasting**: Uses an **ARIMA (AutoRegressive Integrated Moving Average)** model to estimate future gas prices based on historical trends in `Nat_Gas.csv`.
- **Operational Costs**: Includes storage fees, transport costs, and injection/withdrawal processing fees.
- **Inventory Management**: Tracks gas volume in storage relative to capacity limits.

## 🛠️ Project Structure

- `pricing_model/`: Core Python package.
  - `forecaster.py`: ARIMA-based price prediction engine.
  - `contract_pricer.py`: Business logic for contract valuation.
  - `cli.py`: Command-line interface for rapid analysis.
- `app.py`: Streamlit-based web dashboard for interactive visualization.
- `Nat_Gas.csv`: Historical natural gas price dataset.
- `tests/`: Automated unit tests for logic verification.

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arko-saha/Prototype-Pricing-Model.git
   cd Prototype-Pricing-Model
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📈 Usage

### Web Interface (Recommended)
Run the Streamlit dashboard for a visual experience:
```bash
streamlit run app.py
```

### Command Line
Price a contract directly from the terminal:
```bash
python -m pricing_model.cli --injection-dates 2020-10-31 2021-02-28 --withdrawal-dates 2024-09-30 2024-02-29
```

### Programmatic Access
```python
from pricing_model.forecaster import NaturalGasForecaster
from pricing_model.contract_pricer import ContractPricer

forecaster = NaturalGasForecaster("Nat_Gas.csv")
pricer = ContractPricer(forecaster)

# Value your contract
results = pricer.value_contract(
    injection_dates=['2021-01-01'],
    withdrawal_dates=['2022-01-01'],
    ...
)
print(results['contract_value'])
```

## 📝 Methodology & Mathematical Model

### Core Valuation Logic (`price_contract`)
The valuation follows a standard Profit & Loss (P&L) formula for natural gas storage contracts:
**`Contract Value = (Withdrawal Revenues - Withdrawal Fees) - (Injection Costs + Injection Fees) - (Storage Costs) - (Transport Costs)`**

#### Detailed Components:
- **Injection Cost**: Calculated as `(Purchase Price * Volume) + (Injection fee * Volume / 1e6)`.
- **Withdrawal Revenue**: Calculated as `(Sale Price * Volume) - (Withdrawal fee * Volume / 1e6)`.
- **Storage Cost**: Calculated based on the number of months the gas is held: `Monthly Storage Cost * Storage Duration (Months)`.
- **Transport Cost**: Assumed to be incurred twice (to and from the facility).

#### Step-by-Step Calculation Process:
1. **Date Conversion**: All dates are normalized to datetime objects.
2. **Price Forecasting**: The system identifies the market price for the specific dates using historical data or the ARIMA forecasting model.
3. **Injection Analysis**: For each injection date, the system calculates the volume to be stored (capped by daily injection rates and total storage capacity). 
4. **Storage Evaluation**: The duration between the first injection and last withdrawal is calculated to determine total storage overhead.
5. **Withdrawal Analysis**: For each withdrawal date, the system calculates the revenue from selling the stored inventory (capped by daily withdrawal rates and current available volume).
6. **Final Valuation**: Sums all variable revenues and subtracts all fixed and variable costs.

### Price Forecasting (ARIMA)
Natural gas prices exhibit significant cycles. This project uses the `statsmodels` implementation of the **ARIMA (AutoRegressive Integrated Moving Average)** algorithm (specifically an ARIMA(1,1,1) configuration) to project future price movements, enabling the valuation of forward-dated contracts.

## 🧪 Testing
Run the test suite to ensure accuracy:
```bash
pytest tests/
```
