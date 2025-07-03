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

### 4 - Descripción de los datos

Para observar cómo se distribuyen los datos de peso seco obtenidos para la inoculación de distintas especies de plantas con distintas cepas/tratamientos, se realizó el siguiente histograma (Figura 1). Como puede observarse en la figura, la distribución de los datos obtenidos no parece corresponderse con una distribución normal, tanto para los datos de peso seco obtenidos de Medicago truncatula como de Medicago sativa. Sin embargo, eso puede confirmarse con un test de normalidad y analizando la homocedasticidad.

![Figure_1-histograma-curva-por-especie](https://github.com/user-attachments/assets/024afd83-1240-4a18-922c-31f0c87a4a6a)


# Carga de datos a analizar
archivo = "datos-peso-seco.csv"
df = pd.read_csv(archivo, sep=";", decimal=",")
cat_cols = ["Especie", "Tratamiento"]
num_cols = [col for col in df.columns if col not in cat_cols]
print(df.head())
peso_seco = df['peso-seco-mg'].dropna()



