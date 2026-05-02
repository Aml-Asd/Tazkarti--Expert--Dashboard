import simpy

class TicketSystem:
    def __init__(self, env, num_servers):
        self.env = env
        # Pure M/G/c model: Capacity directly equals number of servers
        self.servers = simpy.Resource(env, capacity=num_servers)