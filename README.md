# 🎟️ High-Demand Ticket Booking Simulation

A Discrete Event Simulation (DES) system built with **SimPy** to model high-traffic ticket booking scenarios (like Tazkarti). It helps administrators determine the optimal number of servers needed to balance cost, waiting times, and user abandonment.

## 🚀 Features
- **Smart Engine:** Uses Queuing Theory to simulate Poisson arrivals.
- **Admin Dashboard:** Built with Streamlit for real-time "What-If" analysis.
- **SLA Validation:** Automatically checks if the configuration meets wait time and abandonment thresholds.
- **AWS Cost Modeling:** Estimates hourly infrastructure costs.

## 🛠️ Installation

1. **Clone or download** this folder.
2. Open your terminal/command prompt in the project directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt