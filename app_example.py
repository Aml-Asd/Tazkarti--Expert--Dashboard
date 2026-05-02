import streamlit as st
import config
import pandas as pd
from simulation import run_engine, run_comparison
from metrics import MetricsCalculator

st.set_page_config(page_title="Tazkarti Expert Dashboard", layout="wide")
st.title("🎟️ High-Demand Infrastructure Planner")

# Sidebar
st.sidebar.header("🛠️ Scenario Settings")
match_type = st.selectbox("Scenario", ["low", "medium", "high"], index=1)
arrival_rate = st.sidebar.number_input("Base Arrival Rate (Users/Min)", value=config.MATCH_TYPES[match_type])

if st.sidebar.button("🧹 Clear Cache"): st.cache_data.clear()

# Calculate math recommendation
theo_min = MetricsCalculator.get_theoretical_minimum(arrival_rate, config.USER_TYPE_DISTRIBUTION[match_type], config.SERVICE_TIME)
st.sidebar.info(f"💡 **Planning Hint:** Math suggests you need at least **{theo_min}** servers.")

servers = st.slider("Provisioned AWS Instances", 1, 60, int(theo_min))

# FIX: Added 'opt_n' to the cache function signature
@st.cache_data
def get_cached_comparison(m_type, a_rate, opt_n): 
    return run_comparison(m_type, a_rate, opt_n)

if st.button("🚀 Execute Full System Stress Test"):
    with st.spinner("Simulating Traffic Spike & Peak Demand..."):
        metrics, logs_df, queue_df = run_engine(match_type, servers, arrival_rate)
    
    # 1. PRIMARY METRICS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Wait", f"{metrics['avg_wait']}s", help=metrics['wait_label'])
    c2.metric("Abandon Rate", f"{metrics['abandon_rate']*100:.2f}%", help=metrics['abandon_label'])
    c3.metric("System Throughput", f"{metrics['throughput']} users/min")
    c4.metric("Hourly Revenue", f"${metrics['actual_revenue']:,.0f}")

    if "Pass" in metrics['passed_sla']: st.success(f"✅ SLA STATUS: Pass")
    else: st.error(f"❌ SLA STATUS: Fail")

    # 2. EFFICIENCY HINT (IDLE SERVERS)
    idle_servers = round(servers * (1 - metrics['utilization']))
    if metrics['utilization'] < 0.6:
        st.warning(f"💡 **Efficiency Hint:** System is over-provisioned. **{idle_servers}** servers are idle. Reduce instances to save costs.")
    elif metrics['utilization'] > 0.95:
        st.error(f"⚠️ **Efficiency Hint:** Critical Load! Only **{idle_servers}** servers idle. System may crash if traffic increases.")
    else:
        st.info(f"✨ **Efficiency Hint:** Healthy Load. **{idle_servers}** servers available as a safety buffer.")

    # 3. GRAPHS
    st.divider()
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("📉 Queue Depth (FIFO Discipline)")
        st.line_chart(queue_df.set_index('time'))
        st.caption("Visualizing the virtual waiting room surge during the spike.")
    
    with col_r:
        st.subheader("📊 Scalability Analysis")
        # FIX: Now passing all 3 required arguments
        comp_df = get_cached_comparison(match_type, arrival_rate, theo_min)
        st.line_chart(comp_df.set_index("Servers")["AbandonRate"])

    # 4. PROFESSOR'S EXPERIMENTAL TABLE
    st.subheader("📋 Experimental Results: Server Sensitivity Table")
    st.table(comp_df[['Servers', 'Wait Time', 'Abandon', 'Throughput', 'Utilization', 'SLA']])

    with st.expander("📝 Technical Assumptions & RNG Algorithm"):
        st.write(f"""
        - **Model:** M/G/c/K Queueing system.
        - **RNG:** Mersenne Twister (MT19937) via fixed seed 42.
        - **Spike:** {config.SPIKE_MULTIPLIER}x traffic multiplier active (20-40 min).
        - **Discipline:** Strict First-In-First-Out (FIFO) queueing.
        """)