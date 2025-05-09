import random
from scipy.stats import chi2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, chisquare

random.seed(42)
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
#Comento esto para que ande el test de poker
"""k = 10
frecuencias_obs, _ = np.histogram(valores, bins=k, range=(0, 1))
frecuencia_esp = [n / k] * k
chi2, p_chi = chisquare(frecuencias_obs, f_exp=frecuencia_esp)
print(f"Chi-cuadrado (n=100000): {chi2:.4f}")
print(f"Valor p: {p_chi:.6f}")"""

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

# 6. Test de poker
"""Bibliografía: https://idoc.pub/documents/idocpub-6klz2po2qvlg"""
def clasificar_mano(digitos):
    conteo = {}
    for d in digitos:
        conteo[d] = conteo.get(d, 0) + 1
    valores = sorted(conteo.values(), reverse=True)
    if valores == [5]: return "generala"
    if valores == [4,1]: return "póker"
    if valores == [3,2]: return "full"
    if valores == [3,1,1]: return "trío"
    if valores == [2,2,1]: return "doble par"
    if valores == [2,1,1,1]: return "un par"
    return "todos distintos"

def poker_test(numeros, nombre=""):
    n = len(numeros)
    categorias = ["todos distintos", "un par", "doble par", "trío", "full", "póker", "generala"]
    conteo_obs = {cat: 0 for cat in categorias}

    for num in numeros:
        digitos = list(str(num)[2:7])
        if len(digitos) < 5:
            continue
        categoria = clasificar_mano(digitos)
        conteo_obs[categoria] += 1

    probs = {
        "todos distintos": 0.3024,
        "un par": 0.5040,
        "doble par": 0.1080,
        "trío": 0.0720,
        "full": 0.0090,
        "póker": 0.0045,
        "generala": 0.0001
    }

    chi2_stat = 0
    print(f"\n🔍 Resultados para: {nombre}")
    print("Categoría\tObs.\tEsp.\t(Obs-Esp)^2/Esp")
    for cat in categorias:
        esperada = probs[cat] * n
        observada = conteo_obs[cat]
        chi2_parcial = (observada - esperada) ** 2 / esperada
        chi2_stat += chi2_parcial
        print(f"{cat:<15}{observada:>5}\t{esperada:>6.1f}\t{chi2_parcial:>7.3f}")

    gl = len(categorias) - 1
    p_value = 1 - chi2.cdf(chi2_stat, gl)
    print(f"Chi² = {chi2_stat:.3f}, gl = {gl}, p-valor = {p_value:.4f}")
    if p_value < 0.05:
        print("❌ Rechazamos H0: NO aleatorio (α = 0.05)")
    else:
        print("✅ No se rechaza H0: aleatorio (α = 0.05)")

    return conteo_obs

conteo_rand = poker_test(valores, "random.random()")
