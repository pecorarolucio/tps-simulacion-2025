import random
import matplotlib.pyplot as plt

INF = 1.0e30
max_time = 360

mean_interdemand = 0.8
s = 2   # Cantidad en la que se realiza pedido
S = 20  # Capacidad del inventario

setup_cost = 2      # k
shortage_cost = 40  # p
holding_cost = 2    # h
unit_cost = 1       # i

inv_level = 10
sim_time = 0.0
amount = 0  # Cantidad a pedir (Z)

shortages_costs: list[float] = [0]  # I-
holding_costs: list[float] = [0]    # I+
unit_costs: list[float] = [0]       # iZ
total_costs: list[float] = [0]      # C

avg_holding_costs: list[float] = [0]    # I+
avg_shortage_costs: list[float] = [0]
avg_unit_costs: list[float] = [0]
avg_total_costs: list[float] = [0]

I_plus: list[float] = [max(inv_level, 0)]
I_minus: list[float] = [max(-inv_level, 0)]
inv_levels = [inv_level]
times = [0.0]
costs_times = [0.0]

time_next_event: dict[str, float] = {
    "demand": random.expovariate(mean_interdemand),
    "order_arrival": INF,
    "evaluation": 1
}

def reset_simulation():
    global sim_time, costs_times, amount, shortages_costs, holding_costs, unit_costs, total_costs, I_plus, I_minus, inv_levels, times, time_next_event
    inv_level = 10
    sim_time = 0.0
    amount = 0  # Cantidad a pedir (Z)

    shortages_costs = [0]  # I-
    holding_costs = [0]    # I+
    unit_costs = [0]       # iZ
    total_costs = [0]      # C

    I_plus = [max(inv_level, 0)]
    I_minus = [max(-inv_level, 0)]
    inv_levels = [inv_level]
    times = [0.0]
    costs_times = [0.0]

    time_next_event = {
        "demand": random.expovariate(mean_interdemand),
        "order_arrival": INF,
        "evaluation": 1
    }

def random_empiric():
    r = random.random()

    if r < 1/6:
        return 1
    elif r < 1/2:  # 1/6 + 1/3 = 1/2
        return 2
    elif r < 5/6:  # 1/2 + 1/3 = 5/6
        return 3
    else:
        return 4


def demand():
    global inv_level

    inv_level -= random_empiric()
    time_next_event["demand"] = sim_time + random.expovariate(mean_interdemand)


def order_arrival():
    global inv_level

    inv_level += amount
    time_next_event["order_arrival"] = INF


def evaluation():
    global amount

    if inv_level < s:
        amount = S - inv_level
        # total_ordering_cost += setup_cost + incremental_cost * amount;
        time_next_event["order_arrival"] = sim_time + random.uniform(0.5, 1)
    time_next_event["evaluation"] += 1.0


def update_graph_values():
    i_plus = max(inv_level, 0)+0.1
    i_minus = max(-inv_level, 0)+0.1

    I_plus.append(i_plus)
    I_minus.append(i_minus)
    inv_levels.append(inv_level)
    times.append(sim_time)


def get_next_event_type() -> str:
    min = INF
    event = ""
    for k in time_next_event:
        if time_next_event[k] < min:
            min = time_next_event[k]
            event = k

    return event


def update_prom_values():
    unit_costs.append(amount * unit_cost)
    i_plus  = max(inv_level, 0)
    i_minus = max(-inv_level, 0)

    holding_costs.append(i_plus * holding_cost)
    shortages_costs.append(i_minus * shortage_cost)
    total_costs.append(amount * unit_cost + i_plus * holding_cost + i_minus * shortage_cost)
    costs_times.append(sim_time)

    # Average costs
    avg_holding_costs.append(sum(holding_costs) / len(holding_costs))
    avg_shortage_costs.append(sum(shortages_costs) / len(shortages_costs))
    avg_unit_costs.append(sum(unit_costs) / len(unit_costs))
    avg_total_costs.append(sum(total_costs) / len(total_costs))


def graph_inventory(file_name=None):
    plt.plot(times, inv_levels, marker=',', label='Inv. level')
    plt.plot([i+0.1 for i in times], I_plus, linestyle=':', marker=',', color='r', label='I+')
    plt.plot([i+0.1 for i in times], I_minus, marker=',', color='g', label='I-')

    plt.title('Inventario vs Tiempo')
    plt.xlabel('Tiempo (Meses)')
    plt.ylabel('Inventario')
    plt.grid(True)
    plt.legend()
    if file_name:
        plt.savefig(f"results/{file_name}", format="png")
    else:
        plt.show()

def graph_costs(file_name=None):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    axs[0, 0].plot(costs_times, total_costs, color='b', linestyle='--')
    axs[0, 0].plot(costs_times, avg_total_costs, color='r', linestyle='-', label='Average')
    axs[0, 0].set_title(f'Avg. Total cost = {calc_prom(total_costs, sim_time):.2f}')
    axs[0, 0].set_ylabel('Total Cost')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    axs[0, 1].plot(costs_times, holding_costs, color='r', linestyle='--', label='Holding cost')
    axs[0, 1].plot(costs_times, avg_holding_costs, color='b', linestyle='-', label='Average')
    axs[0, 1].set_title(f'Avg. Holding cost = {calc_prom(holding_costs, sim_time):.2f}')
    axs[0, 1].set_ylabel('Holding Cost')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    axs[1, 0].plot(costs_times, shortages_costs, color='g', linestyle='--')
    axs[1, 0].plot(costs_times, avg_shortage_costs, color='b', linestyle='-', label='Average')
    axs[1, 0].set_title(f'Avg. Shortage cost = {sum(shortages_costs)/len(shortages_costs):.2f}')
    axs[1, 0].set_ylabel('Shortage Cost')
    axs[1, 0].set_xlabel('Tiempo (Meses)')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    axs[1, 1].plot(costs_times, unit_costs, color='orange', linestyle='--')
    axs[1, 1].plot(costs_times, avg_unit_costs, color='b', linestyle='-', label='Average')
    axs[1, 1].set_title(f'Avg. Unit cost = {sum(unit_costs)/len(unit_costs):.2f}')
    axs[1, 1].set_ylabel('Unit Cost')
    axs[1, 1].set_xlabel('Tiempo (Meses)')
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    fig.suptitle('Costos vs Tiempo', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    if file_name:
        plt.savefig(f"results/{file_name}", format="png")
    else:
        plt.show()


def calc_prom(values: list[float], n: float):
    prev = values[0]
    sum = 0.0
    for level in values:
        if level != prev:
            sum += level
            prev = level

    return sum / int(n)

def main():
    global sim_time

    while sim_time < max_time:
        next_event = get_next_event_type()

        update_prom_values()
        if next_event == "demand":
            sim_time = time_next_event["demand"]
            update_graph_values()
            demand()
        elif next_event == "order_arrival":
            sim_time = time_next_event["order_arrival"]
            update_graph_values()
            order_arrival()
        elif next_event == "evaluation":
            sim_time = time_next_event["evaluation"]
            evaluation()
        update_graph_values()

if __name__ == "__main__":
    save_fig = True
    max_simulations = 1
    for i in range(max_simulations): 
        main()
        #file_name = f"{i}_s{s}_S{S}_lambda{mean_interdemand}_inventory.png" 
        #graph_inventory()
        graph_costs()
        plt.clf()
        reset_simulation()