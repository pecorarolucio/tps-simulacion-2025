import numpy as np
import heapq
import matplotlib.pyplot as plt

###Explicación y uso
"""
-El código simula un sistema M/M/1 con cola finita (cola de tamaño máximo max_queue_size).
-Se generan eventos de llegada y salida, y se actualizan las métricas en cada evento.
-Se realizan 10 corridas para cada combinación de tasa de llegada (como factor de la tasa de servicio) y tamaño de cola.
-Se calcula promedio de clientes en sistema y cola, tiempos promedio, utilización y probabilidad de bloqueo (rechazo).
-Al final, se grafica un ejemplo de utilización del servidor para cola tamaño 10.
"""


class MM1QueueFinite:
    def __init__(self, arrival_rate, service_rate, max_queue_size, max_customers=1000):
        self.lambda_ = arrival_rate
        self.mu = service_rate
        self.max_queue_size = max_queue_size  # tamaño cola finita (0 = sin cola)
        self.max_customers = max_customers    # número total de clientes a simular

        # Estado del sistema
        self.time = 0.0
        self.server_busy = False
        self.queue = []
        self.num_in_system = 0

        # Estadísticas
        self.arrivals = 0
        self.departures = 0
        self.blocked = 0
        self.area_num_in_system = 0.0
        self.area_num_in_queue = 0.0
        self.last_event_time = 0.0
        self.wait_times = []
        self.queue_lengths = []

        # Eventos: (time, event_type)
        # event_type: 'arrival' o 'departure'
        self.events = []
        # Para guardar tiempo de llegada de clientes en cola (para calcular tiempo en cola)
        self.arrival_times_queue = []

    def schedule_event(self, event_time, event_type):
        heapq.heappush(self.events, (event_time, event_type))

    def run(self):
        # Programar primera llegada
        self.schedule_event(np.random.exponential(1/self.lambda_), 'arrival')

        while self.departures < self.max_customers:
            if not self.events:
                break
            event_time, event_type = heapq.heappop(self.events)

            # Actualizar áreas para promedio
            time_diff = event_time - self.last_event_time
            self.area_num_in_system += self.num_in_system * time_diff
            num_in_queue = max(0, self.num_in_system - (1 if self.server_busy else 0))
            self.area_num_in_queue += num_in_queue * time_diff
            self.last_event_time = event_time
            self.time = event_time

            if event_type == 'arrival':
                self.handle_arrival()
            else:
                self.handle_departure()

        # Resultados
        total_time = self.time
        avg_num_system = self.area_num_in_system / total_time
        avg_num_queue = self.area_num_in_queue / total_time
        avg_time_system = np.mean(self.wait_times) if self.wait_times else 0
        # Tiempo en cola = tiempo en sistema - tiempo servicio (aprox mu^-1)
        avg_time_queue = avg_time_system - (1/self.mu)

        utilization = (self.area_num_in_system - self.area_num_in_queue) / total_time  # tiempo servidor ocupado / total

        prob_block = self.blocked / self.arrivals if self.arrivals > 0 else 0

        # Probabilidad de n clientes en cola (histograma)
        # Para estimar, guardamos la longitud de cola a cada evento (opcional)
        # Aquí se puede devolver la distribución empírica
        return {
            'avg_num_system': avg_num_system,
            'avg_num_queue': avg_num_queue,
            'avg_time_system': avg_time_system,
            'avg_time_queue': avg_time_queue,
            'utilization': utilization,
            'prob_block': prob_block,
            'total_arrivals': self.arrivals,
            'total_blocked': self.blocked
        }

    def handle_arrival(self):
        self.arrivals += 1
        if self.num_in_system > self.max_queue_size:  # cola llena + servidor ocupado
            # Cliente rechazado
            self.blocked += 1
            # No se programa nada más para este cliente
        else:
            # Cliente entra al sistema
            self.num_in_system += 1
            if not self.server_busy:
                # Servidor libre: atender inmediatamente
                self.server_busy = True
                service_time = np.random.exponential(1/self.mu)
                self.schedule_event(self.time + service_time, 'departure')
                # Tiempo en sistema será calculado en salida
                self.wait_times.append(service_time)  # sin espera en cola
            else:
                # Servidor ocupado, cliente espera en cola
                self.arrival_times_queue.append(self.time)

        # Programar próxima llegada
        next_arrival = self.time + np.random.exponential(1/self.lambda_)
        self.schedule_event(next_arrival, 'arrival')

    def handle_departure(self):
        self.departures += 1
        self.num_in_system -= 1
        if self.num_in_system >= 1:
            # Hay clientes en cola, atender siguiente
            self.server_busy = True
            # Calcular tiempo en cola para el cliente que sale ahora
            arrival_time = self.arrival_times_queue.pop(0)
            wait_in_queue = self.time - arrival_time
            service_time = np.random.exponential(1/self.mu)
            self.wait_times.append(wait_in_queue + service_time)
            self.schedule_event(self.time + service_time, 'departure')
        else:
            # Cola vacía, servidor libre
            self.server_busy = False


def run_experiments(mu=1.0, queue_sizes=[0,2,5,10,50], lambda_factors=[0.25,0.5,0.75,1.0,1.25], runs=10):
    results = {}
    for q_size in queue_sizes:
        print(f"\nCola finita tamaño: {q_size}")
        results[q_size] = {}
        for lf in lambda_factors:
            lam = lf * mu
            metrics_runs = []
            for _ in range(runs):
                sim = MM1QueueFinite(arrival_rate=lam, service_rate=mu, max_queue_size=q_size, max_customers=1000)
                res = sim.run()
                metrics_runs.append(res)
            # Promedio de métricas
            avg_metrics = {}
            for key in metrics_runs[0].keys():
                if key in ['total_arrivals', 'total_blocked']:
                    avg_metrics[key] = sum([m[key] for m in metrics_runs]) / runs
                else:
                    avg_metrics[key] = np.mean([m[key] for m in metrics_runs])
            results[q_size][lf] = avg_metrics
            print(f"λ/μ={lf:.2f} | Avg clientes en sistema: {avg_metrics['avg_num_system']:.3f} | "
                  f"Avg clientes en cola: {avg_metrics['avg_num_queue']:.3f} | "
                  f"Utilización: {avg_metrics['utilization']:.3f} | "
                  f"Prob. bloqueo: {avg_metrics['prob_block']:.4f}")
    return results

def theoretical_mm1_metrics(lambda_, mu, queue_size):
    rho = lambda_ / mu
    if rho >= 1:
        # Sistema inestable, no hay valores finitos
        return None

    if queue_size == float('inf'):
        # M/M/1 cola infinita
        Ls = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        Ws = 1 / (mu - lambda_)
        Wq = lambda_ / (mu * (mu - lambda_))
        p_block = 0.0
    else:
        # M/M/1/K cola finita
        # Probabilidad de rechazo
        numerator = (1 - rho) * (rho ** queue_size)
        denominator = 1 - (rho ** (queue_size + 1))
        p_block = numerator / denominator

        # Para Ls, Lq, Ws, Wq se usan fórmulas más complejas o aproximaciones
        # Aquí se usa aproximación para Ls (media clientes en sistema):
        # Ls = sum_{n=0}^K n * P_n, con P_n = (1 - rho)/(1 - rho^{K+1}) * rho^n
        P0 = (1 - rho) / (1 - rho ** (queue_size + 1))
        Ls = sum(n * P0 * rho ** n for n in range(queue_size + 1))
        Lq = Ls - (1 - p_block)  # aproximación: clientes en cola = en sistema - en servicio
        Ws = Ls / (lambda_ * (1 - p_block)) if lambda_ * (1 - p_block) > 0 else float('inf')
        Wq = Ws - 1/mu

    return {
        'avg_num_system': Ls,
        'avg_num_queue': Lq,
        'avg_time_system': Ws,
        'avg_time_queue': Wq,
        'utilization': rho,
        'prob_block': p_block
    }


if __name__ == "__main__":
# Parámetros base
    mu = 1.0
    queue_sizes = [0, 2, 5, 10, 50]
    lambda_factors = [0.25, 0.5, 0.75, 1.0, 1.25]
    runs = 10

    # Ejecutar simulación
    sim_results = run_experiments(mu=mu, queue_sizes=queue_sizes, lambda_factors=lambda_factors, runs=runs)

    print("\nComparación Simulación vs Teoría\n")
    for q_size in queue_sizes:
        print(f"Cola finita tamaño: {q_size}")
        for lf in lambda_factors:
            lam = lf * mu
            sim = sim_results[q_size][lf]
            teor = theoretical_mm1_metrics(lam, mu, q_size if q_size > 0 else float('inf'))
            if teor is None:
                print(f"λ/μ={lf:.2f}: Sistema inestable (ρ≥1)")
                continue
            print(f"λ/μ={lf:.2f} | Sim avg clientes en sistema: {sim['avg_num_system']:.3f} | Teor: {teor['avg_num_system']:.3f}")
            print(f"           Sim avg tiempo en sistema: {sim['avg_time_system']:.4f} | Teor: {teor['avg_time_system']:.4f}")
            print(f"           Sim avg tiempo en cola: {sim['avg_time_queue']:.4f} | Teor: {teor['avg_time_queue']:.4f}")
            #print(f"           Sim utilización: {sim['utilization']:.3f} | Teor: {teor['utilization']:.3f}")
        print()
