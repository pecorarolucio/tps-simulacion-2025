
import random

# Configuración
N = 1000
capital_inicial = 10000000
ci = "N"  # Se apuesta a negro
color_esperado = "R"
contador_victorias_jugada_9 = 0
contador_victorias_total = 0

# Función para convertir número a color
def numero_a_color(numero):
    if numero == 0:
        return 'V'
    elif (1 <= numero <= 10) or (19 <= numero <= 28):
        return 'R'
    else:
        return 'N'

# Simular una corrida con Martingala y detectar victoria en jugada 9
p = capital_inicial
apuesta = 1
colores = []
for i in range(N):
    numero = random.randint(0, 36)
    color = numero_a_color(numero)
    colores.append(color)
    gano = color == ci
    if gano:
        p += apuesta
        apuesta = 1
    else:
        p -= apuesta
        apuesta *= 2

    if gano:
        contador_victorias_total += 1
        if i >= 4 and colores[i-3:i] == ['N'] * 3 and color == 'R':
            contador_victorias_jugada_9 += 1

# Resultado
if contador_victorias_total > 0:
    frecuencia = contador_victorias_jugada_9 / contador_victorias_total
else:
    frecuencia = 0.0

print(f"Victorias totales: {contador_victorias_total}")
print(f"Victorias en jugada 9 (8N seguidos + R): {contador_victorias_jugada_9}")
print(f"Frecuencia relativa: {frecuencia:.6f}")
