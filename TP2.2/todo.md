# Lista de cosas para hacer
**Imporante**: Sacar todo el material de libro que dejaron en el classroom junto con el tp (las pruebas y eso si las podemos hacer aparte creo)
## Generadores
- ~~Realizar generador de valores para cada distribucion~~
    - uniforme
    - exponencial
    - gamma
    - normal
    - pascal
    - binomial
    - hipergeometrica
    - poisson
    - empirica discreta

Tengo entendido que no podemos utilizar los generadores directos, sino mediante una formula o funcion definida (o sea, no podemos usar numpy.random.gamma())
Esta todo en el libro que pusieron en el classroom (formulas y diagramas para hacer el codigo)

## Pruebas
- ~~Realizar una prueba a eleccion (diria chi cuadrado, pero vemos) de cada generador~~
- ~~Realizar histograma o grafico de frecuencia de valores~~

## Informe
- Desarrollo teorico (con formulas) de cada generador
- Metodo de transformada inversa para los que aplica segun la tabla del informe (uniforme, exponencial y normal)
- Metodo del rechazo (esta en el libro pero realmente no lo entiendo)

## Resultados obtenidos (correspondiente a los graficos)
### Normal
Chi²: 3.5280540761665593
p-valor: 0.9396482681759648
Grados de libertad: 7
Valor crítico (chi²): 14.067140449340167
✅ No se rechaza la hipótesis nula

### Emp discreta
Distribución: Empírica Discreta
Chi²: 7.088461374514992
p-valor: 0.6279096813784573
Grados de libertad: 9
Valor crítico: 16.918977604620448
✅

### Binomial
Distribución: Binomial
Chi²: 330.25931568599185
p-valor: 9.796950171190533e-66
Grados de libertad: 8
Valor crítico: 15.507313055865453
❌

### Uniforme
Distribución: Uniforme
Chi²: 1.468
p-valor: 0.9973772729633104
Grados de libertad: 9
Valor crítico: 16.918977604620448
✅

### Poisson
Distribución: Poisson
Chi²: 75.78482258000355
p-valor: 0.008373412177736208
Grados de libertad: 48
Valor crítico: 65.17076890356982
❌

### Exponencial
Distribución: Exponencial
Chi²: 7.306896902371877
p-valor: 0.6052003997670417
Grados de libertad: 8
Valor crítico: 15.507313055865453
✅