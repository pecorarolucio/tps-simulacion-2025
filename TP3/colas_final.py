import random
import queue
import matplotlib.pyplot as plt

def simular_mm1(lambda_, mu, tiempo_simulacion, n, tamaño_cola):
    # Inicialización de variables
    tiempo_actual = 0.0
    tiempo_proxima_llegada = random.expovariate(lambda_)
    tiempo_proxima_salida = float('inf')
    num_clientes_en_sistema = 0
    tiempo_acumulado_en_sistema = 0.0
    tiempo_acumulado_en_cola = 0.0
    tiempo_total_ocupado = 0.0
    total_clientes_atendidos = 0  # Para calcular el promedio de tiempo
    rechazos = 0  # Contador para rechazos de clientes cuando la cola está llena
    conteo_n_en_cola = 0  # Contador de veces que hay exactamente n clientes en cola

    cola = queue.Queue(maxsize=tamaño_cola)

    while tiempo_actual < tiempo_simulacion:
        if tiempo_proxima_llegada < tiempo_proxima_salida:
            # Evento de llegada
            tiempo_actual = tiempo_proxima_llegada
            num_clientes_en_sistema += 1

            if num_clientes_en_sistema > 1:
                if cola.full():
                    rechazos += 1  # Rechazo si la cola está llena
                    num_clientes_en_sistema -= 1  # Cliente no entra al sistema
                else:
                    cola.put(tiempo_actual)
                    

            else:
                tiempo_proxima_salida = tiempo_actual + random.expovariate(mu)
                tiempo_total_ocupado += tiempo_proxima_salida - tiempo_actual

            tiempo_proxima_llegada = tiempo_actual + random.expovariate(lambda_)
        else:
            # Evento de salida
            tiempo_actual = tiempo_proxima_salida
            num_clientes_en_sistema -= 1
            total_clientes_atendidos += 1

            if not cola.empty():
                tiempo_llegada_cola = cola.get()
                tiempo_acumulado_en_cola += tiempo_actual - tiempo_llegada_cola
                tiempo_proxima_salida = tiempo_actual + random.expovariate(mu)
                tiempo_total_ocupado += tiempo_proxima_salida - tiempo_actual
            else:
                tiempo_proxima_salida = float('inf')

        # Actualizar estadísticas
        tiempo_acumulado_en_sistema += num_clientes_en_sistema * (min(tiempo_proxima_llegada, tiempo_proxima_salida) - tiempo_actual)
        if cola.qsize() == n:
            conteo_n_en_cola += 1


    # Calcular métricas
    promedio_num_en_sistema = tiempo_acumulado_en_sistema / tiempo_simulacion
    promedio_num_en_cola = tiempo_acumulado_en_cola / tiempo_simulacion
    utilizacion = tiempo_total_ocupado / tiempo_simulacion
    promedio_tiempo_en_sistema = tiempo_acumulado_en_sistema / total_clientes_atendidos
    promedio_tiempo_en_cola = tiempo_acumulado_en_cola / total_clientes_atendidos

    probabilidad_n_en_cola = conteo_n_en_cola / tiempo_simulacion
    probabilidad_denegacion_servicio = rechazos / tiempo_simulacion

    return {
        'promedio_numero_en_sistema': promedio_num_en_sistema,
        'promedio_numero_en_cola': promedio_num_en_cola,
        'utilizacion': utilizacion,
        'promedio_tiempo_en_sistema': promedio_tiempo_en_sistema,
        'promedio_tiempo_en_cola': promedio_tiempo_en_cola,
        'probabilidad_n_en_cola': probabilidad_n_en_cola,
        'probabilidad_denegacion_servicio': probabilidad_denegacion_servicio
    }


def graficas_mm1(lambda_, mu, tiempo_simulacion, corridas, n=3, tamaño_cola=10):
    resultados_corridas = {
        'promedio_numero_en_sistema': [],
        'promedio_numero_en_cola': [],
        'utilizacion': [],
        'promedio_tiempo_en_sistema': [],
        'promedio_tiempo_en_cola': [],
        'probabilidad_n_en_cola': [],
        'probabilidad_denegacion_servicio': []
    }

    for _ in range(corridas):
        resultado = simular_mm1(lambda_, mu, tiempo_simulacion, n, tamaño_cola)
        for key in resultados_corridas:
            resultados_corridas[key].append(resultado[key])

    # Valores teóricos
    rho = lambda_ / mu
    L_teorico = float('inf') if rho == 1 else rho / (1 - rho)
    Lq_teorico = (lambda_**2) / (mu * (mu - lambda_)) if rho < 1 else float('inf')
    W_teorico = 1 / (mu - lambda_) if rho < 1 else float('inf')
    Wq_teorico = lambda_ / (mu * (mu - lambda_)) if rho < 1 else float('inf')
    
    # Probabilidad teórica de encontrar n clientes en cola
    Pn_teorico = (1 - rho) * (rho ** n) 
    
    # Probabilidad teórica de denegación de servicio (cola finita de tamaño 20)
    P_denegacion_teorico = (rho ** tamaño_cola) * (1 - rho) / (1 - rho ** (tamaño_cola + 1)) if rho < 1 else 1

    # Promedios simulados
    promedios_simulados = {key: sum(val) / len(val) for key, val in resultados_corridas.items()}

    # Graficar resultados
    plt.figure(figsize=(14, 10))

    # Promedio número de clientes en el sistema
    plt.subplot(3, 3, 1)
    plt.plot(resultados_corridas['promedio_numero_en_sistema'], label="Simulado")
    plt.axhline(y=L_teorico, color='r', linestyle='--', label="Teórico")
    plt.axhline(y=promedios_simulados['promedio_numero_en_sistema'], color='g', linestyle='-.', label="Promedio Simulado")
    plt.title("Promedio número en sistema (L)")
    plt.legend()

    # Promedio número de clientes en cola
    plt.subplot(3, 3, 2)
    plt.plot(resultados_corridas['promedio_numero_en_cola'], label="Simulado")
    plt.axhline(y=Lq_teorico, color='r', linestyle='--', label="Teórico")
    plt.axhline(y=promedios_simulados['promedio_numero_en_cola'], color='g', linestyle='-.', label="Promedio Simulado")
    plt.title("Promedio número en cola (Lq)")
    plt.legend()

    # Utilización del servidor
    plt.subplot(3, 3, 3)
    plt.plot(resultados_corridas['utilizacion'], label="Simulado")
    plt.axhline(y=rho, color='r', linestyle='--', label="Teórico")
    plt.axhline(y=promedios_simulados['utilizacion'], color='g', linestyle='-.', label="Promedio Simulado")
    plt.title("Utilización del servidor (ρ)")
    plt.legend()

    # Promedio tiempo en sistema
    plt.subplot(3, 3, 4)
    plt.plot(resultados_corridas['promedio_tiempo_en_sistema'], label="Simulado")
    plt.axhline(y=W_teorico, color='r', linestyle='--', label="Teórico")
    plt.axhline(y=promedios_simulados['promedio_tiempo_en_sistema'], color='g', linestyle='-.', label="Promedio Simulado")
    plt.title("Promedio tiempo en sistema (W)")
    plt.legend()

    # Promedio tiempo en cola
    plt.subplot(3, 3, 5)
    plt.plot(resultados_corridas['promedio_tiempo_en_cola'], label="Simulado")
    plt.axhline(y=Wq_teorico, color='r', linestyle='--', label="Teórico")
    plt.axhline(y=promedios_simulados['promedio_tiempo_en_cola'], color='g', linestyle='-.', label="Promedio Simulado")
    plt.title("Promedio tiempo en cola (Wq)")
    plt.legend()

    # Probabilidad de encontrar n clientes en cola
    plt.subplot(3, 3, 6)
    plt.plot(resultados_corridas['probabilidad_n_en_cola'], label="Simulado")
    plt.axhline(y=Pn_teorico, color='r', linestyle='--', label="Teórico")
    plt.axhline(y=promedios_simulados['probabilidad_n_en_cola'], color='g', linestyle='-.', label="Promedio Simulado")
    plt.title(f"Probabilidad de encontrar {n} clientes en cola")
    plt.legend()

    # Probabilidad de denegación de servicio
    plt.subplot(3, 3, 7)
    plt.plot(resultados_corridas['probabilidad_denegacion_servicio'], label="Simulado")
    plt.axhline(y=P_denegacion_teorico, color='r', linestyle='--', label="Teórico")
    plt.axhline(y=promedios_simulados['probabilidad_denegacion_servicio'], color='g', linestyle='-.', label="Promedio Simulado")
    plt.title(f"Probabilidad de denegación de servicio (cola={tamaño_cola})")
    plt.legend()

    plt.tight_layout()
    plt.show()


# Ejemplo de uso
graficas_mm1(1.25,1.0,10_000,10,3,10)