import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.stats import chisquare
from scipy.stats import chi2
from scipy.stats import norm



# Parámetros del GCL
a = 1664525
c = 1013904223
m = 2**32
semilla = 4343
n = 100000

# GCL 
def generar_gcl(n, semilla=42, a=1664525, c=1013904223, m=2**32):
    x = semilla
    numeros = []
    for _ in range(n):
        x = (a * x + c) % m
        numeros.append(x / m)
    return numeros

valores = generar_gcl(n)

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

#Comente esto para que me ande el chi^2 dentro del test de poker.
"""# Test de chi-cuadrado
chi2, p_valor = chisquare(frecuencias_obs, f_exp=frecuencia_esp)

print(f"Chi-cuadrado (n=100.000): {chi2:.4f}")
print(f"Valor p: {p_valor:.6f}")"""


#Test de corridas por encima y debajo de la media
def calculo_corridas(valores):
    lista_transformada = []
    media = np.mean(valores)
    for i in valores:  #genero lista de 0 si el valor es menor a la media o 1 si es mayor
        if (i < media): lista_transformada.append(0)
        elif (i>media): lista_transformada.append(1)

    #contar corridas
    corridas = 1
    for i in range(1, len(lista_transformada)):
        if (lista_transformada[i] !=lista_transformada[i-1]):
            corridas += 1

    #cuento cantidad de valores mayores y menores
    mayores = lista_transformada.count(1)
    menores = lista_transformada.count(0) 

    #Calculo de valor esperado y varianza
    media_corridas = (2*mayores*menores) / (mayores + menores) + 1

    #La formula de varianza proviene de: https://influentialpoints.com/Training/runs_tests-principles-properties-assumptions.htm#:~:text=To%20assess%20whether%20a%20given,and%20below%20the%20median%20test.
    #Y tambien de gpt. Es distinta porque es sobre numeros binarios
    varianza_corridas = (2*mayores*menores*(2*mayores*menores-mayores-menores))/\
                        (((mayores+menores)**2)*(mayores+menores-1)) #capaz nombrarlo mayores y menores no fue la mejor idea
    
    #Calculo de Z
    z_corridas = (corridas-media_corridas) / np.sqrt(varianza_corridas)
    p_value = 2 * (1 - norm.cdf(abs(z_corridas))) #no tengo idea, es el valor p que sirve para algo

    print("\nTest de corridas")
    print(f"Cantidad de corridas: {corridas}")
    print(f"Corridas esperadas: {media_corridas}")
    print(f"Valor de Z: {z_corridas}")
    print(F"Valor de p: {p_value}")

    if (abs(z_corridas)<=1.95) and (p_value > 0.05):
        print("✅ No se rechaza H0: aleatorio (α = 0.05)")
    else:
        print("❌ Rechazamos H0: NO aleatorio (α = 0.05)")





# Test de series
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

#Test de poker
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

conteo_glc = poker_test(valores, "GLC")

calculo_corridas(valores)