import random
import matplotlib as mp
import scipy.stats
import math

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

def distr_poisson(p, size=1): #p seria el lambda
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
