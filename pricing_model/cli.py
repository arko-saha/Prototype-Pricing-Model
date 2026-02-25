import argparse
import json
from pricing_model.forecaster import NaturalGasForecaster
from pricing_model.contract_pricer import ContractPricer

def main():
    parser = argparse.ArgumentParser(description="Natural Gas Contract Pricing CLI")
    parser.add_argument("--data", type=str, default="Nat_Gas.csv", help="Path to historical price data")
    parser.add_argument("--injection-dates", nargs="+", required=True, help="List of injection dates (YYYY-MM-DD)")
    parser.add_argument("--withdrawal-dates", nargs="+", required=True, help="List of withdrawal dates (YYYY-MM-DD)")
    parser.add_argument("--injection-rate", type=float, default=1e6, help="Injection rate in MMBtu")
    parser.add_argument("--withdrawal-rate", type=float, default=1e6, help="Withdrawal rate in MMBtu")
    parser.add_argument("--max-volume", type=float, default=2e6, help="Max storage volume in MMBtu")
    parser.add_argument("--storage-cost", type=float, default=100000, help="Monthly storage cost ($)")
    parser.add_argument("--fee", type=float, default=10000, help="Injection/Withdrawal fee per 1M MMBtu ($)")
    parser.add_argument("--transport", type=float, default=50000, help="Transport cost ($)")

    args = parser.parse_args()

    forecaster = NaturalGasForecaster(args.data)
    pricer = ContractPricer(forecaster)

    results = pricer.value_contract(
        args.injection_dates,
        args.withdrawal_dates,
        args.injection_rate,
        args.withdrawal_rate,
        args.max_volume,
        args.storage_cost,
        args.fee,
        args.transport
    )

    print("\n--- Contract Valuation Results ---")
    print(f"Contract Value: ${results['contract_value']:,.2f}")
    print(f"Total Revenue:  ${results['total_revenue']:,.2f}")
    print(f"Total Cost:     ${results['total_cost']:,.2f}")
    print(f"Remaining Vol:  {results['current_volume_remaining']:,} MMBtu")
    print("----------------------------------\n")

if __name__ == "__main__":
    main()
