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

Se calcularon los intervalos sobre los cuales que podamos establecer (con cierta probabilidad) que el parámetro poblacional se encuentra contenido mediante intervalos de confianza. Para ello, teniendo en cuenta que todos los tratamientos contenian más de 30 datos, se asumió distribución normal.

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
```
