import pytest
import pandas as pd
from pricing_model.forecaster import NaturalGasForecaster
from pricing_model.contract_pricer import ContractPricer
import os

def test_forecaster_initialization():
    # Ensure it loads historical data
    forecaster = NaturalGasForecaster("Nat_Gas.csv")
    df = forecaster.get_historical_data()
    assert not df.empty
    assert "Prices" in df.columns

def test_forecaster_prediction():
    forecaster = NaturalGasForecaster("Nat_Gas.csv")
    # Test historical date
    price = forecaster.predict("2020-10-31")
    assert price == 10.1
    
    # Test future date
    future_price = forecaster.predict("2025-10-31")
    assert isinstance(future_price, float)

def test_contract_pricer():
    forecaster = NaturalGasForecaster("Nat_Gas.csv")
    pricer = ContractPricer(forecaster)
    
    results = pricer.value_contract(
        injection_dates=["2020-10-31"],
        withdrawal_dates=["2024-09-30"],
        injection_rate=1e6,
        withdrawal_rate=1e6,
        max_volume=2e6,
        storage_cost_per_month=100000,
        injection_withdrawal_cost_per_mmbtu=10000,
        transport_cost=50000
    )
    
    assert "contract_value" in results
    assert results["total_revenue"] > 0
    assert results["total_cost"] > 0
