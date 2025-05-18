import random
import math
import matplotlib.pyplot as plt

#Valor n
n=10000

def distr_uniforme(a, b, size):
    """
    Distribucion uniforme
    a, b: rango de valores
    """
    x=[]
    for _ in range(size):
        x.append(a+(b-a)*random.random())
    return x

# Test: generar 10.000 números entre 5 y 15
datos_uniforme = distr_uniforme(5, 15, n)

# Graficar histograma
plt.hist(datos_uniforme, bins=50, density=True, edgecolor='black')
plt.title('Distribución Uniforme Continua U(5, 15)')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.grid(True)
plt.show()

def distr_exp(ex, size):
    x=[]
    for _ in range(size):
        x.append(-ex*math.log(random.random()))
    return x

# Test: generar 10.000 números con lambda = 1.5
datos_exponencial = distr_exp(1.5, n)

# Graficar histograma
plt.hist(datos_exponencial, bins=50, density=True, edgecolor='black')
plt.title('Distribución Exponencial λ = 1.5')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.grid(True)
plt.show()

def distr_gamma(k, a, size):
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

# Test: generar 10.000 números con alpha = 3, beta = 2
datos_gamma = distr_gamma(3, 2, n)

# Graficar histograma
plt.hist(datos_gamma, bins=50, density=True, edgecolor='black')
plt.title('Distribución Gamma α = 3, β = 2')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.grid(True)
plt.savefig('gamma.png')
plt.show()

def distr_normal(ex, stdx, size):
    x=[]
    for _ in range(size):
        sum=0
        for _ in range(12):
            sum=sum+random.random()
        x.append(stdx*(sum-6)+ex)
    return x

# Test: generar 10.000 números con media 0 y desviación 1
datos_normal = distr_normal(0, 1, n)

# Graficar histograma
plt.hist(datos_normal, bins=50, density=True, edgecolor='black')
plt.title('Distribución Normal N(0, 1)')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.grid(True)
plt.savefig('normal.png')
plt.show()


def distr_pascal(k, q, size=1): #en el libro esta como binomial negativa, es un caso especial de esa
    nx=[]
    for _ in range(size):
        tr = 1
        for _ in range(k):
            tr *= random.random()
        x = math.log(tr) // math.log(q)
        nx.append(x)
    return nx

def distr_binomial(n, p, size):
    x=[]
    for _ in range(size):
        y=0
        for _ in range(1, n):
            if((random.random()-p)<0):
                y+=1
        x.append(y)
    return x

# Test: 10000 muestras con n = 10, p = 0.3
datos_binomial = distr_binomial(10, 0.3, n)

# Histograma
plt.hist(datos_binomial, bins=range(0, 11), density=True, edgecolor='black', align='left')
plt.title('Distribución Binomial n=10, p=0.3')
plt.xlabel('Cantidad de éxitos')
plt.ylabel('Probabilidad')
plt.grid(True)
plt.savefig('binomial.png')
plt.show()

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

def distr_poisson(p, size): #p seria el lambda
    x=[]
    for _ in range(size):
        y=0
        tr=1
        b=0
        while(tr-b > 0):
            b=math.exp(p)
            tr *= random.random()
            if (tr - b >= 0):
                y+=1
        x.append(y)
    return x

# Test: generar 10.000 valores con lambda = 4
datos_poisson = distr_poisson(4, n)

# Histograma
plt.hist(datos_poisson, bins=range(0, max(datos_poisson)+1), density=True, edgecolor='black', align='left')
plt.title('Distribución Poisson λ = 4')
plt.xlabel('Número de eventos')
plt.ylabel('Probabilidad')
plt.grid(True)
plt.savefig('poisson.png')
plt.show()

def distr_empdiricadiscr(size=1): #empirica discreta
    x = []
    p = [0.273, 0.037, 0.195, 0.009, 0.124, 0.058, 0.062, 0.151, 0.047, 0.044] #tabla del libro
    for _ in range(size):
        a = 0
        z = 1
        for i in p:
            a += i
            if random.random() <= a:
                break
            else:
                z += 1
        x.append(z)
    return x
