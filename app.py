import streamlit as st
import pandas as pd
import numpy as np

st.title("Sales, Inventory, and Profit Forecaster")

st.sidebar.header("Forecast settings")

# Inputs
periods = st.sidebar.slider("Forecast periods (months)", 3, 36, 12)
last_sales = st.sidebar.number_input("Last month units sold", min_value=0.0, value=100.0, step=10.0)
growth_rate = st.sidebar.number_input("Monthly sales growth rate (%)", -50.0, 200.0, 10.0) / 100
price = st.sidebar.number_input("Selling price per unit", min_value=0.0, value=25.0, step=1.0)
unit_cost = st.sidebar.number_input("Cost per unit", min_value=0.0, value=10.0, step=1.0)
safety_stock = st.sidebar.number_input("Safety stock (units)", min_value=0.0, value=50.0, step=10.0)
other_cost_per_period = st.sidebar.number_input("Other fixed costs per period", min_value=0.0, value=500.0, step=50.0)

# Forecast index
period_index = np.arange(1, periods + 1)

# Sales forecast
forecast_sales = last_sales * (1 + growth_rate) ** period_index

# Inventory requirement (simple)
required_inventory = forecast_sales + safety_stock

# Financials
revenue = forecast_sales * price
cogs = forecast_sales * unit_cost
profit = revenue - cogs - other_cost_per_period

df = pd.DataFrame({
    "Period": period_index,
    "Forecast Sales (units)": forecast_sales.round(2),
    "Required Inventory (units)": required_inventory.round(2),
    "Revenue": revenue.round(2),
    "COGS": cogs.round(2),
    "Profit": profit.round(2),
})

st.subheader("Forecast table")
st.dataframe(df)

st.subheader("Sales vs Inventory")
st.line_chart(df.set_index("Period")[["Forecast Sales (units)", "Required Inventory (units)"]])

st.subheader("Profit over time")
st.line_chart(df.set_index("Period")[["Profit"]])

st.caption("Starter model – you can later add multiple products, seasonality, and more advanced forecasting.")
