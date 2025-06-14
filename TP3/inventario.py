import numpy as np
import matplotlib.pyplot as plt

class InventorySimulation:
    def __init__(self, demand_rate, lead_time, order_cost, holding_cost, shortage_cost,
                 review_period, order_quantity, initial_inventory=100, max_time=1000):
        self.demand_rate = demand_rate          # demanda media por unidad de tiempo (Poisson)
        self.lead_time = lead_time              # tiempo de entrega del pedido (constante o variable)
        self.order_cost = order_cost            # costo fijo por orden
        self.holding_cost = holding_cost        # costo por unidad almacenada por unidad de tiempo
        self.shortage_cost = shortage_cost      # costo por unidad faltante por unidad de tiempo
        self.review_period = review_period      # periodo de revisión para hacer pedido
        self.order_quantity = order_quantity    # cantidad a pedir cuando se ordena
        self.inventory = initial_inventory      # inventario inicial
        self.time = 0
        self.max_time = max_time

        # Variables para seguimiento
        self.inventory_levels = []
        self.backorders = 0
        self.cost_order = 0
        self.cost_holding = 0
        self.cost_shortage = 0

        # Para simular llegada de demanda
        self.next_review = 0
        self.pending_orders = []  # lista de tuplas (arrival_time, quantity)

    def simulate(self):
        dt = 1  # paso de tiempo discreto (1 unidad)
        while self.time < self.max_time:
            # 1. Llegada de pedidos pendientes
            self._receive_orders()

            # 2. Generar demanda (Poisson)
            demand = np.random.poisson(self.demand_rate * dt)

            # 3. Atender demanda
            if demand <= self.inventory:
                self.inventory -= demand
            else:
                self.backorders += demand - self.inventory
                self.inventory = 0

            # 4. Revisar inventario y ordenar si es tiempo
            if self.time >= self.next_review:
                self._place_order()
                self.next_review += self.review_period

            # 5. Calcular costos para este periodo
            self.cost_holding += self.holding_cost * max(self.inventory, 0)
            self.cost_shortage += self.shortage_cost * self.backorders

            self.inventory_levels.append(self.inventory)

            self.time += dt

        self.cost_order = (self.time / self.review_period) * self.order_cost

    def _receive_orders(self):
        # Revisar si algún pedido llega en este tiempo
        arrivals = [order for order in self.pending_orders if order[0] <= self.time]
        for arrival_time, qty in arrivals:
            self.inventory += qty
            if self.backorders > 0:
                # Reducir backorders si hay inventario
                if self.inventory >= self.backorders:
                    self.inventory -= self.backorders
                    self.backorders = 0
                else:
                    self.backorders -= self.inventory
                    self.inventory = 0
            self.pending_orders.remove((arrival_time, qty))

    def _place_order(self):
        # Ordenar sólo si inventario + pedidos pendientes < punto de pedido (simplificado)
        # Aquí se puede ajustar la política según se desee
        # Para simplicidad, ordenamos siempre la cantidad fija
        arrival_time = self.time + self.lead_time
        self.pending_orders.append((arrival_time, self.order_quantity))

    def get_costs(self):
        total_cost = self.cost_order + self.cost_holding + self.cost_shortage
        return {
            'order_cost': self.cost_order,
            'holding_cost': self.cost_holding,
            'shortage_cost': self.cost_shortage,
            'total_cost': total_cost
        }

def run_inventory_experiments(runs=10):
    # Parámetros (puedes modificarlos para análisis de sensibilidad)
    demand_rate = 5          # demanda media por unidad de tiempo
    lead_time = 2            # tiempo de entrega
    order_cost = 50          # costo fijo por ordenar
    holding_cost = 1         # costo por unidad almacenada por unidad de tiempo
    shortage_cost = 10       # costo por unidad faltante por unidad de tiempo
    review_period = 5        # periodo de revisión
    order_quantity = 30      # cantidad a pedir
    max_time = 200           # tiempo total de simulación

    results = []
    for i in range(runs):
        sim = InventorySimulation(demand_rate, lead_time, order_cost, holding_cost,
                                  shortage_cost, review_period, order_quantity, max_time=max_time)
        sim.simulate()
        costs = sim.get_costs()
        results.append(costs)
        print(f"Corrida {i+1}: {costs}")

    # Promedio de costos
    avg_costs = {key: np.mean([r[key] for r in results]) for key in results[0].keys()}
    print("\nPromedio de costos tras", runs, "corridas:")
    for k, v in avg_costs.items():
        print(f"{k}: {v:.2f}")

    # Graficar inventario promedio (de la última corrida)
    plt.plot(sim.inventory_levels)
    plt.title("Nivel de inventario a lo largo del tiempo (última corrida)")
    plt.xlabel("Tiempo")
    plt.ylabel("Inventario")
    plt.grid(True)
    plt.show()

    return avg_costs

if __name__ == "__main__":
    run_inventory_experiments()
