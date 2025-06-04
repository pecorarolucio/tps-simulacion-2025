
import random
import numpy as np

# ---------------- CONFIGURACIÓN ----------------

XXX = 100       # Número de tiradas por corrida
YYY = 1000      # Número de corridas
a = "f"         # Tipo de capital: "f" (finito) o "i" (infinito)
cfi = 100       # Capital inicial
ci = "R"        # Color inicial: "R", "N", "V" o "Auto"

# ---------------- FUNCIONES BASE ----------------

chosen_colors = []

def tipocapital(a):
    if a == "i":
        return float('inf')
    else:
        return cfi

def jugar(apuesta):
    na = random.randint(0, 36)
    color_na = ""
    color_n = ""
    if (1 <= na <= 10) or (19 <= na <= 28):
        color_na = "R"
    elif na == 0:
        color_na = "V"
    else:
        color_na = "N"
    chosen_colors.append(color_na)

    global ci
    if ci in ["R", "V", "N"]:
        color_n = ci
    else:
        if chosen_colors:
            counts = {color: chosen_colors.count(color) for color in {"R", "V", "N"}}
            color_n = max(counts, key=counts.get)
        else:
            color_n = "R"
    return color_n == color_na

def jugar_par_impar(apuesta, apuesta_a="par"):
    numero = random.randint(0, 36)
    if numero == 0:
        return False
    if apuesta_a == "par":
        return numero % 2 == 0
    elif apuesta_a == "impar":
        return numero % 2 == 1
    else:
        raise ValueError("Apuesta inválida")

# ---------------- MARTINGALA (por COLOR) ----------------

def martingala_jugada_color(jugada_objetivo):
    p = tipocapital(a)
    apuesta = 1
    resultado_jugada = None
    for r in range(1, XXX + 1):
        resultado = jugar(apuesta)
        if r == jugada_objetivo:
            resultado_jugada = resultado
            break
        if resultado:
            p += apuesta
            apuesta = 1
        else:
            p -= apuesta
            apuesta *= 2
    return resultado_jugada

# ---------------- MARTINGALA (por PAR/IMPAR) ----------------

def martingala_jugada_par_impar(jugada_objetivo, apuesta_a="par"):
    p = tipocapital(a)
    apuesta = 1
    resultado_jugada = None
    for r in range(1, XXX + 1):
        resultado = jugar_par_impar(apuesta, apuesta_a)
        if r == jugada_objetivo:
            resultado_jugada = resultado
            break
        if resultado:
            p += apuesta
            apuesta = 1
        else:
            p -= apuesta
            apuesta *= 2
    return resultado_jugada

# ---------------- EJECUCIÓN ----------------

def correr_experimento(modo="color", jugada=10, par_impar=None):
    victorias = 0
    global chosen_colors
    for _ in range(YYY):
        chosen_colors = []
        if modo == "color":
            if martingala_jugada_color(jugada):
                victorias += 1
        elif modo == "par_impar":
            if martingala_jugada_par_impar(jugada, apuesta_a=par_impar):
                victorias += 1
    return victorias / YYY

# -------------- RESULTADOS --------------------

# 1. Martingala por color en jugada 10
frecuencia_color = correr_experimento(modo="color", jugada=10)
print(f"[COLOR] Frecuencia relativa de victoria en jugada 10: {frecuencia_color:.4f}")

# 2. Martingala por par en jugada 10
frecuencia_par = correr_experimento(modo="par_impar", jugada=10, par_impar="par")
print(f"[PAR] Frecuencia relativa de victoria en jugada 10: {frecuencia_par:.4f}")

# 3. Martingala por impar en jugada 10
frecuencia_impar = correr_experimento(modo="par_impar", jugada=10, par_impar="impar")
print(f"[IMPAR] Frecuencia relativa de victoria en jugada 10: {frecuencia_impar:.4f}")
