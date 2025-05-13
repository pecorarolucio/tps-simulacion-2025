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

| Prueba | Generador Congruencial Lineal (GCL) | random.random() (Python) | RANDU (GCL) | XORShift 32 bits
|--------|-------------------------------------|---------------------------|
| **Histograma (Visual)** | ✅ Muy bueno | ✅ Muy bueno | - | ✅ Muy bueno
| **Coef. Pearson** | 0.002425 | -0.000963 | 0.000793 | 0.002425
| **Valor p Pearson** | 0.403674 | 0.611695 | 0.801906 | 0.443153
| **Chi-cuadrado** | 8.9522 | 12.5154 | - | 4.5030
| **Valor p Chi-cuadrado** | 0.441698 | 0.185787 | - | 0.875307
| **Z Test de Corridas** | 0.5675 | 0.5600 |
| **Test de Poker** | 0.4002 | 0.7814 | - | 0.4027

### 📌 Conclusión de la comparativa:
Ambos generadores mostraron resultados excelentes y muy similares. La leve diferencia numérica observada no tiene implicaciones prácticas relevantes y ambos son estadísticamente confiables para simulaciones generales. Esto valida nuestra implementación casera (GCL) como comparable en calidad al estándar de Python.

Con RANDU, vas a notar gráficamente que:
- Los puntos se alinean en líneas paralelas (en 2D).
- El gráfico 3D revela que los números generados por RANDU no son independientes en múltiples dimensiones. En lugar de ocupar el espacio tridimensional de manera uniforme, los puntos se agrupan en planos paralelos, lo que es un signo claro de correlación. Esto invalida su uso en simulaciones o algoritmos donde la aleatoriedad genuina es crítica.
- Si usás un gráfico 3D de tríadas (r[i], r[i+1], r[i+2]), los puntos caen en unos pocos planos.
Este patrón demuestra que RANDU no tiene independencia entre valores consecutivos, lo que lo hace predecible y no aleatorio, lo cual es inaceptable en simulaciones serias.
- El histograma nos muestra fluctuaciones en la frecuencia de ciertos valores, lo que sugiere que no todos los números tienen la misma probabilidad de ocurrencia.

XORShift 32 bits: 
- es rápido y simple, con distribución aceptable, pero muestra dependencias estadísticas.
- apto para usos informales o simulaciones livianas, pero no para aplicaciones que requieren alta aleatoriedad o criptografía.
- El período es bueno
- genera números aparentemente uniformes en [0, 1] si se normalizan correctamente. Sin embargo, estudios muestran que ciertas correlaciones pueden aparecer si se usan muchos bits directamente (por ejemplo, los bits menos significativos son más predecibles).
📌 Solución común: descartar algunos bits o aplicar un hash/mix post-proceso si querés mejorar su aleatoriedad
- Tiene autocorrelación baja, lo cual es bueno. Pero no es completamente libre de patrones si generás muchos valores en serie.
- ✅ ¿Cuándo conviene usar XORShift?
    En simulaciones ligeras donde la rapidez importa más que la calidad absoluta.
    Para videojuegos, pruebas rápidas, generación de IDs temporales.
    No se recomienda para criptografía, sorteos serios, juegos de azar reales o ciencia estadística rigurosa.

---

## Pendiente:

- hacer mas pruebas (Test de Series, Test Kolmogorov-Smirnov).
- Comparar por lo menos con un tercer generador. Podriamos hacerlo con un generador que falle para mostrar uno no eficiente
- Documentar sensibilidad ante cambios de parámetros.