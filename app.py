
import streamlit as st
import pandas as pd

st.set_page_config(page_title="GDP Growth Model v4.4.3", layout="wide")

st.title("📈 GDP Growth Model v4.4.3 – Employment-Adjusted")

st.markdown("""
Use the sliders below to adjust the weights of key economic indicators and see how the GDP forecast changes for Q2 2025.
""")

# Default indicator data
data = {
    "Indicator": [
        "Manufacturing PMI", "Consumer Spending", "Retail Sales YoY", "Corporate Profit Growth",
        "New Home Sales", "Durable Goods Orders", "10-Year Treasury Yield Spread",
        "Nonfarm Payrolls", "Job Openings (JOLTS)", "Consumer Confidence Index",
        "Small Business Optimism", "Credit Card Delinquencies"
    ],
    "Default Weight": [0.14, 0.13, 0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.03, 0.02],
    "Predictive Score": [0.92, 0.89, 0.87, 0.84, 0.82, 0.79, 0.76, 0.63, 0.61, 0.58, 0.56, 0.41]
}

df = pd.DataFrame(data)
df["Adjusted Weight"] = 0.0

total_weight = 0.0
st.sidebar.header("🔧 Adjust Indicator Weights")

# Create sliders for each indicator
for i, row in df.iterrows():
    new_weight = st.sidebar.slider(
        label=f"{row['Indicator']}",
        min_value=0.00,
        max_value=0.20,
        value=float(row['Default Weight']),
        step=0.01
    )
    df.at[i, "Adjusted Weight"] = new_weight
    total_weight += new_weight

# Normalize weights if needed
if total_weight > 0:
    df["Normalized Weight"] = df["Adjusted Weight"] / total_weight
else:
    df["Normalized Weight"] = 0

# Forecast calculation: Weighted average of predictive scores
forecast = (df["Normalized Weight"] * df["Predictive Score"]).sum() * 3  # Scaling factor to map to GDP range
baseline_forecast = 2.04

# Display forecast
st.metric(label="📊 Adjusted Q2 2025 GDP Forecast", value=f"{forecast:.2f}%", delta=f"{forecast - baseline_forecast:+.2f}% vs Original")

# Show data table
st.subheader("🔍 Indicator Breakdown")
st.dataframe(df[["Indicator", "Predictive Score", "Adjusted Weight", "Normalized Weight"]])

st.caption("Model scaled to fit historical GDP range. For demo use only.")
