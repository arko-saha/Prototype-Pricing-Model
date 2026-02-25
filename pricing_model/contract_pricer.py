import pandas as pd
from datetime import datetime

class ContractPricer:
    """
    Evaluates the value of natural gas storage contracts.
    """
    def __init__(self, forecaster):
        self.forecaster = forecaster

    def value_contract(self, 
                       injection_dates, 
                       withdrawal_dates, 
                       injection_rate, 
                       withdrawal_rate, 
                       max_volume, 
                       storage_cost_per_month, 
                       injection_withdrawal_cost_per_mmbtu, 
                       transport_cost):
        """
        Calculates the valuation of the contract.
        """
        # Convert dates
        inj_dates = [pd.to_datetime(d) for d in injection_dates]
        with_dates = [pd.to_datetime(d) for d in withdrawal_dates]

        total_revenue = 0
        total_cost = 0
        current_volume = 0

        # 1. Injection Phase
        for date in inj_dates:
            price = self.forecaster.predict(date)
            # Calculate volume to inject: limited by rate and capacity
            volume = min(injection_rate, max_volume - current_volume)
            current_volume += volume
            
            # Cost = Purchase Price + Variable Injection Fee
            # (Logic matches notebook: injection_withdrawal_cost_per_mmbtu is per 1M MMBtu in the example)
            # Dividing by 1e6 because the notebook units suggest 'per 1M MMBtu'
            fee = (injection_withdrawal_cost_per_mmbtu * volume / 1e6)
            injection_cost = (price * volume) + fee
            total_cost += injection_cost

        # 2. Storage Phase
        # Storage cost is based on the duration the gas is held.
        # Simple duration Calc: Max withdrawal - Min injection
        if inj_dates and with_dates:
            storage_months = max(0, (max(with_dates) - min(inj_dates)).days // 30)
            storage_cost = storage_cost_per_month * storage_months
            total_cost += storage_cost

        # 3. Withdrawal Phase
        for date in with_dates:
            price = self.forecaster.predict(date)
            # Volume to withdraw: limited by rate and current inventory
            volume = min(withdrawal_rate, current_volume)
            current_volume -= volume
            
            # Revenue = Sale Price - Variable Withdrawal Fee
            fee = (injection_withdrawal_cost_per_mmbtu * volume / 1e6)
            revenue = (price * volume) - fee
            total_revenue += revenue

        # 4. Transport Costs
        # Usually incurred for both ways
        total_cost += (transport_cost * 2)

        contract_value = total_revenue - total_cost
        
        return {
            "contract_value": contract_value,
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "current_volume_remaining": current_volume
        }
