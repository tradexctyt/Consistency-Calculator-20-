import streamlit as st

# Example values
total_profit = 6000
biggest_day = 2000
max_allowed = total_profit * 0.2

# Display results
st.write(f"📊 **Total Profit:** ${total_profit:,.2f}")
st.write(f"📈 **Biggest Day Profit:** ${biggest_day:,.2f}")
st.write(f"✅ **Max Allowed (20%):** ${max_allowed:,.2f}")

if biggest_day <= max_allowed:
    st.success("✅ Consistent — Eligible to Withdraw")
else:
    required_total = biggest_day / 0.20
    needed = required_total - total_profit
    st.error("❌ Not Consistent — Keep Trading")
    if needed > 0:
        st.info(f"💡 To meet the rule, you need at least **${needed:,.2f}** more profit in future trades.")
