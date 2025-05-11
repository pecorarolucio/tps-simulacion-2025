
# Avances hasta ahora - 06/05

## 🔧 Parámetros utilizados del GCL

- **Fórmula:** Xₙ₊₁ = (a · Xₙ + c) mod m
- **Normalización:** Uₙ = Xₙ / m
- **Parámetros usados:**
  - a = 1664525
  - c = 1013904223
  - m = 2³²
  - semilla = 42

---

## ✅ Pruebas realizadas

### 1. Histograma de 10.000 valores
- Se generó un histograma de los valores Uₙ ∈ [0,1).
- **Resultado:** Distribución visualmente uniforme, sin acumulaciones ni vacíos notorios.

### 2. Correlación entre valores consecutivos (Uₙ vs Uₙ₊₁)
- Se generó un gráfico de dispersión 2D.
- **Resultado:** Nube homogénea de puntos. Coeficiente de Pearson cercano a 0 (~ -0.0099).
- **Conclusión:** No hay correlación lineal significativa.

### 3. Dispersión 3D: (Uₙ, Uₙ₊₁, Uₙ₊₂)
- Se graficó en 3D para detectar alineamientos en hiperplanos (Marsaglia).
- **Resultado:** Cubo 3D denso y bien distribuido, sin patrones visibles.
- **Conclusión:** No se detecta estructura reticular a simple vista.

### 4. Test de Frecuencia (Chi-cuadrado)
- Se dividió el intervalo [0,1) en 10 subintervalos.
Para GLC (n=100000):
Los resultados del test de chi-cuadrado indican que no hay una diferencia significativa entre las frecuencias observadas y las esperadas. Dado que el valor p es alto 0.8753, no se rechaza la hipótesis nula, lo que sugiere que los datos siguen una distribución uniforme y no presentan patrones anómalos

Para random(n=100000):
Los resultados del test de chi-cuadrado muestran que la diferencia entre las frecuencias observadas y esperadas no es estadísticamente significativa. Con un valor p de 0.5249, mayor que 0.05, no se rechaza la hipótesis nula, lo que indica que los datos pueden considerarse aleatorios y seguir una distribución uniforme sin evidencia de patrones estructurados

Para RANDU(n=100000):
Los resultados del test de chi-cuadrado indican que no hay evidencia estadística suficiente para rechazar la hipótesis de que los datos generados por RANDU siguen una distribución uniforme (p = 0.235309). Sin embargo, este test por sí solo no garantiza que los valores sean realmente aleatorios, ya que solo evalúa la distribución de frecuencias.
Dado que RANDU es un generador conocido por su fuerte correlación interna, los gráficos de dispersión y 3D revelan su mayor debilidad: los valores no están distribuidos de manera uniforme, sino que forman patrones estructurados, lo que confirma que RANDU no es adecuado para simulaciones aleatorias confiables.


### 5. Test de corridas (sobre y bajo la media)
Para GLC: 
- Z = -0.93, p=0.34. (**aceptable y esperado**)
- La cantidad de corridas coincide con las esperadas
- **Conclusion** El GLC supera el test de corridas y se considera aleatorio en ese sentido.

Para random:
- Z = 0.16, p=0.86 (**aceptable y esperado**)
- La cantidad de corridas coincide con las esperadas
- **Conclusion** La generacion de valores aleatorios de random supera el test de corridas y se considera aleatorio en ese sentido


## 📌 Próximos pasos

- Aplicar **otros tests estadísticos** clásicos:
  - ~~Corridas~~
  - ~~Poker~~
  - ~~Series~~
- Comparar contra `random.random()` de Python y otros generadores clásicos como **RANDU**.
- Registrar resultados y visualizaciones para el informe.
- Realizar conclusiones de test de poker y series

