import random
import matplotlib.pyplot as plt

# Generamos una lista de 10.000 números entre 0 y 1
numeros = [random.random() for _ in range(10000)]

# Creamos un histograma
plt.hist(numeros, bins=50, edgecolor='black')
plt.title("Distribución de números pseudoaleatorios")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.show()
