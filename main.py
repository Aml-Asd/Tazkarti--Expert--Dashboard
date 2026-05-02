import config
from simulation import run_simulation
from metrics import MetricsCalculator
from scenarios import get_scenario_params

def run_smart_analysis(match_type):
    params = get_scenario_params(match_type)
    
    theo_min = MetricsCalculator.get_theoretical_minimum(
        params['arrival_rate'], params['user_distribution'], config.SERVICE_TIME
    )

    print(f"\n" + "="*80)
    print(f"STRESS TEST: {match_type.upper()} DEMAND ({params['arrival_rate']} users/min)")
    print("="*80)
    print(f"{'Servers':<8} | {'Wait':<6} | {'Abandon%':<10} | {'Util%':<8} | {'Hourly Cost':<12} | {'Status'}")
    print("-" * 80)

    # Automatically generating range to test
    test_range = [int(theo_min * m) for m in [0.5, 0.8, 1.0, 1.1, 1.3, 1.5]]
    simulation_results = []

    for count in sorted(list(set(test_range))):
        if count < 1: continue
        
        logs_df = run_simulation(count, match_type)
        res = MetricsCalculator.calculate(logs_df, count, config.SIM_TIME)
        
        passed = (res['avg_wait'] <= config.MAX_WAIT_TIME_THRESHOLD and 
                  res['abandon_rate'] <= config.MAX_ABANDON_RATE_THRESHOLD)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        hourly_cost = count * config.COST_PER_SERVER
        
        res.update({'num_servers': count, 'hourly_cost': hourly_cost, 'passed': passed})
        simulation_results.append(res)

        print(f"{count:<8} | {res['avg_wait']:<6} | {res['abandon_rate']*100:<9.2f}% | "
              f"{res['utilization']*100:<7.1f}% | ${hourly_cost:<11.2f} | {status}")

    print("-" * 80)
    passing = [r for r in simulation_results if r['passed']]
    if passing:
        optimal = min(passing, key=lambda x: x['num_servers'])
        print(f"FINAL DATA-DRIVEN RECOMMENDATION")
        print(f"Optimal Servers:    {optimal['num_servers']}")
        print(f"Avg Wait Time:      {optimal['avg_wait']} min")
        print(f"Server Utilization: {optimal['utilization']*100:.1f}%")
        print(f"Hourly Budget:      ${optimal['hourly_cost']:.2f}")
    else:
        print("❌ CRITICAL: No tested configuration met the SLA.")

if __name__ == "__main__":
    run_smart_analysis("high")