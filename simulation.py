import streamlit as st
import pandas as pd

# Setting the page configuration
st.set_page_config(page_title="XDC Network Simulation", layout="wide")

# Title for the app
st.title("XDC Network Simulation Tool")

# Sidebar inputs
st.sidebar.header("Input Parameters")
total_xdc_supply = st.sidebar.number_input("Total XDC Supply", value=37937187247, format="%d")
daily_txs = st.sidebar.number_input("Daily Number of Transactions",value=500000, format="%d")
avg_tx_fee = st.sidebar.number_input("Average tx fee",value=0.0002, format="%f")
num_standby_nodes = st.sidebar.number_input("Number of Standby Masternodes",value=108, format="%d")
num_validator_nodes = st.sidebar.number_input("Number of Validator Masternodes",value=108, format="%d")
staked_xdc_per_standby = st.sidebar.number_input("Staked XDC per Standby Masternode",value=10000000, format="%d")
staked_xdc_per_validator = st.sidebar.number_input("Staked XDC per Validator Masternode",value=10000000, format="%d")
reward_rate_validator = st.sidebar.number_input("Annual Reward Rate for Validator Masternodes (%)", value=10.0, format="%f")
reward_rate_standby = st.sidebar.number_input("Annual Reward Rate for Standby Masternodes (%)", value=8.0, format="%f")

include_tx_fee_in_reward = st.sidebar.checkbox("Include Annual TX Fee in Validator Reward")

enable_custom_annual_tip = st.sidebar.checkbox("Enable Custom Annual Tip")
custom_annual_tip = st.sidebar.number_input("Custom Annual Tip (XDC)", min_value=0.0, format="%f") if enable_custom_annual_tip else 0



# Calculations
daily_tx_fee =  avg_tx_fee*daily_txs
annual_tx_fee = daily_tx_fee * 365
annual_reward_validator = staked_xdc_per_validator * reward_rate_validator * 0.01
annual_reward_standby = staked_xdc_per_standby * reward_rate_standby * 0.01

if include_tx_fee_in_reward:
    annual_reward_validator += annual_tx_fee

if enable_custom_annual_tip:
    annual_reward_validator += custom_annual_tip  # Adding custom tip directly to validator reward

total_annual_reward_validator = annual_reward_validator * num_validator_nodes
total_annual_reward_standby = annual_reward_standby * num_standby_nodes
annual_network_emission = total_annual_reward_validator + total_annual_reward_standby
annual_network_inflation_rate = (annual_network_emission / total_xdc_supply) * 100



# Displaying results in a table
df = pd.DataFrame({
    "Metric": [
        "Daily Transaction Fee (XDC)",
        "Annual Transaction Fee (XDC)",
        "Annual Reward per Validator Node (XDC)",
        "Annual Reward per Standby Node (XDC)",
        "Total Annual Reward for Validators (XDC)",
        "Total Annual Reward for Standbys (XDC)",
        "Annual Network Emission (XDC)",
        "Annual Network Inflation Rate (%)"
    ],
    "Value": [
        f"{daily_tx_fee:.2f}",
        f"{annual_tx_fee:.2f}",
        f"{annual_reward_validator:.2f}",
        f"{annual_reward_standby:.2f}",
        f"{total_annual_reward_validator:.2f}",
        f"{total_annual_reward_standby:.2f}",
        f"{annual_network_emission:.2f}",
        f"{annual_network_inflation_rate:.2f}"
    ],
    "Formula": [

        "avg_tx_fee x daily_txs",
        "daily_tx_fee x 365",
        f"staked_xdc_per_validator x reward_rate_validator {'+ annual_tx_fee' if include_tx_fee_in_reward else ''} {'+ custom_annual_tip' if enable_custom_annual_tip else ''}",
        "staked_xdc_per_standby x reward_rate_standby",
        "annual_reward_validator x num_validator_nodes",
        "annual_reward_standby x num_standby_nodes",
        "total_annual_reward_validator + total_annual_reward_standby",
        "(annual_network_emission / total_xdc_supply) x 100"
    ]

})

st.table(df)
