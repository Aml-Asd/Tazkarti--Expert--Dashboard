# config.py - Realistic Queueing Theory Parameters

SIM_TIME_SEC = 3600  
RANDOM_SEED = 42

# --- SERVER REALISM (The Big Fix) ---
# We removed the fake "concurrency" multiplier. 
# 1 Server = 1 processing thread/node.
COST_PER_SERVER = 0.50

# --- SERVICE TIME (Seconds) ---
# Realistic web-request processing times (0.2 to 1.5 seconds)
SERVICE_TIME = {
    "new": (0.6, 1.5),      # Registration takes ~1 sec
    "existing": (0.2, 0.6), # Login/Book takes ~0.4 sec
    "full": (0.8, 2.0)      # Payment takes ~1.4 sec
}

# --- BUSINESS LOGIC ---
TICKET_PRICE = 20.0 
CONVERSION_RATE = 0.05  # 5% conversion -> Realistic Revenue

# --- USER BEHAVIOR ---
# Users refresh/leave if the website hangs for more than 30 seconds
AVG_PATIENCE = 30 

# --- TRAFFIC SPIKE ---
SPIKE_START_SEC = 1200 
SPIKE_END_SEC = 2400   
SPIKE_MULTIPLIER = 1.5  # Realistic 1.5x surge

MATCH_TYPES = {"low": 100, "medium": 1000, "high": 5000}
USER_TYPE_DISTRIBUTION = {
    "low": ["existing", "existing", "new"],
    "medium":["existing", "new", "full"],
    "high": ["full", "full", "existing"]
}

# --- SLA THRESHOLDS ---
MAX_WAIT_TIME_THRESHOLD_SEC = 5.0
MAX_ABANDON_RATE_THRESHOLD = 0.05