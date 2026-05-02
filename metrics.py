# metrics.py
import config

class MetricsCalculator:
    @staticmethod
    def calculate(shared_data, num_servers, sim_time_sec, logs_df=None):
        """
        Calculates KPIs using shared_data counters for O(1) performance.
        """
        # 1. Throughput: Served users per minute
        throughput = shared_data['served'] / (sim_time_sec / 60)
        
        # 2. Revenue: 5% conversion of served users
        actual_revenue = (shared_data['served'] * config.CONVERSION_RATE) * config.TICKET_PRICE
        
        # 3. Utilization: Clamped at 1.0
        total_capacity_sec = num_servers * sim_time_sec
        raw_util = shared_data['total_busy_time'] / total_capacity_sec if total_capacity_sec > 0 else 0
        utilization = min(float(raw_util), 1.0) 

        # 4. Abandon & Wait
        total_arrivals = shared_data['arrivals']
        abandon_rate = shared_data['abandoned'] / total_arrivals if total_arrivals > 0 else 0
        
        # Avg Wait (Total sum / served count) - Output in Seconds
        avg_wait_sec = (shared_data['total_wait_time'] / shared_data['served']) if shared_data['served'] > 0 else 0

        # --- QUALITATIVE LABELS FOR PROFESSOR ---
        wait_label = "🔴 High" if avg_wait_sec > 20 else ("🟡 Medium" if avg_wait_sec > 5 else "🟢 Low")
        abandon_label = "🔴 High" if abandon_rate > 0.30 else ("🟡 Medium" if abandon_rate > 0.15 else "🟢 Low")
        
        # SLA Check
        passed_sla = (avg_wait_sec <= config.MAX_WAIT_TIME_THRESHOLD_SEC and 
                      abandon_rate <= config.MAX_ABANDON_RATE_THRESHOLD)

        return {
            "avg_wait": round(float(avg_wait_sec), 2),
            "wait_label": wait_label,
            "abandon_rate": round(float(abandon_rate), 4),
            "abandon_label": abandon_label,
            "utilization": round(float(utilization), 4),
            "throughput": round(throughput, 2),
            "actual_revenue": round(actual_revenue, 2),
            "passed_sla": "✅ Pass" if passed_sla else "❌ Fail"
        }

    @staticmethod
    def get_theoretical_minimum(arrival_rate_min, user_dist, service_times):
        avg_times_sec = {u: (v[0] + v[1]) / 2 for u, v in service_times.items()}
        weighted_mu_sec = sum(avg_times_sec[u] for u in user_dist) / len(user_dist)
        lambda_sec = arrival_rate_min / 60.0
        return int(lambda_sec * weighted_mu_sec) + 1