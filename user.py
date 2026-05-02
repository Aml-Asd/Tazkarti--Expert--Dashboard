# user.py
import random

def user_process(env, user_id, user_type, system, logger, config, shared_data, silent=False):
    arrival_time = env.now
    shared_data['arrivals'] += 1
    
    # EXTREME SAMPLING: Log only 1 in every 1000 users for the chart
    # This keeps the browser from lagging.
    should_log = (not silent) and (random.random() < 0.001)
    if should_log: logger.log(user_id, "arrival", arrival_time, user_type=user_type)

    patience = random.expovariate(1.0 / config.AVG_PATIENCE)

    with system.servers.request() as request:
        results = yield request | env.timeout(patience)
        wait_time = env.now - arrival_time

        if request in results:
            # TRACK WAIT TIME IN REAL-TIME
            shared_data['total_wait_time'] += wait_time
            
            if should_log: logger.log(user_id, "start_service", env.now, wait_time, user_type)
            
            duration = random.uniform(config.SERVICE_TIME[user_type][0], config.SERVICE_TIME[user_type][1])
            
            # TRACK BUSY TIME FOR UTILIZATION
            time_remaining = config.SIM_TIME_SEC - env.now
            shared_data['total_busy_time'] += max(0, min(duration, time_remaining))
            
            yield env.timeout(duration)
            
            if env.now <= config.SIM_TIME_SEC:
                shared_data['served'] += 1
                if should_log: logger.log(user_id, "finish", env.now, wait_time, user_type)
        else:
            shared_data['abandoned'] += 1
            if should_log: logger.log(user_id, "abandon", env.now, wait_time, user_type)