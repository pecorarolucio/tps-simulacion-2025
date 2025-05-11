import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import chisquare

# Función RANDU: Xn+1 = (65539 * Xn) % 2^31
def randu(n, seed=1):
    a = 65539
    m = 2**31
    x = seed
    r = []
    for _ in range(n):
        x = (a * x) % m
        r.append(x / m)  # Normalizar a [0, 1)
    return r

# Generar n valores
n = 100000
r = randu(n)


# Armar los pares (U_n, U_{n+1})
pares = [(r[i], r[i+1]) for i in range(n - 1)]
x_vals, y_vals = zip(*pares)

# Calcular el coeficiente de correlación de Pearson
corr, p_valor = pearsonr(x_vals, y_vals)

print(f"Coeficiente de correlación (Pearson): {corr:.6f}")
print(f"Valor p asociado: {p_valor:.6f}")


# Armar las tríadas (U_n, U_{n+1}, U_{n+2})
trios = [(r[i], r[i+1], r[i+2]) for i in range(n - 2)]
x_vals, y_vals, z_vals = zip(*trios)

# Histograma
plt.hist(r, bins=50, edgecolor='black')
plt.title("Histograma RANDU")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.show()

# Gráfico dispersión 2D
plt.figure(figsize=(6, 6))
plt.scatter(x_vals, y_vals, s=1, alpha=0.5)
plt.title("Gráfico dispersión RANDU")
plt.xlabel("U_n")
plt.ylabel("U_n+1")
plt.grid(True)
plt.show()

# Gráfico 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_vals, y_vals, z_vals, s=1, alpha=0.5)

ax.set_title("Gráfico 3D: (U_n, U_{n+1}, U_{n+2}) - GCL")
ax.set_xlabel("U_n")
ax.set_ylabel("U_{n+1}")
ax.set_zlabel("U_{n+2}")
plt.tight_layout()
plt.show()