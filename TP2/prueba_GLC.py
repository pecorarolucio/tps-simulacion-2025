import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.stats import chisquare

# Parámetros del GCL
a = 1664525
c = 1013904223
m = 2**32
semilla = 4343
n = 100000


x = semilla
valores = []

for _ in range(n):
    x = (a * x + c) % m
    u = x / m
    valores.append(u)

# Armar los pares (U_n, U_{n+1})
pares = [(valores[i], valores[i+1]) for i in range(n - 1)]
x_vals, y_vals = zip(*pares)

# Gráfico de dispersión
plt.figure(figsize=(6, 6))
plt.scatter(x_vals, y_vals, s=1, alpha=0.5)
plt.title("Gráfico de dispersión: (U_n, U_{n+1}) - GCL")
plt.xlabel("U_n")
plt.ylabel("U_{n+1}")
plt.grid(True)
plt.show()


# Calcular el coeficiente de correlación de Pearson
corr, p_valor = pearsonr(x_vals, y_vals)

print(f"Coeficiente de correlación (Pearson): {corr:.6f}")
print(f"Valor p asociado: {p_valor:.6f}")


# Armar las tríadas (U_n, U_{n+1}, U_{n+2})
trios = [(valores[i], valores[i+1], valores[i+2]) for i in range(n - 2)]
x_vals, y_vals, z_vals = zip(*trios)

# gráfico 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_vals, y_vals, z_vals, s=1, alpha=0.5)

ax.set_title("Gráfico 3D: (U_n, U_{n+1}, U_{n+2}) - GCL")
ax.set_xlabel("U_n")
ax.set_ylabel("U_{n+1}")
ax.set_zlabel("U_{n+2}")
plt.tight_layout()
plt.show()

#test de chi cuadrado
#cantidad de intervalos
k = 10

#Contamos ocurrencias en cada intervalo
frecuencias_obs, _ = np.histogram(valores, bins=k, range=(0, 1))

#Frecuencia esperada si fuera perfectamente uniforme
frecuencia_esp = [n / k] * k

# Test de chi-cuadrado
chi2, p_valor = chisquare(frecuencias_obs, f_exp=frecuencia_esp)

print(f"Chi-cuadrado (n=100.000): {chi2:.4f}")
print(f"Valor p: {p_valor:.6f}")


# Test de corridas
def contar_corridas(valores):
    r = 1  # siempre hay al menos una corrida
    for i in range(1, len(valores) - 1):
        if (valores[i] > valores[i - 1] and valores[i] > valores[i + 1]) or \
           (valores[i] < valores[i - 1] and valores[i] < valores[i + 1]):
            r += 1
    return r

r = contar_corridas(valores)
mu = (2 * n - 1) / 3
sigma2 = (16 * n - 29) / 90
z = (r - mu) / np.sqrt(sigma2)

print(f"Cantidad de corridas observadas: {r}")
print(f"Esperado (media): {mu:.2f}")
print(f"Z = {z:.4f}")
