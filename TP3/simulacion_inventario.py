import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class InventorySimulation:
    def __init__(self, demand_rate, lead_time, order_cost, holding_cost, shortage_cost,
                 review_period, order_quantity, initial_inventory=100, max_time=1000):
        self.demand_rate = demand_rate
        self.lead_time = lead_time
        self.order_cost = order_cost
        self.holding_cost = holding_cost
        self.shortage_cost = shortage_cost
        self.review_period = review_period
        self.order_quantity = order_quantity
        self.inventory = initial_inventory
        self.time = 0
        self.max_time = max_time

        # Seguimiento
        self.inventory_levels = []
        self.backorders = 0
        self.cost_order = 0
        self.cost_holding = 0
        self.cost_shortage = 0

        # Costos históricos para gráficos
        self.costs_times = []
        self.holding_costs = []
        self.shortage_costs = []
        self.order_costs = []
        self.total_costs = []

        self.next_review = 0
        self.pending_orders = []

    def simulate(self):
        dt = 1
        while self.time < self.max_time:
            self._receive_orders()

            demand = np.random.poisson(self.demand_rate * dt)
            if demand <= self.inventory:
                self.inventory -= demand
            else:
                self.backorders += demand - self.inventory
                self.inventory = 0

            if self.time >= self.next_review:
                self._place_order()
                self.next_review += self.review_period

            # Calcular costos
            holding = self.holding_cost * max(self.inventory, 0)
            shortage = self.shortage_cost * self.backorders
            order = self.order_cost if self.time % self.review_period == 0 else 0

            self.cost_holding += holding
            self.cost_shortage += shortage
            self.cost_order += order

            # Guardar valores
            self.inventory_levels.append(self.inventory)
            self.costs_times.append(self.time)
            self.holding_costs.append(holding)
            self.shortage_costs.append(shortage)
            self.order_costs.append(order)
            self.total_costs.append(holding + shortage + order)

            self.time += dt

    def _receive_orders(self):
        arrivals = [order for order in self.pending_orders if order[0] <= self.time]
        for arrival_time, qty in arrivals:
            self.inventory += qty
            if self.backorders > 0:
                if self.inventory >= self.backorders:
                    self.inventory -= self.backorders
                    self.backorders = 0
                else:
                    self.backorders -= self.inventory
                    self.inventory = 0
            self.pending_orders.remove((arrival_time, qty))

    def _place_order(self):
        arrival_time = self.time + self.lead_time
        self.pending_orders.append((arrival_time, self.order_quantity))

    def get_costs(self):
        total = self.cost_order + self.cost_holding + self.cost_shortage
        return {
            'order_cost': self.cost_order,
            'holding_cost': self.cost_holding,
            'shortage_cost': self.cost_shortage,
            'total_cost': total
        }

    def get_theoretical_costs(self):
        orders_per_unit_time = 1 / self.review_period
        expected_inventory = self.order_quantity / 2  # promedio si no hay faltantes
        expected_holding = self.holding_cost * expected_inventory
        expected_order = self.order_cost * orders_per_unit_time
        expected_shortage = 0  # se asume sin faltantes para comparación base
        total = expected_holding + expected_order + expected_shortage

        return {
            'order_cost': expected_order,
            'holding_cost': expected_holding,
            'shortage_cost': expected_shortage,
            'total_cost': total
        }

    def plot_inventory(self):
        plt.plot(self.inventory_levels)
        plt.title("Nivel de inventario a lo largo del tiempo")
        plt.xlabel("Tiempo")
        plt.ylabel("Inventario")
        plt.grid(True)
        plt.show()

    def plot_costs(self):
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        axs[0, 0].plot(self.costs_times, self.total_costs, color='b')
        axs[0, 0].set_title('Costo total')
        axs[0, 0].grid(True)

        axs[0, 1].plot(self.costs_times, self.holding_costs, color='g')
        axs[0, 1].set_title('Costo de mantenimiento')
        axs[0, 1].grid(True)

        axs[1, 0].plot(self.costs_times, self.shortage_costs, color='r')
        axs[1, 0].set_title('Costo por faltantes')
        axs[1, 0].grid(True)

        axs[1, 1].plot(self.costs_times, self.order_costs, color='orange')
        axs[1, 1].set_title('Costo de orden')
        axs[1, 1].grid(True)

        plt.tight_layout()
        plt.show()

def run_inventory_experiments(runs=10):
    demand_rate = 5
    lead_time = 2
    order_cost = 50
    holding_cost = 1
    shortage_cost = 10
    review_period = 5
    order_quantity = 30
    max_time = 200

    results = []
    for i in range(runs):
        sim = InventorySimulation(demand_rate, lead_time, order_cost, holding_cost,
                                  shortage_cost, review_period, order_quantity, max_time=max_time)
        sim.simulate()
        results.append(sim.get_costs())

    avg_costs = {key: np.mean([r[key] for r in results]) for key in results[0].keys()}
    print("Promedio de costos tras", runs, "corridas:")
    for k, v in avg_costs.items():
        print(f"{k}: {v:.2f}")

    # Comparación con teoría (usando los mismos parámetros)
    sim_teoria = InventorySimulation(demand_rate, lead_time, order_cost, holding_cost,
                                     shortage_cost, review_period, order_quantity, max_time=max_time)
    theoretical = sim_teoria.get_theoretical_costs()

    print("\nComparación con valores teóricos (esperados):")
    for k in avg_costs:
        sim_val = avg_costs[k]
        theo_val = theoretical[k]
        print(f"{k}: Simulado = {sim_val:.2f} | Teórico = {theo_val:.2f}")

    # Gráficos de la última corrida
    sim.plot_inventory()
    sim.plot_costs()

    save_inventory_results(results)
    plot_cost_comparison(avg_costs, theoretical)


def save_inventory_results(results, filename="inventory_results.csv"):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)

def plot_cost_comparison(avg_costs, theoretical):
    import matplotlib.pyplot as plt
    import numpy as np

    labels = ['Orden', 'Mantenimiento', 'Faltantes', 'Total']
    sim_values = [avg_costs[k] for k in avg_costs.keys()]
    theo_values = [theoretical[k] for k in theoretical.keys()]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(x - width/2, sim_values, width, label='Simulado', color='#1f77b4')
    bars2 = ax.bar(x + width/2, theo_values, width, label='Teórico', color='#ff7f0e')

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)

    ax.set_ylabel('Costo ($)')
    ax.set_title('Comparación de costos promedio vs teóricos')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    run_inventory_experiments()
