import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import pandas as pd

class MM1Simulator:
    def __init__(self, lambda_rate, mu_rate, max_time, queue_size=float('inf'), target_n=3):
        self.lambda_rate = lambda_rate
        self.mu_rate = mu_rate
        self.max_time = max_time
        self.queue_size = queue_size
        self.target_n = target_n

        self.queue = deque()
        self.current_time = 0
        self.next_arrival = np.random.exponential(1/lambda_rate)
        self.next_departure = float('inf')

        self.total_customers = 0
        self.customers_in_system = 0
        self.customers_in_queue = 0
        self.total_wait_time = 0
        self.total_system_time = 0
        self.server_busy_time = 0
        self.denied_service = 0
        self.time_in_n_queue = 0

        self.time_history = [0]
        self.queue_length_history = [0]
        self.system_length_history = [0]

    def run(self):
        while self.current_time < self.max_time:
            if self.next_arrival < self.next_departure:
                self.process_arrival()
            else:
                self.process_departure()

        self.process_end_of_simulation()

    def process_arrival(self):
        self.update_time_in_n_queue()
        self.current_time = self.next_arrival
        self.total_customers += 1

        if len(self.queue) < self.queue_size:
            self.customers_in_system += 1
            if self.customers_in_system == 1:
                self.next_departure = self.current_time + np.random.exponential(1/self.mu_rate)
            else:
                self.customers_in_queue += 1
                self.queue.append(self.current_time)
        else:
            self.denied_service += 1

        self.next_arrival = self.current_time + np.random.exponential(1/self.lambda_rate)
        self.update_history()

    def process_departure(self):
        self.update_time_in_n_queue()
        self.current_time = self.next_departure
        self.customers_in_system -= 1
        self.server_busy_time += self.next_departure - max(self.time_history[-1], self.next_arrival)

        if self.queue:
            arrival_time = self.queue.popleft()
            self.total_wait_time += self.current_time - arrival_time
            self.total_system_time += self.current_time - arrival_time
            self.customers_in_queue -= 1
            self.next_departure = self.current_time + np.random.exponential(1/self.mu_rate)
        else:
            self.next_departure = float('inf')

        self.update_history()

    def process_end_of_simulation(self):
        while self.queue:
            arrival_time = self.queue.popleft()
            self.total_wait_time += self.max_time - arrival_time
            self.total_system_time += self.max_time - arrival_time

    def update_time_in_n_queue(self):
        if self.queue_length_history[-1] == self.target_n:
            delta_time = self.current_time - self.time_history[-1]
            self.time_in_n_queue += delta_time

    def update_history(self):
        self.time_history.append(self.current_time)
        self.queue_length_history.append(self.customers_in_queue)
        self.system_length_history.append(self.customers_in_system)

    def get_performance_measures(self):
        avg_customers_system = np.mean(self.system_length_history)
        avg_customers_queue = np.mean(self.queue_length_history)
        avg_time_system = self.total_system_time / self.total_customers if self.total_customers > 0 else 0
        avg_time_queue = self.total_wait_time / self.total_customers if self.total_customers > 0 else 0
        server_utilization = self.server_busy_time / self.max_time
        denied_service_prob = self.denied_service / self.total_customers if self.total_customers > 0 else 0
        prob_n_in_queue = self.time_in_n_queue / self.max_time

        return {
            "avg_customers_system": avg_customers_system,
            "avg_customers_queue": avg_customers_queue,
            "avg_time_system": avg_time_system,
            "avg_time_queue": avg_time_queue,
            "server_utilization": server_utilization,
            "denied_service_prob": denied_service_prob,
            "prob_n_in_queue": prob_n_in_queue
        }

    def get_theoretical_measures(self):
        rho = self.lambda_rate / self.mu_rate
        if rho >= 1:
            return {
                "L": float('inf'),
                "Lq": float('inf'),
                "W": float('inf'),
                "Wq": float('inf'),
                "rho": rho,
                "Pn": 0,
                "P_denial": 1 if self.queue_size != float('inf') else 0
            }

        L = rho / (1 - rho)
        Lq = (rho**2) / (1 - rho)
        W = 1 / (self.mu_rate - self.lambda_rate)
        Wq = rho / (self.mu_rate - self.lambda_rate)
        Pn = (1 - rho) * (rho ** self.target_n)
        if self.queue_size == float('inf'):
            P_denial = 0
        else:
            P_denial = ((1 - rho) * rho**self.queue_size) / (1 - rho**(self.queue_size + 1))

        return {
            "L": L,
            "Lq": Lq,
            "W": W,
            "Wq": Wq,
            "rho": rho,
            "Pn": Pn,
            "P_denial": P_denial
        }
    def plot_queue_length(self):
        plt.figure(figsize=(10, 6))
        plt.step(self.time_history, self.queue_length_history, where='post')
        plt.xlabel('Time')
        plt.ylabel('Queue Length')
        plt.title('Queue Length over Time')
        plt.grid(True)
        plt.show()

def run_mm1_experiments(mu_rate, max_time, num_runs, queue_sizes, lambda_percentages):
    results = {}
    
    for queue_size in queue_sizes:
        for lambda_percentage in lambda_percentages:
            lambda_rate = mu_rate * lambda_percentage
            
            avg_measures = {
                "avg_customers_system": 0,
                "avg_customers_queue": 0,
                "avg_time_system": 0,
                "avg_time_queue": 0,
                "server_utilization": 0,
                "denied_service_prob": 0
            }
            
            for _ in range(num_runs):
                simulator = MM1Simulator(lambda_rate, mu_rate, max_time, queue_size)
                simulator.run()
                measures = simulator.get_performance_measures()
                
                for key in avg_measures:
                    avg_measures[key] += measures[key]
            
            for key in avg_measures:
                avg_measures[key] /= num_runs
            
            results[(queue_size, lambda_percentage)] = avg_measures
    
    return results

def save_results_to_csv(results, filename="mm1_results.csv"):
    rows = []
    for (queue_size, lambda_percentage), measures in results.items():
        row = {
            "queue_size": queue_size,
            "lambda_percentage": lambda_percentage,
            **measures
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)

def plot_metric_vs_lambda(results, metric_name, queue_size):
    x = []
    y = []
    for (q_size, lam_pct), measures in results.items():
        if q_size == queue_size:
            x.append(lam_pct)
            y.append(measures[metric_name])
    plt.plot(x, y, marker='o')
    plt.title(f"{metric_name} vs Lambda % (Queue Size {queue_size})")
    plt.xlabel("Lambda / Mu")
    plt.ylabel(metric_name)
    plt.grid(True)
    plt.show()

#Ejecución de todos los datos que pide
"""# Parámetros de simulación
mu_rate = 1.0  # Tasa de servicio base
max_time = 10000  # Tiempo total de simulación
num_runs = 10  # Número de corridas por experimento
queue_sizes = [float('inf'), 0, 2, 5, 10, 50]  # Tamaños de cola a evaluar
lambda_percentages = [0.25, 0.50, 0.75, 1.00, 1.25]  # Porcentajes de tasa de llegada respecto a la tasa de servicio

# Justificación:
# - mu_rate = 1.0: Elegimos una tasa de servicio unitaria para facilitar la interpretación de los resultados.
# - max_time = 10000: Un tiempo de simulación largo para asegurar que el sistema alcance un estado estable.
# - num_runs = 10: Cumple con el requisito mínimo de corridas.
# - queue_sizes: Incluye el caso de cola infinita y los tamaños específicos solicitados en el enunciado.
# - lambda_percentages: Corresponden a los porcentajes solicitados en el enunciado (25%, 50%, 75%, 100%, 125% de la tasa de servicio).

# Ejecutar experimentos
results = run_mm1_experiments(mu_rate, max_time, num_runs, queue_sizes, lambda_percentages)
save_results_to_csv(results, "mm1_results.csv")
# Imprimir resultados
for (queue_size, lambda_percentage), measures in results.items():
    print(f"Queue Size: {queue_size}, Lambda: {lambda_percentage * 100}% of Mu")
    for key, value in measures.items():
        print(f"  {key}: {value:.4f}")
    print()"""

# Ejemplo de grafico y comparación de resultados para una simulación especifica
sim = MM1Simulator(lambda_rate=0.75, mu_rate=1.0, max_time=10000, queue_size=10, target_n=3)
sim.run()
sim.plot_queue_length()
sim_measures = sim.get_performance_measures()
theory_measures = sim.get_theoretical_measures()


if __name__ == "__main__":
    # Parámetros generales
    mu_rate = 1.0
    max_time = 10000
    num_runs = 10
    queue_sizes = [float('inf'), 0, 2, 5, 10, 50]
    lambda_percentages = [0.25, 0.50, 0.75, 1.00, 1.25]

    # Simulación completa
    results = run_mm1_experiments(mu_rate, max_time, num_runs, queue_sizes, lambda_percentages)
    save_results_to_csv(results)

    # Simulación individual
    sim = MM1Simulator(lambda_rate=0.75, mu_rate=1.0, max_time=10000, queue_size=10, target_n=3)
    sim.run()
    sim.plot_queue_length()

    # Comparación Sim vs Teoría
    sim_measures = sim.get_performance_measures()
    theory_measures = sim.get_theoretical_measures()
    print("\nMedidas Simuladas:")
    for key, val in sim_measures.items():
        print(f"  {key}: {val:.4f}")
    print("\nMedidas Teóricas:")
    for key, val in theory_measures.items():
        print(f"  {key}: {val:.4f}")

    # Gráfico ejemplo
    plot_metric_vs_lambda(results, "avg_time_queue", queue_size=10)
