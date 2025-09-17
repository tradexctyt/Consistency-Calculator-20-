import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consistency Calculator By TradeX", page_icon="🃏", layout="centered")

st.title(" 🃏 Consistency Calculator")
st.write(
    "Enter your daily profits and choose timeframe, consistency % and account sizes. The app now supports 20%, 40% and 50% consistency checks and shows recommended daily targets for common account sizes."
)

# Session state for profits
if "profits" not in st.session_state:
    st.session_state.profits = [0.0]

# Controls
col1, col2 = st.columns([2,1])
with col1:
    timeframe = st.radio("📅 Timeframe", ("Weekly (5 days)", "Biweekly (14 days)", "Monthly (30 days)"), horizontal=True)
with col2:
    consistency_pct = st.selectbox("🎯 Consistency %", (20, 40, 50))

# Account sizes for scenario table
st.subheader("🏷️ Account sizes for scenario calculations")
accounts = st.multiselect("Pick account sizes to display", [10000, 25000, 50000, 100000, 200000], default=[10000,25000,100000,200000])

# Add / input daily profits
st.subheader("➕ Enter Daily Profits")
if st.button("➕ Add Another Day"):
    st.session_state.profits.append(0.0)

for i in range(len(st.session_state.profits)):
    st.session_state.profits[i] = st.number_input(f"Day {i+1} Profit ($)", value=float(st.session_state.profits[i]), step=50.0)

# Determine period length
if "Weekly" in timeframe:
    period_length = 5
elif "Biweekly" in timeframe:
    period_length = 14
else:
    period_length = 30

profits = st.session_state.profits[:period_length]

# Calculations for current window
total_profit = sum(profits)
biggest_day = max(profits) if profits else 0.0
max_allowed = total_profit * (consistency_pct/100.0)
consistent = biggest_day <= max_allowed

st.subheader("📈 Results for chosen window")
st.write(f"**Timeframe:** {timeframe} — considering first {period_length} day(s) of inputs")
st.write(f"**Consistency target:** {consistency_pct}%")
st.metric("Total Profit ($)", f"{total_profit:,.2f}")
st.metric("Biggest Day ($)", f"{biggest_day:,.2f}")
st.metric(f"Max Allowed ({consistency_pct}%) ($)", f"{max_allowed:,.2f}")

if consistent:
    st.success("✅ Consistent — Eligible to Withdraw")
else:
    st.error("❌ Not Consistent — Keep Trading")
    # recommendation to reach consistency within this window
    if total_profit > 0 and biggest_day > 0:
        required_total = biggest_day / (consistency_pct/100.0)
        needed_more = max(0.0, required_total - total_profit)
        st.info(f"💡 To meet the {consistency_pct}% rule in this window you need **${needed_more:,.2f}** more profit.")

# Show a progress bar toward consistency
progress = 0.0
if biggest_day > 0 and max_allowed > 0:
    progress = min(1.0, max_allowed / biggest_day)
st.write("\n")
st.progress(progress)
if not consistent and biggest_day>0:
    st.write(f"Progress toward making biggest day acceptable: {progress*100:.1f}% (1.0 = OK)")

# Scenario table for selected account sizes
st.subheader("🧾 Scenario table — daily targets and max single-day allowed")

# Define daily target tiers (conservative, moderate, aggressive) as % of account
tiers = {
    "Conservative": 0.2/100,    # 0.2%
    "Moderate": 0.4/100,        # 0.4%
    "Aggressive": 1.0/100       # 1.0%
}

rows = []
for acc in accounts:
    for name, pct in tiers.items():
        daily = acc * pct
        total_period = daily * period_length
        max_single_allowed = total_period * (consistency_pct/100.0)
        rows.append({
            "Account ($)": acc,
            "Tier": name,
            "Daily Target ($)": round(daily,2),
            f"Total ({period_length}d) ($)": round(total_period,2),
            f"Max Single Allowed ({consistency_pct}%) ($)": round(max_single_allowed,2)
        })

if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df)

st.write("---")
st.caption("Notes:\n• If your trading week has only 4 active days, use a 5-day weekly window or biweekly/monthly for consistency checks.\n• The app calculates how much more profit you need to make the largest day fall inside the chosen consistency % for the selected timeframe.")

# Reset button
if st.button("🔄 Reset All Data"):
    st.session_state.profits = [0.0]
    st.experimental_rerun()
