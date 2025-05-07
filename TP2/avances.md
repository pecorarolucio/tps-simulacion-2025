
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
- Para n = 10.000 → p = 0.032 (ligeramente sospechoso).
- Para n = 100.000 → p = 0.44 (resultado **aceptable y esperado**).
- **Conclusión:** El GCL genera valores con distribución uniforme estadísticamente válida en muestras grandes.

---

## 📌 Próximos pasos

- Aplicar **otros tests estadísticos** clásicos:
  - Corridas
  - Poker
  - Series
- Comparar contra `random.random()` de Python y otros generadores clásicos como **RANDU**.
- Registrar resultados y visualizaciones para el informe.

