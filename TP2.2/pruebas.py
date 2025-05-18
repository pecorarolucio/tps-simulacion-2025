import random
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import chisquare, expon, norm, binom, poisson, chi2
import math
import numpy as np

def distr_uniforme(a, b, size=1):
    """
    Distribucion uniforme
    a, b: rango de valores
    """
    x=[]
    for _ in range(size):
        x.append(a+(b-a)*random.random())
    return x

def distr_exp(ex, size=1):
    x=[]
    for _ in range(size):
        x.append(-ex*math.log(random.random()))
    return x

def distr_gamma(k, a, size=1):
    """
    Generador de valores con distribucion gamma basado en el libro
    k, a: parametros necesarios para distribucion gamma
    """
    x=[]
    for _ in range(1, size):
        tr = 1
        for _ in range(1, k):
            tr = tr*random.random()
        x.append(-(math.log(tr)/a))
    return x

def distr_normal(ex, stdx, size=1):
    x=[]
    for _ in range(size):
        sum=0
        for _ in range(12):
            sum=sum+random.random()
        x.append(stdx*(sum-6)+ex)
    return x

def distr_pascal(k, q, size=1): #en el libro esta como binomial negativa, es un caso especial de esa
    nx=[]
    for _ in range(size):
        tr = 1
        for _ in range(k):
            tr *= random.random()
        x = math.log(tr) // math.log(q)
        nx.append(x)
    return nx

def distr_binomial(n, p, size=1):
    x=[]
    for _ in range(size):
        y=0
        for _ in range(1, n):
            if((random.random()-p)<0):
                y+=1
        x.append(y)
    return x

def distr_hipergeometrica(tn, ns, p, size=1):
    x=[]
    for _ in range(size):
        tn1=tn
        ns1=ns
        p1=p
        y=0
        for _ in range(1, ns1):
            if((random.random() -p1) > 0):
                s=0
            else:
                s=1
                y+=1
            p1=(tn1*p1-s)/(tn1-1)
            tn1-=1
        x.append(y)
    return x

def distr_poisson(lambd, size=1):  # λ es la media (esperada) de la distribución
    x = []
    for _ in range(size):
        L = math.exp(-lambd)
        k = 0
        p = 1
        while p > L:
            k += 1
            p *= random.random()
        x.append(k - 1)
    return x


"""def distr_empiricadiscr(probs, size=1): #empirica discreta
    x = []
    for _ in range(size):
        a = 0
        z = 0
        for i in probs:
            a += i
            if random.random() <= a:
                break
            else:
                z += 1
        x.append(z)
    return x """ #La comento porque creo que esta mal

def distr_empiricadiscr_corregida(probs, size=1): #creo que esta bien
    x = []
    for _ in range(size):
        u = random.random()
        acum = 0
        z = 0
        for i, prob in enumerate(probs):
            acum += prob
            if u < acum:
                z = i
                break
        x.append(z)
    return x


#PRUEBAS DE CHI CUADRADO PARA CADA DISTRIBUCION

def ajustar_esperadas(expected_freq, observed_freq):
    expected_freq = np.array(expected_freq)
    total_obs = np.sum(observed_freq)
    total_exp = np.sum(expected_freq)
    return expected_freq * (total_obs / total_exp)

def test_chi2_uniforme(valores, num_intervalos=10, alpha=0.05):
    n = len(valores)
    min_val = min(valores)
    max_val = max(valores)
    bins = np.linspace(min_val, max_val, num_intervalos + 1)
    observed_freq, _ = np.histogram(valores, bins)

    expected_freq = [(1 / num_intervalos) * n] * num_intervalos
    expected_freq = ajustar_esperadas(expected_freq, observed_freq)

    df = num_intervalos - 1
    chi2_stat, p_valor = chisquare(observed_freq, expected_freq)

    print("Distribución: Uniforme")
    print("Chi²:", chi2_stat)
    print("p-valor:", p_valor)
    print("Grados de libertad:", df)
    print("Valor crítico:", chi2.ppf(1 - alpha, df))
    print("✅" if p_valor >= alpha else "❌")


def test_chi2_exponencial(valores, num_intervalos=10, alpha=0.05):
    n = len(valores)
    lambd = 1 / np.mean(valores)
    bins = np.linspace(min(valores), max(valores), num_intervalos + 1)
    observed_freq, _ = np.histogram(valores, bins)

    expected_freq = []
    for i in range(len(bins) - 1):
        p = expon.cdf(bins[i + 1], scale=1/lambd) - expon.cdf(bins[i], scale=1/lambd)
        expected_freq.append(n * p)
    expected_freq = ajustar_esperadas(expected_freq, observed_freq)

    df = num_intervalos - 1 - 1  # 1 parámetro (lambda)
    chi2_stat, p_valor = chisquare(observed_freq, expected_freq)

    print("Distribución: Exponencial")
    print("Chi²:", chi2_stat)
    print("p-valor:", p_valor)
    print("Grados de libertad:", df)
    print("Valor crítico:", chi2.ppf(1 - alpha, df))
    print("✅" if p_valor >= alpha else "❌")

def test_chi2_poisson(valores, alpha=0.05):
    from scipy.stats import poisson
    vals, obs_freq = np.unique(valores, return_counts=True)
    media = np.mean(valores)
    max_k = max(vals)

    expected_freq = [poisson.pmf(k, media) * len(valores) for k in vals]
    expected_freq = ajustar_esperadas(expected_freq, obs_freq)

    df = len(vals) - 1 - 1  # 1 parámetro estimado (λ)
    chi2_stat, p_valor = chisquare(obs_freq, expected_freq)

    print("Distribución: Poisson")
    print("Chi²:", chi2_stat)
    print("p-valor:", p_valor)
    print("Grados de libertad:", df)
    print("Valor crítico:", chi2.ppf(1 - alpha, df))
    print("✅" if p_valor >= alpha else "❌")

def test_chi2_empirica_discreta(valores, p, alpha=0.05):
    valores_posibles = list(range(len(p)))
    obs_freq = [valores.count(v) for v in valores_posibles]
    expected_freq = [len(valores) * pi for pi in p]
    expected_freq = ajustar_esperadas(expected_freq, obs_freq)

    df = len(p) - 1
    chi2_stat, p_valor = chisquare(obs_freq, expected_freq)

    print("Distribución: Empírica Discreta")
    print("Chi²:", chi2_stat)
    print("p-valor:", p_valor)
    print("Grados de libertad:", df)
    print("Valor crítico:", chi2.ppf(1 - alpha, df))
    print("✅" if p_valor >= alpha else "❌")

def test_chi2_binomial(valores, n_binom, p_binom, alpha=0.05):
    from scipy.stats import binom
    vals, obs_freq = np.unique(valores, return_counts=True)
    expected_freq = [binom.pmf(k, n_binom, p_binom) * len(valores) for k in vals]
    expected_freq = ajustar_esperadas(expected_freq, obs_freq)

    df = len(vals) - 1 - 1  # solo 1 parámetro se estima si es necesario (p)
    chi2_stat, p_valor = chisquare(obs_freq, expected_freq)

    print("Distribución: Binomial")
    print("Chi²:", chi2_stat)
    print("p-valor:", p_valor)
    print("Grados de libertad:", df)
    print("Valor crítico:", chi2.ppf(1 - alpha, df))
    print("✅" if p_valor >= alpha else "❌")

def test_chi2_normal(valores, num_intervalos=10, alpha=0.05):
    n = len(valores)
    media = np.mean(valores)
    desviacion = np.std(valores, ddof=1)

    # Crear intervalos equiespaciados en base a los datos
    bins = np.linspace(min(valores), max(valores), num_intervalos + 1)
    observed_freq, _ = np.histogram(valores, bins)

    # Calcular frecuencias esperadas usando la CDF de la normal
    expected_freq = []
    for i in range(len(bins) - 1):
        prob = norm.cdf(bins[i+1], media, desviacion) - norm.cdf(bins[i], media, desviacion)
        expected_freq.append(n * prob)

    # Ajustar esperadas para que sumen lo mismo que las observadas
    expected_freq = np.array(expected_freq)
    expected_freq *= observed_freq.sum() / expected_freq.sum()

    # Fusionar clases si alguna esperada < 5 (opcional)

    # Grados de libertad: k - 1 - c (c=2 si estimamos media y desviación)
    df = num_intervalos - 1 - 2
    chi2_stat, p_valor = chisquare(f_obs=observed_freq, f_exp=expected_freq)

    print("Chi²:", chi2_stat)
    print("p-valor:", p_valor)
    print("Grados de libertad:", df)
    chi2_critico = chi2.ppf(1 - alpha, df)
    print("Valor crítico (chi²):", chi2_critico)

    if p_valor < alpha:
        print("❌ Rechazamos la hipótesis nula")
    else:
        print("✅ No se rechaza la hipótesis nula")

#Graficar
def graficar(u, g, e, n, p, b, em, pas, hipergeo):
    plt.figure(1)
    plt.title("Distribución Uniforme")
    plt.hist(u, edgecolor='black')
    plt.grid(True)

    plt.show()

    plt.figure(2)
    plt.title("Distribución Gamma")
    plt.hist(g, edgecolor='black')
    plt.grid(True)

    plt.show()

    plt.figure(3)
    plt.title("Distribución Exponencial")
    plt.hist(e, 25, edgecolor='black')
    plt.grid(True)

    plt.show()

    plt.figure(4)
    plt.title("Distribución Normal")
    plt.hist(n, 25, edgecolor='black')
    plt.grid(True)
    plt.show()

    plt.figure(5)
    plt.title("Distribución Poisson")
    plt.hist(p, 25, edgecolor='black')
    plt.grid(True)
    plt.show()

    plt.figure(6)
    plt.title("Distribución Binomial")
    plt.hist(b, 25, edgecolor='black')
    plt.grid(True)
    plt.show()

    plt.figure(7)
    plt.title("Distribución Empirica")
    plt.hist(em, edgecolor='black')
    plt.grid(True)
    plt.show()

    plt.figure(8)
    plt.title("Distribución Pascal")
    plt.hist(pas, edgecolor='black')
    plt.grid(True)
    plt.show()

    plt.figure(9)
    plt.title("Distribución Hipergeometrica")
    plt.hist(hipergeo, edgecolor='black')
    plt.grid(True)

    plt.show()

def inicio():
    p = [0.273, 0.037, 0.195, 0.009, 0.124, 0.058, 0.062, 0.151, 0.047, 0.044] #tabla del libro
    uni = (distr_uniforme(0, 5, 1000))
    gam = (distr_gamma(5, 20, 1000))
    expo = (distr_exp(5, 1000))
    nor = distr_normal(2.35, 30, 1000)
    poi = distr_poisson(50, 1000)
    bino = distr_binomial(10, 0.4, 1000)
    #empi = distr_empiricadiscr(p, 1000)
    pas = distr_pascal(5, 0.4, 1000)
    hipergeo = distr_hipergeometrica(5000000, 500, 0.4, 1000)
    empi2 = distr_empiricadiscr_corregida(p, 1000)

    test_chi2_normal(nor)
    test_chi2_empirica_discreta(empi2, p)
    test_chi2_binomial(bino, 10, 0.4)
    test_chi2_uniforme(uni)
    test_chi2_poisson(poi)
    test_chi2_exponencial(expo)
    
    graficar(uni, gam, expo, nor, poi, bino, empi2, pas, hipergeo)

inicio()