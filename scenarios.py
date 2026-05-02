import config

def get_scenario_params(match_type):
    return {
        "arrival_rate": config.MATCH_TYPES[match_type],
        "user_distribution": config.USER_TYPE_DISTRIBUTION[match_type]
    }