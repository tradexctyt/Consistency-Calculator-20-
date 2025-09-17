import streamlit as st

st.set_page_config(page_title="20% Consistency Calculator", page_icon="📊", layout="centered")

st.title("📊 20% Consistency Calculator")
st.write(
    "Check if your trading profits meet the **20% consistency rule**.\n\n"
    "Enter your daily profits below. The calculator will tell you if you're "
    "eligible to withdraw and how much more profit you need if you're not consistent yet."
)

# Store daily profits in session state
if "profits" not in st.session_state:
    st.session_state.profits = [0.0]

# Function to add a new day
def add_day():
    st.session_state.profits.append(0.0)

# Input fields for daily profits
st.subheader("➕ Enter Daily Profits")
for i in range(len(st.session_state.profits)):
    st.session_state.profits[i] = st.number_input(
        f"Day {i+1} Profit ($)", value=float(st.session_state.profits[i]), step=100.0
    )

st.button("Add Another Day", on_click=add_day)

# Calculations
total_profit = sum(st.session_state.profits)
biggest_day = max(st.session_state.profits) if st.session_state.profits else 0
max_allowed = total_profit * 0.20
consistent = biggest_day <= max_allowed

# Display results
st.subheader("📈 Results")
st.write(f"📊 **Total Profit:** ${total_profit:,.2f}")
st.write(f"📈 **Biggest Day Profit:** ${biggest_day:,.2f}")
st.write(f"✅ **Max Allowed (20%):** ${max_allowed:,.2f}")

if consistent:
    st.success("✅ Consistent — Eligible to Withdraw")
else:
    st.error("❌ Not Consistent — Keep Trading")

    # Recommendation for next trade
    if total_profit > 0:
        required_total = biggest_day / 0.20
        needed = required_total - total_profit
        if needed > 0:
            st.info(f"💡 To meet the rule, you need at least **${needed:,.2f}** more profit in future trades.")
