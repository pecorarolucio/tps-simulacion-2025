import random
import sys
import numpy as np
import matplotlib.pyplot as plt
#En consola adentro de la direccion donde esta el archivo: python RuletaSimulacion.py (Numero de tiradas) (Numero de corridas) (Numero elegido)
XXX = int(sys.argv[1])
YYY = int(sys.argv[2])
X = int(sys.argv[3])

# Listas para almacenar los datos de cada corrida
std_devs_all = []
frecuencias_all = []
promedios_all = []
varianzas_all = []

# Realizar análisis YYY veces
for _ in range(YYY):
    std_devs = []
    frecuencias = []
    promedios = []
    varianzas = []
    values = []

    # Realizar XXX tiradas
    for _ in range(XXX):
        curVal = random.randint(0, 36)
        values.append(curVal)
        std_devs.append(np.std(values))
        freq = values.count(X) / len(values)
        frecuencias.append(freq)
        promedios.append(np.mean(values))
        varianzas.append(np.var(values))

    std_devs_all.append(std_devs)
    frecuencias_all.append(frecuencias)
    promedios_all.append(promedios)
    varianzas_all.append(varianzas)

# Calcular promedios de cada conjunto de datos
yd = np.mean(std_devs_all, axis=0)
yf = 0.027
yp = np.mean(promedios_all, axis=0)
yv = np.mean(varianzas_all, axis=0)

# Graficar los resultados individuales
fig, axs = plt.subplots(2, 2)

# Graficar Desvío Estándar
axs[0, 0].axhline(y=np.mean(std_devs), color='r', linestyle='--')  # Línea de promedio
axs[0, 0].plot(range(len(std_devs)), std_devs, linestyle='-')
axs[0, 0].set_xlabel('n (numero de tiradas)')
axs[0, 0].set_ylabel('Desvío Estándar')
axs[0, 0].grid(True)

# Graficar Frecuencia Relativa
axs[0, 1].axhline(y=yf, color='r', linestyle='--')  # Línea de frecuencia esperada
axs[0, 1].plot(range(len(frecuencias)), frecuencias, 'tab:orange', linestyle='-')
axs[0, 1].set_xlabel('n (numero de tiradas)')
axs[0, 1].set_ylabel('Frecuencia relativa respecto a :{}'.format(X))
axs[0, 1].grid(True)

# Graficar Promedios
axs[1, 0].axhline(y=np.mean(promedios), color='r', linestyle='--')  # Línea de promedio
axs[1, 0].plot(range(len(promedios)), promedios, 'tab:green', linestyle='-')
axs[1, 0].set_xlabel('n (numero de tiradas)')
axs[1, 0].set_ylabel('Valor promedio de las tiradas')
axs[1, 0].grid(True)

# Graficar Varianzas
axs[1, 1].axhline(y=np.mean(varianzas), color='r', linestyle='--')  # Línea de varianza
axs[1, 1].plot(range(len(varianzas)), varianzas, 'tab:red', linestyle='-')
axs[1, 1].set_xlabel('n (numero de tiradas)')
axs[1, 1].set_ylabel('Varianzas')
axs[1, 1].grid(True)

plt.show()

# Graficar los resultados superpuestos
fig, axs = plt.subplots(2, 2)

# Graficar Desvío Estándar
for std_devs in std_devs_all:
    axs[0, 0].plot(range(len(std_devs)), std_devs, linestyle='-')
#axs[0, 0].axhline(y=yd[0], color='r', linestyle='--')  # Línea de promedio
axs[0, 0].set_xlabel('n (numero de tiradas)')
axs[0, 0].set_ylabel('Desvío Estándar')
axs[0, 0].grid(True)

# Graficar Frecuencia Relativa
for frecuencias in frecuencias_all:
    axs[0, 1].plot(range(len(frecuencias)), frecuencias, linestyle='-')
#axs[0, 1].axhline(y=yf, color='r', linestyle='--')  # Línea de frecuencia esperada
axs[0, 1].set_xlabel('n (numero de tiradas)')
axs[0, 1].set_ylabel('Frecuencia relativa respecto a :{}'.format(X))
axs[0, 1].grid(True)

# Graficar Promedios
for promedios in promedios_all:
    axs[1, 0].plot(range(len(promedios)), promedios, linestyle='-')
#axs[1, 0].axhline(y=yp[0], color='r', linestyle='--')  # Línea de promedio
axs[1, 0].set_xlabel('n (numero de tiradas)')
axs[1, 0].set_ylabel('Valor promedio de las tiradas')
axs[1, 0].grid(True)

# Graficar Varianzas
for varianzas in varianzas_all:
    axs[1, 1].plot(range(len(varianzas)), varianzas, linestyle='-')
#axs[1, 1].axhline(y=yv[0], color='r', linestyle='--')  # Línea de varianza
axs[1, 1].set_xlabel('n (numero de tiradas)')
axs[1, 1].set_ylabel('Varianzas')
axs[1, 1].grid(True)

plt.tight_layout()
plt.show()
