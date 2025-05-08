import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, chisquare

n = 100000
valores = [random.random() for _ in range(n)]

# 1. Histograma
plt.hist(valores, bins=50, edgecolor='black')
plt.title("Histograma random.random()")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.show()

# 2. Correlación lineal (U_n vs U_n+1)
pares = [(valores[i], valores[i+1]) for i in range(n - 1)]
x_vals, y_vals = zip(*pares)
corr, p_valor = pearsonr(x_vals, y_vals)

print(f"Coeficiente de correlación (Pearson): {corr:.6f}")
print(f"Valor p asociado: {p_valor:.6f}")

# Gráfico dispersión 2D
plt.figure(figsize=(6, 6))
plt.scatter(x_vals, y_vals, s=1, alpha=0.5)
plt.title("Gráfico dispersión random.random()")
plt.xlabel("U_n")
plt.ylabel("U_n+1")
plt.grid(True)
plt.show()

# 3. Gráfico 3D (U_n, U_n+1, U_n+2)
from mpl_toolkits.mplot3d import Axes3D
trios = [(valores[i], valores[i+1], valores[i+2]) for i in range(n - 2)]
x_vals, y_vals, z_vals = zip(*trios)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_vals, y_vals, z_vals, s=1, alpha=0.5)
ax.set_title("Gráfico 3D random.random()")
ax.set_xlabel("U_n")
ax.set_ylabel("U_n+1")
ax.set_zlabel("U_n+2")
plt.tight_layout()
plt.show()

# 4. Test Chi-cuadrado (Frecuencia)
k = 10
frecuencias_obs, _ = np.histogram(valores, bins=k, range=(0, 1))
frecuencia_esp = [n / k] * k
chi2, p_chi = chisquare(frecuencias_obs, f_exp=frecuencia_esp)

print(f"Chi-cuadrado (n=100000): {chi2:.4f}")
print(f"Valor p: {p_chi:.6f}")

# 5. Test de corridas
def contar_corridas(valores):
    r = 1
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
