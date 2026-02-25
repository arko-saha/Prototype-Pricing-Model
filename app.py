import streamlit as st
import pandas as pd
import plotly.express as px
from pricing_model.forecaster import NaturalGasForecaster
from pricing_model.contract_pricer import ContractPricer
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Gas Price Optimizer", layout="wide")

st.title("🔥 Natural Gas Contract Pricing Model")
st.markdown("""
This application helps you evaluate natural gas trading contracts by forecasting future prices 
and calculating the net value of storage-based operations.
""")

# Sidebar for Inputs
st.sidebar.header("📁 Data & Parameters")
data_path = st.sidebar.text_input("Data Source", "Nat_Gas.csv")

st.sidebar.header("🔧 Contract Constraints")
max_volume = st.sidebar.number_input("Max Storage (MMBtu)", value=2000000, step=100000)
inj_rate = st.sidebar.number_input("Injection Rate (MMBtu/day)", value=1000000, step=100000)
with_rate = st.sidebar.number_input("Withdrawal Rate (MMBtu/day)", value=1000000, step=100000)

st.sidebar.header("💰 Costs")
storage_cost = st.sidebar.number_input("Monthly Storage Cost ($)", value=100000, step=10000)
fee = st.sidebar.number_input("Inj/With Fee ($ per 1M MMBtu)", value=10000, step=1000)
transport = st.sidebar.number_input("Transport Cost ($)", value=50000, step=5000)

# Initialize Backend
@st.cache_resource
def get_backend(path):
    forecaster = NaturalGasForecaster(path)
    pricer = ContractPricer(forecaster)
    return forecaster, pricer

try:
    forecaster, pricer = get_backend(data_path)
    
    # Main Dashboard
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📅 Schedule Injection & Withdrawal")
        
        # Injections
        st.write("**Injections**")
        inj_dates_input = st.text_area("Injection Dates (YYYY-MM-DD, comma separated)", "2020-10-31, 2021-02-28")
        inj_dates = [d.strip() for d in inj_dates_input.split(",") if d.strip()]
        
        # Withdrawals
        st.write("**Withdrawals**")
        with_dates_input = st.text_area("Withdrawal Dates (YYYY-MM-DD, comma separated)", "2024-09-30, 2024-02-29")
        with_dates = [d.strip() for d in with_dates_input.split(",") if d.strip()]

        if st.button("Calculate Contract Value"):
            results = pricer.value_contract(
                inj_dates, with_dates, inj_rate, with_rate, 
                max_volume, storage_cost, fee, transport
            )
            
            st.success(f"### Contract Value: ${results['contract_value']:,.2f}")
            
            # Metrics
            m1, m2 = st.columns(2)
            m1.metric("Total Revenue", f"${results['total_revenue']:,.2f}")
            m2.metric("Total Cost", f"${results['total_cost']:,.2f}")
            
            if results['contract_value'] < 0:
                st.warning("⚠️ This contract is currently projected to be unprofitable.")
            else:
                st.balloons()

    with col2:
        st.subheader("📈 Price Forecast (ARIMA)")
        hist_df = forecaster.get_historical_data()
        
        # Generate some future dates for visualization
        last_date = hist_df['Dates'].max()
        future_dates = [last_date + timedelta(days=30*i) for i in range(1, 13)]
        future_prices = [forecaster.predict(d) for d in future_dates]
        
        forecast_df = pd.DataFrame({'Dates': future_dates, 'Prices': future_prices, 'Type': 'Forecast'})
        hist_df['Type'] = 'Historical'
        
        viz_df = pd.concat([hist_df, forecast_df])
        
        fig = px.line(viz_df, x='Dates', y='Prices', color='Type', 
                      title="Natural Gas Prices: Historical vs Forecast")
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading model: {e}")
    st.info("Ensure Nat_Gas.csv is in the correct format and path.")

st.divider()
st.caption("Developed as part of the MLOps Prototype Pricing Model project.")
