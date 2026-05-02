import pandas as pd

class SimulationLogger:
    def __init__(self):
        self.events = []
        self.queue_data = []

    def log(self, user_id, event, time, wait_time=0, user_type=""):
        self.events.append({
            "user_id": user_id, "event": event, "time": round(time, 2),
            "wait_time": round(wait_time, 2), "user_type": user_type
        })

    def log_queue(self, time, length):
        self.queue_data.append({"time": round(time, 2), "queue_length": length})

    def get_dataframe(self):
        return pd.DataFrame(self.events)

    def get_queue_dataframe(self):
        # Returns the queue length over time for the Streamlit chart
        return pd.DataFrame(self.queue_data)