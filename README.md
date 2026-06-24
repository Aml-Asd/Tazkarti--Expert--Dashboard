# 🚌 Egypt Transport AI — Simulation & Prediction Dashboard

A Discrete Event Simulation (DES) system combined with an ML delay-prediction pipeline, modelling high-traffic public transport across 4 Upper Egypt road routes. Helps administrators find the optimal number of servers/buses to minimise waiting times and user abandonment.

---

## 🗺️ Routes Covered

| Route | Location | Base Headway |
|---|---|---|
| Route 1 | Western Desert Road (Edfu) | 120 min |
| Route 2 | Qena–Luxor Agricultural Road | 300 min |
| Route 3 | Aswan Eastern Road | 60 min |
| Route 4 | Marsa Alam Coastal Road | 540 min |

---

## ✨ Features

- **DES Engine** — SimPy-based Poisson arrival modelling to simulate realistic traffic load
- **ML Delay Predictor** — scikit-learn pipeline trained on 300 real route records, serialised with joblib
- **Dual-Portal Streamlit Dashboard:**
  - 👤 **Commuter Portal** — compare live delay status across all 4 routes, get the fastest recommendation, view route map
  - 🏢 **Ops Command Centre** — KPI metrics, What-If headway simulation, projected delay reduction bar charts
- **SLA Validation** — automatically checks if a configuration meets wait-time and abandonment thresholds
- **AWS Cost Modelling** — estimates hourly infrastructure cost per configuration

---

## 🛠️ Tech Stack

Python · SimPy · scikit-learn · joblib · Streamlit · pandas · matplotlib · seaborn · Queuing Theory

---

## ⚙️ Setup

```bash
git clone https://github.com/Aml-Asd/Tazkarti--Expert--Dashboard
cd Tazkarti--Expert--Dashboard

pip install -r requirements.txt

# Place final_transport_model.pkl and Cleaned_Data_300_Rows.csv in the project root
streamlit run main.py
```

---

## 📊 ML Pipeline

```
Input features: hour, passenger_count, weather_severity, pressure_index, delay_range
      ↓
scikit-learn Pipeline (preprocessing + regressor)
      ↓
Predicted delay (minutes) per route
      ↓
Status: 🟢 Smooth (<15 min) | 🟡 Moderate (<45 min) | 🔴 Severe (≥45 min)
```

---

## 👩‍💻 Author

**Aml Abdelrhman Ahmed Mohamed**  
B.Sc. Computer Science — AASTMT Aswan (GPA: 3.67/4.0 — Excellence)

