# Trabajo final del curso:
# “Manejo de datos en biología computacional. Herramientas de estadística”
Autora: Carolina Vacca

### 1 - Descripción del sistema

Mi tema de trabajo postdoctoral se concentra en entender cómo un sistema de dos componentes bacteriano (Two-Component System) presente en Sinorhizobium meliloti responde al estrés abiótico. Este microorganismo es una bacteria del suelo (rizobio)  que establece simbiosis con plantas leguminosas del género Medicago, Melilotus y Trigonella. La interacción entre S. meliloti y M. sativa (mejor conocida como alfalfa) es una interacción agronómica muy importante. Mediante esta interacción los rizobios son capaces de fijar nitrógeno atmosférico y transformarlo en variante de N reducidas, que son utilizables por las plantas. Sin embargo, muchas veces esta interacción se ve afectada por factores ambientales adversos como el estrés abiótico, es decir, estrés por extremos de pH, exceso de salinidad, por metales, entre otros.

En nuestro grupo de trabajo hace varios años que venimos estudiando el sistema ActJ-ActK, un TCS que responde al estrés ácido y por metales. ActJ codifica para un regulador transcripcional y ActK para una histidina quinasa. En conjunto, la quinasa detecta una señal, transfiere la información al regulador en forma de un grupo fosfato y éste último media la transcripción (activación o represión) de ciertos genes para dar lugar a una respuesta específica.

Con el fin de entender cómo funciona la vía de señalización mediada por ActJ y ActK y evaluar el fenotipo simbiótico de estos genes,, realizamos mutantes delecionales en ambos componentes del sistema y estimamos la fijación biológica de nitrógeno en simbiosis con plantas de dos especies distintas: Medicago truncatula y Medicago sativa.

### 2 - Diseño experimental

Se realizaron ensayos en plantas de Medicago truncatula y Medicago sativa y se inocularon con distintas cepas de S. meliloti: wt, actK1 y  actK2. También se realizó un control de plantas sin inocular. actK1 y actK2 son mutantes delecionales en la histidina quinasa. actK1 es un mutante que interrumpe un small RNA, mientras que actK2 lo mantiene intacto. 


### 3 - Organización de los datos

Los datos resultantes de este ensayo para evaluar la eficiencia simbiótica se encuentran representados en una tabla:

Variables categóricas: 
- Especie de planta utilizada: Medicago truncatula o Medicago sativa.
- Tratamiento: wt, actK1, actK2, control sin inocular

Variable aleatoria continua:
- Peso seco de fracción area de cada planta, para cada condición de tratamiento y especie de planta utilizada, medido como mg/planta.
Aclaración: el peso seco de la fracción área de una planta permite estimar la fijación biológica de nitrógeno (FBN). Cuanto mayor es el peso seco, mayor será la FBN.

### 4 - Descripción de los datos

Para observar cómo se distribuyen los datos de peso seco obtenidos para la inoculación de distintas especies de plantas con distintas cepas/tratamientos, se realizó el siguiente histograma (Figura 1). Como puede observarse en la figura, la distribución de los datos obtenidos no parece corresponderse con una distribución normal, tanto para los datos de peso seco obtenidos de Medicago truncatula como de Medicago sativa. Sin embargo, eso puede confirmarse con un test de normalidad y analizando la homocedasticidad.

![Figure_1-histograma-curva-por-especie](https://github.com/user-attachments/assets/024afd83-1240-4a18-922c-31f0c87a4a6a) 
### Figura 1

Por otro lado, también grafiqué como se distribuyen las frecuencias de cada Especie-Tratamiento:

![Figure_2-frecuencias-individuales](https://github.com/user-attachments/assets/5ef0a894-4dee-4950-8433-2b7ddadaed0e)
### Figura 2
En este caso, es posible visualizar cada set de datos Especie-Tratamiento, dado que al visualizar todas las frecuencias de peso seco para cada especie de planta, puede enmascararse otro tipo de distribución.

Además, calculé medidas resumen: de centralización (media, mediana, moda y percentiles) y de dispersión (varianza y desviación) para analizar los resultados por especie y tratamiento. 
Los resultados se muestran en la siguiente tabla:

```python
'''
       Especie Tratamiento  cantidad   media  mediana  moda     p25    p50     p75  varianza  desviacion_tipica
0      Msativa      actK1-        47  56.891    59.60  59.6  46.850  59.60  68.200   234.408             15.310
1      Msativa      actK2-        49  52.876    54.80  54.8  45.400  54.80  61.200   203.266             14.257
2      Msativa     control        46   8.046     7.90   8.9   6.950   7.90   8.900     3.124              1.768
3      Msativa          wt        48  52.935    51.00  47.3  40.475  51.00  64.075   303.022             17.408
4  Mtruncatula      actK1-        53  61.826    60.30  17.5  48.100  60.30  72.600   340.275             18.447
5  Mtruncatula      actK2-        46  48.943    47.65  31.4  39.150  47.65  58.325   190.581             13.805
6  Mtruncatula     control        52  19.152    18.00  13.0  13.650  18.00  23.550    37.261              6.104
7  Mtruncatula          wt        48  75.708    74.50  68.9  67.900  74.50  84.575   414.580             20.361
'''
```

Como puede observarse en la tabla, la media más baja para cada especie de planta utilizada corresponde al tratamiento control. Este control es el tratamiento sin inocular, es decir, sin bacterias capaces de fijar el nitrógeno atmosférico. Por lo tanto, es lógico que tengan menor peso seco por planta, dado que en ausencia de nitrógeno las plantas presentan menor crecimiento.

Por otro lado, las medidas de dispersión nos indican la representatividad de las medidas de dispersión y cuánto se desvían los datos de su valor central.
Para eso, calculé dentro de cada especie de planta cuáles eran los tratamientos que presentaban mayor desviación típica y varianza de la siguiente forma:

```python
mayores = medidas.loc[medidas.groupby('Especie')['varianza'].idxmax()].reset_index(drop=True)
print(mayores)
```

El resultado se muestra en la siguiente tabla:
```python
'''
       Especie Tratamiento  cantidad      media  mediana  moda     p25   p50     p75    varianza  desviacion_tipica
0      Msativa          wt        48  52.935417     51.0  47.3  40.475  51.0  64.075  303.022336          17.407537
1  Mtruncatula          wt        48  75.708333     74.5  68.9  67.900  74.5  84.575  414.580355          20.361246
'''
```

Se observa que el tratamiento con la cepa wt es el que mayor desviación típica y varianza presenta tanto en M. sativa como en M. truncatula.

### 5 - Coeficientes de asimetría y curtosis

Las medidas de dispersión calculadas previamente quedan expresadas en las unidades de la variable. Para solucionar este problema se definen medidas de dispersión relativas.
Por esta razón calculé el coeficiente de variación de Pearson, el coeficiente de asimetría de Fisher y el coeficiente de curtosis.

```python
Código:
medidas_especie = df.groupby('Especie')['peso-seco-mg'].agg(
    coef_variacion=lambda x: np.std(x, ddof=1) / np.mean(x),
    asimetria=lambda x: stats.skew(x, bias=False),
    curtosis=lambda x: stats.kurtosis(x, bias=False)
).reset_index()
print(medidas_especie.round(3))

'''
       Especie  coef_variacion  asimetria  curtosis
0      Msativa           0.560     -0.192    -0.986
1  Mtruncatula           0.514      0.412     0.096
'''
```
El grupo de datos de peso seco provenientes de M. sativa presenta asimetría negativa, esto significa que presenta una cola de datos ligeramente hacia la izquierda. Además, presenta curtosis ligeramente negativa, siendo en este caso una distribución platicúrtica.
A diferencia, los datos de peso seco de M. truncatula presentan asimetría positiva, esto significa que la cola de datos se encuentra ligeramente hacia la derecha. El coeficiente de curtosis presenta un valor cercano a cero, por lo que se trata de una distribución mesocúrtica.

### 6 - Estimación de intervalos de confianza

Se calcularon los intervalos sobre los cuales podamos establecer (con cierta probabilidad) que el parámetro poblacional se encuentra contenido mediante intervalos de confianza. Para ello, teniendo en cuenta que todos los tratamientos contenian más de 30 datos, se asumió distribución normal.

```python
Código:
# Intervalos de confianza por especie y tratamiento
# IC = media +- Z * (desviación tipica / raiz de n)
# IC = media +- Z * (error estandar)
# Z para 95% de confianza
Z = 1.96
# Error estándar y límites IC
medidas['error_estandar'] = medidas['desviacion_tipica'] / np.sqrt(medidas['cantidad'])
medidas['IC_inf'] = medidas['media'] - Z * medidas['error_estandar']
medidas['IC_sup'] = medidas['media'] + Z * medidas['error_estandar']
print("\nIntervalos de confianza por especie y tratamiento:")
print(medidas[['Especie', 'Tratamiento', 'cantidad', 'media', 'IC_inf', 'IC_sup']].round(3))

Resultado:
'''
Intervalos de confianza por especie y tratamiento:
       Especie Tratamiento  cantidad   media  IC_inf  IC_sup
0      Msativa      actK1-        47  56.891  52.514  61.269
1      Msativa      actK2-        49  52.876  48.884  56.868
2      Msativa     control        46   8.046   7.535   8.556
3      Msativa          wt        48  52.935  48.011  57.860
4  Mtruncatula      actK1-        53  61.826  56.860  66.793
5  Mtruncatula      actK2-        46  48.943  44.954  52.933
6  Mtruncatula     control        52  19.152  17.493  20.811
7  Mtruncatula          wt        48  75.708  69.948  81.469
'''
```

### 7 - Estimación del tamaño muestral

Aunque en este caso se conoce el n de cada tratamiento, al diseñar un experimento muchas veces es necesario tenerlo en cuenta previamente.
Para calcular el tamaño de la muestra se necesitan los siguientes parámetro:
- Nivel α (nivel alfa) (generalmente = 0.05)
- Potencia (normalmente 0,8)
- Tamaño del efecto (diferencia entre dos medias dividida por una desviación estándar)

Para calcular el tamaño del efecto, en primer lugar lo calculé para cada especie de plantas considerando que entre wt y el tratamiento control voy a encontrar la mayor diferencia.
```python
# Calcular desviación típica global por especie
medidas_especie = df.groupby('Especie')['peso-seco-mg'].agg(
    desviacion_tipica = lambda x: np.std(x, ddof=1)
).reset_index()

# Filtrar medias de wt y control, donde debería observarse la mayor diferencia
wt = medidas[medidas['Tratamiento'] == 'wt'].set_index('Especie')
control = medidas[medidas['Tratamiento'] == 'control'].set_index('Especie')
# Unir todo
merged = wt[['media']].join(
    control[['media']],
    lsuffix='_wt', rsuffix='_control'
).join(
    medidas_especie.set_index('Especie')
)
# Calcular tamaño del efecto estandarizado con SD global
merged['tamaño_efecto'] = (merged['media_control'] - merged['media_wt']) / merged['desviacion_tipica']
t_efecto_Msativa = merged.loc['Msativa', 'tamaño_efecto']
t_efecto_Mtruncatula = merged.loc['Mtruncatula', 'tamaño_efecto']
print(f"Tamaño de efecto Msativa: {t_efecto_Msativa:.3f}")
print(f"Tamaño de efecto Mtruncatula: {t_efecto_Mtruncatula:.3f}")
print(merged[['media_control', 'media_wt', 'desviacion_tipica', 'tamaño_efecto']].round(3))
analisis = TTestIndPower()
# Calcular n para Msativa
n_Msativa = int(analisis.solve_power(
    effect_size=t_efecto_Msativa,
    alpha=0.05,
    power=0.8,
    alternative='two-sided'
))
print(f"Tamaño de muestra por grupo para Msativa: {n_Msativa:.1f}") # Resultado 5
# Calcular n para Mtruncatula
n_Mtruncatula = int(analisis.solve_power(
    effect_size=t_efecto_Mtruncatula,
    alpha=0.05,
    power=0.8,
    alternative='two-sided'
))
print(f"Tamaño de muestra por grupo para Mtruncatula: {n_Mtruncatula:.1f}") # Resultado 4
```
Los resultados obtenidos fueron: n = 5 para M. sativa y n = 4 para M. truncatula. Sin embargo, en general, el control sin inocular se realiza para controlar que no haya contaminaciones en el experimento. Comunmente, lo que se busca evaluar (al menos en este experimento) es si existen diferencias en la inoculación/tratamiento con diferentes tipos de bacterias/cepas. Por esta razón, recalculé de forma análoga los tamaños de la muestra pero ahora comparando el tamaño del efecto para la comparación wt vs actK1 y wt vs actK2.

wt vs actK2 --> En este caso, como es de esperarse, se observa que dado que las medias son prácticamente iguales en M. sativa, el tamaño de la muestra debería ser infinitamente grande para detectar diferencias entre wt y actK2.
```python
'''
             media_actK2-  media_wt  desviacion_tipica  tamaño_efecto
Especie
Msativa            52.876    52.935             24.093         -0.002
Mtruncatula        48.943    75.708             26.219         -1.021
Tamaño de muestra por grupo para Msativa wt vs actK2-: 2539107.0
Tamaño de muestra por grupo para Mtruncatula wt vs actK2-: 16.0
'''
```
wt vs actK1 --> En este otro caso, para este mutante las medias son diferentes y el tamaño de la muestra debería ser cercano a 583 para detectar diferencias entre wt y actK1 en M. sativa, mientras que con 56 plantas bastaría para determinar diferencias entre wt y actK1 en M. truncatula. Esto se debe a que al ser mayor la diferencia detectada entre las medias de estas dos cepas en esta especie de plantas, menor cantidad de plantas se necesita para demostrarla.
```python
'''
             media_actK1-  media_wt  desviacion_tipica  tamaño_efecto
Especie
Msativa            56.891    52.935             24.093          0.164
Mtruncatula        61.826    75.708             26.219         -0.529
Tamaño de muestra por grupo para Msativa wt vs actK1-: 583.0
Tamaño de muestra por grupo para Mtruncatula wt vs actK1-: 56.0
'''
```

### 8 - Contraste de hipótesis
Si bien en la Figura 1 se puede observar que los datos tanto para M. sativa como para M. truncatula no parecen seguir una distribución normal, realizo un test para verificarlo.

**Test de normalidad:**
H0: los datos se distribuyen normalmente.
H1: los datos no se distribuyen normalmente.
```python
peso_seco = df['peso-seco-mg'].dropna() # Guardo datos globales de peso seco en una variable
print("El resultado del test de normalidad es: ", stats.normaltest(peso_seco, axis=0, nan_policy='propagate'))
```
El resultado del test de normalidad es:  NormaltestResult(statistic=np.float64(2.517611463908273), pvalue=np.float64(0.2839929878047395))
De este modo, no hay evidencia para afirmar que los datos globales, sin distinguir especie y tratamiento, se desvían de la normalidad y no es posible rechazar H0.

**Test de normalidad distinguiendo especie**
```python
=== Normalidad: Msativa ===
Estadístico = 31.988, p-valor = 0.0000
No se puede asumir normalidad (Msativa)

=== Normalidad: Mtruncatula ===
Estadístico = 5.733, p-valor = 0.0569
Se puede asumir normalidad (Mtruncatula)
```
Al realizar el test con los datos globales de peso seco, estos cumplen el test de normalidad. Es decir, no es posible rechazar H0. 
Sin embargo, al distinguir por especie se encuentra que para M. sativa no se puede asumir normalidad mientras que para M. truncatula sí.

**Test de normalidad para Especie-Tratamiento**
```python
Normalidad para Mtruncatula - wt:
  Estadístico = 16.705, p-valor = 0.0002
No se puede asumir normalidad

Normalidad para Mtruncatula - actK1-:
  Estadístico = 3.413, p-valor = 0.1815
Se puede asumir normalidad

Normalidad para Mtruncatula - actK2-:
  Estadístico = 1.730, p-valor = 0.4210
Se puede asumir normalidad

Normalidad para Mtruncatula - control:
  Estadístico = 3.221, p-valor = 0.1997
Se puede asumir normalidad

Normalidad para Msativa - wt:
  Estadístico = 4.118, p-valor = 0.1276
Se puede asumir normalidad

Normalidad para Msativa - actK1-:
  Estadístico = 1.740, p-valor = 0.4189
Se puede asumir normalidad

Normalidad para Msativa - actK2-:
  Estadístico = 0.140, p-valor = 0.9324
Se puede asumir normalidad

Normalidad para Msativa - control:
  Estadístico = 3.768, p-valor = 0.1520
Se puede asumir normalidad
```
Realizando el test para cada set de datos Especie-Tratamiento (La Figura 2 muestra los histogramas de frecuencia por separado), se encuentra que solo en un caso la distribución de datos no se puede asumir normal: M. truncatula - wt.

**Conclusiones:**
- A nivel global, la distribución del peso seco puede considerarse normal.
- Al separar por especie, existen diferencias: M. sativa no cumple normalidad, M. truncatula sí.
- Analizando Especie-Tratamiento, casi todos los set de datos cumplen normalidad, excepto M. truncatula - wt.

Test de Levene para comparar varianzas entre tratamientos dentro de cada especie de planta:

**Realizo el test de Levene para comparar varianzas entre tratamientos dentro de cada especie**

```python
Código:
for especie in df['Especie'].unique():
    subset = df[df['Especie'] == especie]
    grupos = [subset[subset['Tratamiento'] == t]['peso-seco-mg'].dropna()
              for t in subset['Tratamiento'].unique()]
    
    stat, p = levene(*grupos)
    
    print(f"\nEspecie: {especie}")
    print(f"Estadístico de Levene: {stat:.3f}")
    print(f"p-valor: {p:.4f}")
    
    if p < 0.05:
        print("No se cumple la igualdad de varianzas (varianzas desiguales).")
    else:
        print("Se cumple la igualdad de varianzas (homocedasticidad).")

# Resultado:
# Especie: Mtruncatula
# Estadístico de Levene: 9.414
# p-valor: 0.0000
# No se cumple la igualdad de varianzas (varianzas desiguales).

# Especie: Msativa
# Estadístico de Levene: 19.779
# p-valor: 0.0000
# No se cumple la igualdad de varianzas (varianzas desiguales).
```

**Prueba Welch**
Teniendo en cuenta que los datos para M. truncatula cumplen el test de normalidad pero cuentan con varianzas desiguales, realizo la Prueba de Welch para comparar entre dos tratamientos dentro de esta especie de plantas. Es una versión modificada de la prueba t de Student que se utiliza cuando los datos tienen varianzas desiguales o diferentes tamaños de muestra.

H0: Los tratamientos no difieren significativamente.
H1: Los tratamientos presentan presentan diferencias significativas.

```python
Código:
### Test de Welch - Modificación de t-test con varianzas desiguales
# Pares de comparación
comparaciones = [
    ('wt', 'actK1-'),
    ('wt', 'actK2-'),
    ('actK1-', 'actK2-')
]
# Especies a analizar: lo hago solo para M.truncatula porque los datos son normales pero con varianzas desiguales
especies = ['Mtruncatula']
# Recorrer especies y pares
for especie in especies:
    subset = df[df['Especie'] == especie]
    print(f"\n=== Welch t-tests para {especie} ===")
    for t1, t2 in comparaciones:
        grupo1 = subset[subset['Tratamiento'] == t1]['peso-seco-mg']
        grupo2 = subset[subset['Tratamiento'] == t2]['peso-seco-mg']
        stat, p = ttest_ind(grupo1, grupo2, equal_var=False)
        print(f"{t1} vs {t2}: t = {stat:.3f}, p = {p:.4f}")
        if p < 0.05:
            print(f"Diferencia significativa ({t1} vs {t2})")
        else:
            print(f"No hay diferencia significativa ({t1} vs {t2})")


# Resultados:
=== Welch t-tests para Mtruncatula ===
wt vs actK1-: t = 3.577, p = 0.0005
Diferencia significativa (wt vs actK1-)
wt vs actK2-: t = 7.487, p = 0.0000
Diferencia significativa (wt vs actK2-)
actK1- vs actK2-: t = 3.964, p = 0.0001
Diferencia significativa (actK1- vs actK2-)

```

Al realizar el test de Welch entre pares de tratamientos, se observa que los tratamientos en M. truncatula difieren significativamente y es posible rechazar H0 en todos los casos.

**Test de Kruskal-Wallis**
Por otro lado, dado que los datos para M. sativa no cumplen el supuesto de normalidad realizo en este caso un test no paramétrico: Test de Kruskal-Wallis.
Es una prueba no paramétrica que se utiliza para comparar la mediana de tres o más grupos independientes cuando los datos no siguen una distribución normal.

H0: Los tratamientos no presentan presentan diferencias significativas entre sí.
H1: Los tratamientos presentan presentan diferencias significativas entre sí.

```python
Código:
# Test de Kruskal-Wallis para M.sativa (comparación múltiple simultánea) - Test no paramétrico
print("\n=== Test de Kruskal-Wallis para Msativa ===")
df_msativa = df[df['Especie'] == 'Msativa']
# Extraer datos para los 3 tratamientos
grupo_wt = df_msativa[df_msativa['Tratamiento'] == 'wt']['peso-seco-mg'].dropna()
grupo_actK1 = df_msativa[df_msativa['Tratamiento'] == 'actK1-']['peso-seco-mg'].dropna()
grupo_actK2 = df_msativa[df_msativa['Tratamiento'] == 'actK2-']['peso-seco-mg'].dropna()
stat, p = kruskal(grupo_wt, grupo_actK1, grupo_actK2)
print(f"Kruskal-Wallis H = {stat:.3f}, p = {p:.4f}")
if p < 0.05:
    print("Hay diferencias significativas entre al menos dos grupos en Msativa")
else:
    print("No hay diferencias significativas entre los grupos en Msativa")

# Resultado:
=== Test de Kruskal-Wallis para Msativa ===
Kruskal-Wallis H = 2.774, p = 0.2498
No hay diferencias significativas entre los grupos en Msativa
```
Como puede observarse en los resultados, no hay diferencias significativas entre los tratamientos en M. sativa y no es posible rechazar H0.

### 9 - Comparación entre variables categóricas

Prueba de chi-cuadrado: Es una prueba estadística que se utiliza para evaluar la asociación entre dos variables categóricas. La prueba de chi-cuadrado compara la frecuencia observada en cada celda de la tabla de contingencia con la frecuencia esperada si no hubiera ninguna relación entre las variables. Si la diferencia entre la frecuencia observada y la esperada es grande, se concluye que hay una relación significativa entre las variables.

El test de Chi2 evalúa si hay dependencia entre las dos variables categóricas:
H0: Especie y Tratamiento son variables independientes.
H1: Existe una relación entre las variables Especie y Tratamiento.

```python
Código:
## Dependencia de variables categoricas
# Ejemplo: tabla de contingencia
tabla = pd.crosstab(df['Especie'], df['Tratamiento'])
print(tabla)
# Prueba de Chi-cuadrado
chi2, p, dof, expected = chi2_contingency(tabla)
print(f"Estadístico Chi2: {chi2:.3f}")
print(f"p-valor: {p:.4f}")
print(f"Grados de libertad: {dof}")
print("\nFrecuencias esperadas:")
print(expected)
if p < 0.05:
    print("Existe asociación significativa entre Especie y Tratamiento --> se rechaza H0")
else:
    print("No hay evidencia de dependencia entre Especie y Tratamiento --> no se rechaza H0")

# Resultado:
'''
Tratamiento  actK1-  actK2-  control  wt
Especie
Msativa          47      49       46  48
Mtruncatula      53      46       52  48
'''
# Estadístico Chi2: 0.614
# p-valor: 0.8932 --> > 0.05
# Grados de libertad: 3

# Frecuencias esperadas:
# [[48.84318766 46.40102828 47.86632391 46.88946015]
# [51.15681234 48.59897172 50.13367609 49.11053985]]
# No hay evidencia de dependencia entre Especie y Tratamiento --> no se rechaza H0
```

Esto significa que no hay evidencia estadística de que la frecuencia de tratamientos dependa de la especie. En otras palabras, la distribución de cepas es similar entre M. sativa y M. truncatula (en términos de cantidad de muestras por tratamiento).

### 10 - Análisis de correlación

Para llevar a cabo este análisis debería contar con otra variable aleatoria continua que haya sido evaluada en el experimento. Si bien en este caso no cuento con esos datos, sería interesante evaluar la cantidad de nódulos por planta y realizar un test de correlación para evaluar si la cantidad de nódulos correlaciona con mayor fijación biológica de nitrógeno. Esta evaluación resulta interesante porque más nódulos no implica necesariamente mayor FBN. De hecho, se han reportado casos de cepas que generan muchos nódulos en las raíces de M. truncatula o M. sativa pero que los mismos son ineficientes en la FBN.

  
