
# simulation.py
import simpy, random, pandas as pd, config
from system import TicketSystem
from user import user_process
from logger import SimulationLogger
from metrics import MetricsCalculator
from scenarios import get_scenario_params

def arrival_generator(env, system, params, logger, shared_data, override_min=None, silent=False):
    user_id = 0
    base_rate_min = override_min if override_min else params['arrival_rate']
    while True:
        multiplier = config.SPIKE_MULTIPLIER if config.SPIKE_START_SEC <= env.now <= config.SPIKE_END_SEC else 1.0
        rate_sec = (base_rate_min * multiplier) / 60.0
        yield env.timeout(random.expovariate(rate_sec))
        user_id += 1
        # Log queue every 100 users only if not silent
        if not silent and user_id % 100 == 0: 
            logger.log_queue(env.now, len(system.servers.queue))
        env.process(user_process(env, user_id, random.choice(params['user_distribution']), 
                                 system, logger, config, shared_data, silent))

def run_engine(match_type, num_servers, arrival_override=None, silent=False):
    random.seed(config.RANDOM_SEED)
    env = simpy.Environment()
    system = TicketSystem(env, num_servers)
    logger = SimulationLogger()
    shared_data = {
        'arrivals': 0, 'served': 0, 'abandoned': 0, 
        'total_busy_time': 0, 'total_wait_time': 0
    }
    params = get_scenario_params(match_type)
    env.process(arrival_generator(env, system, params, logger, shared_data, arrival_override, silent))
    env.run(until=config.SIM_TIME_SEC)
    
    # We pass logs_df as the 4th argument (empty DF if silent)
    logs_df = logger.get_dataframe() if not silent else pd.DataFrame()
    metrics = MetricsCalculator.calculate(shared_data, num_servers, config.SIM_TIME_SEC, logs_df)
    
    if silent:
        return metrics, None, None
    return metrics, logs_df, logger.get_queue_dataframe()

def run_comparison(match_type, arrival_rate, optimal_n):
    res = []
    # Test fail points, optimal point, and over-provisioned point
    cases = sorted(list(set([5, 10, 15, optimal_n, 25, 40])))
    for c in cases:
        # Pass silent=True for speed
        m, _, _ = run_engine(match_type, c, arrival_rate, silent=True)
        res.append({
            "Servers": c, 
            "Wait Time": m['wait_label'],
            "Abandon": m['abandon_label'],
            "Throughput": m['throughput'],
            "Utilization": f"{m['utilization']*100:.1f}%",
            "SLA": m['passed_sla'],
            "AbandonRate": m['abandon_rate'] * 100 # For chart logic
        })
    return pd.DataFrame(res)