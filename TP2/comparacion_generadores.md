- **Generador Congruencial Lineal (GCL)** 
- **Generador random.random()** 
---
##  Generador Congruencial Lineal (GCL)

### Parámetros utilizados:
- **Multiplicador (a)**: 1664525
- **Incremento (c)**: 1013904223
- **Módulo (m)**: 2³²
- **Semilla inicial**: 4343
- **Tamaño de muestra (n)**: 100000

###  Resultados:
- **Histograma**: Uniforme visualmente.
- **Coeficiente Pearson**: -0.002641 (sin correlación significativa).
- **Chi-cuadrado**: 8.9522, Valor p: 0.441698 (uniforme).
- **Test de corridas**: Z = 0.5675 (orden aleatorio validado).

###  Conclusión del GCL:
Muestra un comportamiento robusto, uniforme y aleatorio en todas las pruebas realizadas.

---

##  Generador random.random() (Python)

### Parámetros utilizados:
- **Algoritmo**: Mersenne Twister (implementación estándar en Python)
- **Tamaño de muestra (n)**: 100000

###  Resultados:
- **Histograma**: Uniforme visualmente.
- **Coeficiente Pearson**: 0.001605 (sin correlación significativa).
- **Chi-cuadrado**: 12.5154, Valor p: 0.185787 (uniforme).
- **Test de corridas**: Z = 0.5600 (orden aleatorio validado).

###  Conclusión de random.random():
Comportamiento altamente satisfactorio, uniforme y sin correlaciones notables. Es el estándar industrial de referencia.

---

## 🗃️ Comparativa General

| Prueba | Generador Congruencial Lineal (GCL) | random.random() (Python) |
|--------|-------------------------------------|---------------------------|
| **Histograma (Visual)** | ✅ Muy bueno | ✅ Muy bueno |
| **Coef. Pearson** | -0.002641 | 0.001605 |
| **Valor p Pearson** | 0.403674 | 0.611695 |
| **Chi-cuadrado** | 8.9522 | 12.5154 |
| **Valor p Chi-cuadrado** | 0.441698 | 0.185787 |
| **Z Test de Corridas** | 0.5675 | 0.5600 |

### 📌 Conclusión de la comparativa:
Ambos generadores mostraron resultados excelentes y muy similares. La leve diferencia numérica observada no tiene implicaciones prácticas relevantes y ambos son estadísticamente confiables para simulaciones generales. Esto valida nuestra implementación casera (GCL) como comparable en calidad al estándar de Python.

---

## Pendiente:

- hacer mas pruebas (Test de Poker, Test de Series, Test Kolmogorov-Smirnov).
- Comparar por lo menos con un tercer generador. Podriamos hacerlo con un generador que falle para mostrar uno no eficiente
- Documentar sensibilidad ante cambios de parámetros.