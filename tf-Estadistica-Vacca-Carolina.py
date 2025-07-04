## Trabajo final para el curso de estadística
# Importar librerias que se usarán en el programa
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.stats import levene
from scipy.stats import kruskal
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.power import TTestIndPower, tt_ind_solve_power

# Cargo el archivo con el que voy a trabajar
archivo = "datos-peso-seco.csv"
df = pd.read_csv(archivo, sep=";", decimal=",")
cat_cols = ["Especie", "Tratamiento"] # Defino variables categoricas
num_cols = [col for col in df.columns if col not in cat_cols] # Defino variable numérica
print(df.head()) # Visualizo primeras filas

# Histograma general por especie, para ver cómo se distribuyen los datos globales de cada una
plt.figure(figsize=(10, 6))
sns.histplot(
    data=df,
    x='peso-seco-mg',
    hue='Especie',
    bins=30,
    kde=True,
    edgecolor="black",
    alpha=0.5
)
plt.title('Distribución del peso seco por especie', fontsize=14)
plt.xlabel('Peso seco (mg/planta)', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Histograma por especie y tratamiento, para visualizar la distribución por tratamiento dentro de cada especie de planta
# FacetGrid divide automáticamente por especie y tratamiento)
g = sns.FacetGrid(
    df,
    row='Especie',
    col='Tratamiento',
    margin_titles=True,
    height=4
)
g.map(
    sns.histplot,
    'peso-seco-mg',
    bins=30,
    kde=True,
    color='skyblue',
    edgecolor='black'
)
g.set_axis_labels('Peso seco (mg/planta)', 'Frecuencia')
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle('Distribución de peso seco por especie y tratamiento')
plt.show()

# Calcular estadísticas por Especie y Tratamiento
medidas = df.groupby(['Especie', 'Tratamiento'])['peso-seco-mg'].agg(
    cantidad = 'count',
    media = 'mean',
    mediana = 'median',
    moda = lambda x: stats.mode(x, keepdims=False)[0],
    p25 = lambda x: np.percentile(x, 25),
    p50 = lambda x: np.percentile(x, 50),
    p75 = lambda x: np.percentile(x, 75),
    varianza = lambda x: np.var(x, ddof=1),   # ddof=1 para varianza muestral
    desviacion_tipica = lambda x: np.std(x, ddof=1)  # igual: desviación muestral
).reset_index()
print(medidas.round(3))

# Filtrar los tratamientos con mayor varianza y desviación por especie
mayores = medidas.loc[medidas.groupby('Especie')['varianza'].idxmax()].reset_index(drop=True)
print(mayores)

# Estadísticos por especie global (sin tener en cuenta el tratamiento)
medidas_especie = df.groupby('Especie')['peso-seco-mg'].agg(
    coef_variacion=lambda x: np.std(x, ddof=1) / np.mean(x),
    asimetria=lambda x: stats.skew(x, bias=False),
    curtosis=lambda x: stats.kurtosis(x, bias=False)
).reset_index()
print(medidas_especie.round(3))

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

# Determinación del tamaño de la muestra
# Para resultados continuos, el tamaño del efecto se expresa como la diferencia entre 
# dos medias dividida por una desviación estándar
# Calculo primero el tamaño del efecto

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

## Dado que la cantidad de muestras es muy baja, si bien la mayor diferencia 
# se detecta entre wt y control sin inocular, en realidad uno quiere comparar distintas
# cepas que se inoculan. Por ejemplo, distintos mutantes en relación con la cepa wt.
# Entonces, voy a repetir la estimación comparando wt vs un mutante, por ej. actK2

# Filtrar medias de wt y control, donde quiero detectar diferencias 
wt = medidas[medidas['Tratamiento'] == 'wt'].set_index('Especie')
actK2 = medidas[medidas['Tratamiento'] == 'actK2-'].set_index('Especie')

print(wt)
print(actK2)

# Unir todo
merged = wt[['media']].join(
    actK2[['media']],
    lsuffix='_wt', rsuffix='_actK2-'
).join(
    medidas_especie.set_index('Especie')
)

# Calcular tamaño del efecto estandarizado con SD global
merged['tamaño_efecto'] = (merged['media_actK2-'] - merged['media_wt']) / merged['desviacion_tipica']
t_efecto_Msativa = merged.loc['Msativa', 'tamaño_efecto']
t_efecto_Mtruncatula = merged.loc['Mtruncatula', 'tamaño_efecto']
print(f"Tamaño de efecto Msativa: {t_efecto_Msativa:.3f}")
print(f"Tamaño de efecto Mtruncatula: {t_efecto_Mtruncatula:.3f}")
print(merged[['media_actK2-', 'media_wt', 'desviacion_tipica', 'tamaño_efecto']].round(3))

# Calcular n para Msativa
n_Msativa = int(analisis.solve_power(
    effect_size=t_efecto_Msativa,
    alpha=0.05,
    power=0.8,
    alternative='two-sided'
))
print(f"Tamaño de muestra por grupo para Msativa wt vs actK2-: {n_Msativa:.1f}")
# 
# Calcular n para Mtruncatula
n_Mtruncatula = int(analisis.solve_power(
    effect_size=t_efecto_Mtruncatula,
    alpha=0.05,
    power=0.8,
    alternative='two-sided'
))
print(f"Tamaño de muestra por grupo para Mtruncatula wt vs actK2-: {n_Mtruncatula:.1f}")

## Para actK1
# Filtrar medias de wt y control, donde quiero detectar diferencias 
wt = medidas[medidas['Tratamiento'] == 'wt'].set_index('Especie')
actK1 = medidas[medidas['Tratamiento'] == 'actK1-'].set_index('Especie')
print(wt)
print(actK1)
# Unir todo
merged = wt[['media']].join(
    actK1[['media']],
    lsuffix='_wt', rsuffix='_actK1-'
).join(
    medidas_especie.set_index('Especie')
)

# Calcular tamaño del efecto estandarizado con SD global
merged['tamaño_efecto'] = (merged['media_actK1-'] - merged['media_wt']) / merged['desviacion_tipica']
t_efecto_Msativa = merged.loc['Msativa', 'tamaño_efecto']
t_efecto_Mtruncatula = merged.loc['Mtruncatula', 'tamaño_efecto']
print(f"Tamaño de efecto Msativa: {t_efecto_Msativa:.3f}")
print(f"Tamaño de efecto Mtruncatula: {t_efecto_Mtruncatula:.3f}")
print(merged[['media_actK1-', 'media_wt', 'desviacion_tipica', 'tamaño_efecto']].round(3))

# Calcular n para Msativa
n_Msativa = int(analisis.solve_power(
    effect_size=t_efecto_Msativa,
    alpha=0.05,
    power=0.8,
    alternative='two-sided'
))
print(f"Tamaño de muestra por grupo para Msativa wt vs actK1-: {n_Msativa:.1f}")
# 
# Calcular n para Mtruncatula
n_Mtruncatula = int(analisis.solve_power(
    effect_size=t_efecto_Mtruncatula,
    alpha=0.05,
    power=0.8,
    alternative='two-sided'
))
print(f"Tamaño de muestra por grupo para Mtruncatula wt vs actK1-: {n_Mtruncatula:.1f}")

## Contraste de hipótesis
# Si bien en la Figura 1 se puede observar que los datos tanto para M. sativa como para 
# M. truncatula no siguen una distribución normal, realizo un test para verificarlo.

#supuesto de normalidad. Test de normalidad.
# H0: los datos se distribuyen normalmente.
# H1:los datos no se distribuyen normalmente.

peso_seco = df['peso-seco-mg'].dropna()
stat_global, p_global = stats.normaltest(peso_seco, axis=0, nan_policy='propagate')
print("=== Normalidad: Global ===")
print(f"Estadístico = {stat_global:.3f}, p-valor = {p_global:.4f}")
if p_global < 0.05:
    print("No se puede asumir normalidad\n")
else:
    print("Se puede asumir normalidad\n")
# No hay evidencia para afirmar que los datos se desvían de la normalidad.
#
# Que pasa dentro de cada especie?
# Msativa (todos los datos)
msativa = df[df['Especie'] == 'Msativa']['peso-seco-mg'].dropna()
stat_msativa, p_msativa = stats.normaltest(msativa)
print("=== Normalidad: Msativa ===")
print(f"Estadístico = {stat_msativa:.3f}, p-valor = {p_msativa:.4f}")
if p_msativa < 0.05:
    print("No se puede asumir normalidad (Msativa)\n")
else:
    print("Se puede asumir normalidad (Msativa)\n")
# Mtruncatula (todos los datos)
mtruncatula = df[df['Especie'] == 'Mtruncatula']['peso-seco-mg'].dropna()
stat_mtruncatula, p_mtruncatula = stats.normaltest(mtruncatula)
print("=== Normalidad: Mtruncatula ===")
print(f"Estadístico = {stat_mtruncatula:.3f}, p-valor = {p_mtruncatula:.4f}")
if p_mtruncatula < 0.05:
    print("No se puede asumir normalidad (Mtruncatula)\n")
else:
    print("Se puede asumir normalidad (Mtruncatula)\n")
# Evaluando la combinación entre especie y tratamiento, recalculo el test de normalidad
for especie in df['Especie'].unique():
    for tratamiento in df['Tratamiento'].unique():
        # Subset de datos para ese grupo
        subset = df[
            (df['Especie'] == especie) & 
            (df['Tratamiento'] == tratamiento)
        ]['peso-seco-mg'].dropna()

        if len(subset) > 2:
            stat, p = stats.normaltest(subset)
            print(f"Normalidad para {especie} - {tratamiento}:")
            print(f"  Estadístico = {stat:.3f}, p-valor = {p:.4f}")

            if p < 0.05:
                print("No se puede asumir normalidad\n")
            else:
                print("Se puede asumir normalidad\n")
        else:
            print(f"Normalidad para {especie} - {tratamiento}: No se pudo calcular (n < 3)\n")
# Realizo el test de Levene para comparar varianzas entre tratamientos dentro de cada especie
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
# Dado que no se cumple la homocedasticidad de varianzas, realizo un test no paramétrico
# para comparar más de dos muestras. La comparación de medianas es posible para
# para datos no normales o con varianzas desiguales.
# De este modo, realicé una comparación para determinar si hay diferencias entre las cepas cuando son
# inoculadas en distintas especies de plantas
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
## Dependencia de variables categoricas
# Ejemplo: tabla de contingencia
print("\n=== Prueba de Chi2 para analizar dependencia de variables categóricas ===")
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