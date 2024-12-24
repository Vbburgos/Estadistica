# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 15:38:50 2024

@author: foxbb
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import xlsxwriter
import numpy as np
from datetime import datetime  # Importar el módulo datetime

# Obtener la fecha y hora actual
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # Formatear fecha y hora

# Cargar los datos
df = pd.read_csv('/Users/foxbb/OneDrive/Documentos-LAPTOP-MGVPBMVU/VIU/1er Quatrimestre/01 GIIN ESTADÍSTICA/practica/datosPaisesDelMundo.csv')

# Verificar nombres de las columnas
print(df.columns)

# Añadir una columna de abreviaciones de países usando ISO 3166-1 alfa-2
country_abbr = {
    'Afganistán': 'AF', 'Åland, Islas': 'AX', 'Albania': 'AL', 'Alemania': 'DE',
	'Andorra': 'AD', 'Angola': 'AO', 'Anguila': 'AI', 'Antártida': 'AQ', 'Antigua y Barbuda': 'AG',
	'Arabia Saudita': 'SA', 'Argelia': 'DZ', 'Argentina': 'AR', 'Armenia': 'AM', 'Aruba': 'AW',
	'Australia': 'AU', 'Austria': 'AT', 'Azerbaiyán': 'AZ', 'Bahamas': 'BS', 'Bangladés': 'BD',
	'Barbados': 'BB', 'Baréin': 'BH', 'Bélgica': 'BE', 'Belice': 'BZ', 'Benín': 'BJ', 'Bermudas': 'BM',
	'Bielorrusia': 'BY', 'Bolivia': 'BO', 'Bonaire': 'BQ', 'Bosnia y Herzegovina': 'BA', 'Botsuana': 'BW',
	'Brasil': 'BR', 'Brunéi': 'BN', 'Bulgaria': 'BG', 'Burkina Faso': 'BF', 'Burundi': 'BI', 'Bután': 'BT',
	'Cabo Verde': 'CV', 'Camboya': 'KH', 'Camerún': 'CM', 'Canadá': 'CA', 'Catar': 'QA', 'Chad': 'TD', 'Chile': 'CL',
	'China': 'CN', 'Chipre': 'CY', 'Colombia': 'CO', 'Comoras': 'KM', 'Corea del Norte': 'KP', 'Corea del Sur': 'KR',
	'Costa de Marfil': 'CI', 'Costa Rica': 'CR', 'Croacia': 'HR', 'Cuba': 'CU', 'Curazao': 'CW', 'Dinamarca': 'DK',
	'Dominica': 'DM', 'Ecuador': 'EC', 'Egipto': 'EG', 'El Salvador': 'SV', 'Emiratos Árabes Unidos': 'AE', 'Eritrea': 'ER',
	'Eslovaquia': 'SK', 'Eslovenia': 'SI', 'España': 'ES', 'Estados Unidos': 'US', 'Estonia': 'EE', 'Etiopía': 'ET',
	'Filipinas': 'PH', 'Finlandia': 'FI', 'Fiyi': 'FJ', 'Francia': 'FR', 'Gabón': 'GA', 'Gambia': 'GM', 'Georgia': 'GE',
	'Ghana': 'GH', 'Gibraltar': 'GI', 'Granada': 'GD', 'Grecia': 'GR', 'Groenlandia': 'GL', 'Guadalupe': 'GP', 'Guam': 'GU',
	'Guatemala': 'GT', 'Guayana Francesa': 'GF', 'Guernsey': 'GG', 'Guinea': 'GN', 'Guinea-Bisáu': 'GW', 'Guinea Ecuatorial': 'GQ',
	'Guyana': 'GY', 'Haití': 'HT', 'Honduras': 'HN', 'Hong Kong': 'HK', 'Hungría': 'HU', 'India': 'IN', 'Indonesia': 'ID', 'Irak': 'IQ',
	'Irán': 'IR', 'Irlanda': 'IE', 'Isla Bouvet': 'BV', 'Isla de Man': 'IM', 'Isla de Navidad': 'CX', 'Islandia': 'IS', 'Islas Caimán': 'KY',
	'Islas Cocos': 'CC', 'Islas Cook': 'CK', 'Islas Feroe': 'FO', 'Islas Georgias del Sur y Sandwich': 'GS', 'Islas Heard y McDonald': 'HM',
	'Islas Malvinas': 'FK', 'Islas Marianas': 'MP', 'Islas Marshall': 'MH', 'Islas Pitcairn': 'PN', 'Islas Salomón': 'SB', 'Islas Turcas y Caicos': 'TC',
	'Islas ultramarinas USA': 'UM', 'Islas Vírgenes Británicas': 'VG', 'Islas Vírgenes USA': 'VI', 'Israel': 'IL', 'Italia': 'IT', 'Jamaica': 'JM',
	'Japón': 'JP', 'Jersey': 'JE', 'Jordania': 'JO', 'Kazajistán': 'KZ', 'Kenia': 'KE', 'Kirguistán': 'KG', 'Kiribati': 'KI', 'Kuwait': 'KW',
	'Laos': 'LA', 'Lesoto': 'LS', 'Letonia': 'LV', 'Líbano': 'LB', 'Liberia': 'LR', 'Libia': 'LY', 'Liechtenstein': 'LI', 'Lituania': 'LT', 'Luxemburgo': 'LU',
	'Macao': 'MO', 'Macedonia': 'MK', 'Madagascar': 'MG', 'Malasia': 'MY', 'Malaui': 'MW', 'Maldivas': 'MV', 'Malí': 'ML', 'Malta': 'MT', 'Marruecos': 'MA',
	'Martinica': 'MQ', 'Mauricio': 'MU', 'Mauritania': 'MR', 'Mayotte': 'YT', 'México': 'MX', 'Micronesia': 'FM', 'Moldavia)': 'MD', 'Mónaco': 'MC', 'Mongolia': 'MN',
	'Montenegro': 'ME', 'Montserrat': 'MS', 'Mozambique': 'MZ', 'Myanmar': 'MM', 'Namibia': 'NA', 'Nauru': 'NR', 'Nepal': 'NP', 'Nicaragua': 'NI', 'Níger': 'NE',
	'Nigeria': 'NG', 'Niue': 'NU', 'Norfolk': 'NF', 'Noruega': 'NO', 'Nueva Caledonia': 'NC', 'Nueva Zelanda': 'NZ', 'Omán': 'OM', 'Países Bajos': 'NL', 'Pakistán': 'PK',
	'Palaos': 'PW', 'Palestina': 'PS', 'Panamá': 'PA', 'Papúa Nueva Guinea': 'PG', 'Paraguay': 'PY', 'Perú': 'PE', 'Polinesia Francesa': 'PF', 'Polonia': 'PL', 'Portugal': 'PT',
	'Puerto Rico': 'PR', 'Reino Unido': 'GB', 'República Árabe Saharaui': 'EH', 'República Centroafricana': 'CF', 'República Checa': 'CZ', 'República del Congo': 'CG',
	'República Democrática del Congo': 'CD', 'República Dominicana': 'DO', 'Reunión': 'RE', 'Ruanda': 'RW', 'Rumania': 'RO', 'Rusia': 'RU', 'Samoa': 'WS', 'Samoa Americana': 'AS',
	'San Bartolomé': 'BL', 'San Cristóbal y Nieves': 'KN', 'San Marino': 'SM', 'San Martín': 'MF', 'San Pedro y Miquelón': 'PM', 'San Vicente y las Granadinas': 'VC',
	'Santa Elena, Ascensión y Tristán de Acuña': 'SH', 'Santa Lucía': 'LC', 'Santo Tomé y Príncipe': 'ST', 'Senegal': 'SN', 'Serbia': 'RS', 'Seychelles': 'SC', 'Sierra Leona': 'SL',
	'Singapur': 'SG', 'Sint Maarten': 'SX', 'Siria': 'SY', 'Somalia': 'SO', 'Sri Lanka': 'LK', 'Suazilandia': 'SZ', 'Sudáfrica': 'ZA', 'Sudán': 'SD', 'Sudán del Sur': 'SS',
	'Suecia': 'SE', 'Suiza': 'CH', 'Surinam': 'SR', 'Svalbard y Jan Mayen': 'SJ', 'Tailandia': 'TH', 'Taiwán': 'TW', 'Tanzania': 'TZ', 'Tayikistán': 'TJ',
	'Territorio Británico del Océano Índico': 'IO', 'Tierras Australes y Antárticas': 'TF', 'Timor Oriental': 'TL', 'Togo': 'TG', 'Tokelau': 'TK', 'Tonga': 'TO',
	'Trinidad y Tobago': 'TT', 'Túnez': 'TN', 'Turkmenistán': 'TM', 'Turquía': 'TR', 'Tuvalu': 'TV', 'Ucrania': 'UA', 'Uganda': 'UG', 'Uruguay': 'UY', 'Uzbekistán': 'UZ',
	'Vanuatu': 'VU', 'Vaticano': 'VA', 'Venezuela': 'VE', 'Vietnam': 'VN', 'Wallis y Futuna': 'WF', 'Yemen': 'YE', 'Yibuti': 'DJ', 'Zambia': 'ZM', 'Zimbabue': 'ZW'
    # Añadir más abreviaciones según sea necesario
}

df['Abreviacion'] = df['Pais'].map(country_abbr)

# Manejar valores NaN y infinitos
df = df.replace([float('inf'), float('-inf')], float('nan'))
df = df.dropna()

# Reiniciar índices después de la limpieza de datos
df = df.reset_index(drop=True)

# Crear un archivo de Excel con fecha y hora en el nombre
filename = f'resultados_{timestamp}.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
workbook = writer.book

# Análisis de correlación
correlation_matrix = df.corr()
plt.figure(figsize=(20, 16))  # Aumentar el tamaño de la figura
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)  # Ajustes de formato
plt.title('Matriz de Correlación')
plt.xticks(rotation=45, ha='right')  # Rotar etiquetas de las columnas para mejor legibilidad
plt.yticks(rotation=0)  # Mantener etiquetas de las filas horizontales
plt.tight_layout()  # Ajustar diseño para evitar que las etiquetas se corten
plt.savefig('correlacion.png')
plt.close()

# Guardar matriz de correlación en Excel
correlation_matrix.to_excel(writer, sheet_name='Correlacion')
worksheet = writer.sheets['Correlacion']
worksheet.insert_image('K1', 'correlacion.png')

# Análisis de regresión
X = df[['PIB_PerCapita', 'AccesoAguaMejorPobUrbana', 'TasaFertilidac_NacVivosMujer']]
y = df['CrecimientoPoblacion_TasaAnual']
X = X.dropna()
y = y.dropna()

reg = LinearRegression().fit(X, y)
reg_results = pd.DataFrame({
    'Variables': X.columns,
    'Coeficientes': reg.coef_
})
reg_results.to_excel(writer, sheet_name='Regresion', index=False)
worksheet = writer.sheets['Regresion']
worksheet.write('A10', f'Intercepto: {reg.intercept_}')

# Análisis de clusters
features = df[['Superficie_km2', 'Poblacion_Miles_2017', 'PIB_millonesUSD']]
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
kmeans = KMeans(n_clusters=5).fit(features_scaled)
df['Cluster'] = kmeans.labels_  # Asegurarse de que la columna 'Cluster' se haya creado

plt.figure(figsize=(16, 12))  # Aumentar el tamaño del gráfico
sns.scatterplot(data=df, x='PIB_millonesUSD', y='Poblacion_Miles_2017', hue='Cluster', palette='viridis')
for i, abbr in enumerate(df['Abreviacion']):
    plt.text(df['PIB_millonesUSD'][i], df['Poblacion_Miles_2017'][i], abbr, fontsize=9, alpha=0.7)
plt.title('Clustering de Países')
plt.tight_layout()  # Ajustar diseño
plt.savefig('clusters.png')
plt.close()

# Añadir lista de países usados para Clustering de Países
with open('clusters_paises.txt', 'w') as f:
    for pais in df['Pais']:
        f.write("%s\n" % pais)

# Guardar resultado de clustering en Excel
df[['Pais', 'Cluster']].to_excel(writer, sheet_name='Clusters', index=False)
worksheet = writer.sheets['Clusters']
worksheet.insert_image('D2', 'clusters.png')
worksheet.insert_textbox('D20', 'Clusters de Países:\n' + ', '.join(df['Pais'].tolist()))

# Estudio de desigualdad de género
plt.figure(figsize=(12, 8))  # Aumentar el tamaño de la figura
sns.boxplot(data=df, x='SexoProporcionMpor100F_2017.', y='EsperanzaVidaFem')
plt.title('Desigualdad de Género en Esperanza de Vida')
plt.xticks(rotation=45, ha='right')  # Rotar etiquetas de las columnas para mejor legibilidad
plt.tight_layout()  # Ajustar el diseño para evitar que las etiquetas se corten
plt.savefig('desigualdad_genero.png')
plt.close()

# Añadir lista de países usados para Desigualdad de Género
with open('desigualdad_genero_paises.txt', 'w') as f:
    for pais in df['Pais']:
        f.write("%s\n" % pais)

# Guardar resultado de desigualdad de género en Excel
worksheet = workbook.add_worksheet('Desigualdad Genero')
worksheet.insert_image('A1', 'desigualdad_genero.png')
worksheet.insert_textbox('A20', 'Países usados:\n' + ', '.join(df['Pais'].tolist()))

# Impacto del sector agrícola e industrial
plt.figure(figsize=(16, 12))  # Aumentar el tamaño del gráfico
sns.scatterplot(data=df, x='Empleados_PorcentajeAgricola', y='PIB_crecimientoAnual')
for i, abbr in enumerate(df['Abreviacion']):
    plt.text(df['Empleados_PorcentajeAgricola'][i], df['PIB_crecimientoAnual'][i], abbr, fontsize=9, alpha=0.7)
plt.title('Impacto del Sector Agrícola en el Crecimiento del PIB')
plt.tight_layout()  # Ajustar diseño
plt.savefig('sector_agricola.png')
plt.close()

# Añadir lista de países usados para Impacto del Sector Agrícola
with open('sector_agricola_paises.txt', 'w') as f:
    for pais in df['Pais']:
        f.write("%s\n" % pais)

plt.figure(figsize=(16, 12))  # Aumentar el tamaño del gráfico
sns.scatterplot(data=df, x='Empleados_PorcentajeIndustria', y='PIB_crecimientoAnual')
for i, abbr in enumerate(df['Abreviacion']):
    plt.text(df['Empleados_PorcentajeIndustria'][i], df['PIB_crecimientoAnual'][i], abbr, fontsize=9, alpha=0.7)
plt.title('Impacto del Sector Industrial en el Crecimiento del PIB')
plt.tight_layout()  # Ajustar diseño
plt.savefig('sector_industrial.png')
plt.close()

# Añadir lista de países usados para Impacto del Sector Industrial
with open('sector_industrial_paises.txt', 'w') as f:
    for pais in df['Pais']:
        f.write("%s\n" % pais)

# Guardar resultados de impacto de sectores en Excel
worksheet = workbook.add_worksheet('Impacto Sectores')
worksheet.insert_image('A1', 'sector_agricola.png')
worksheet.insert_textbox('A20', 'Países usados en sector agrícola:\n' + ', '.join(df['Pais'].tolist()))
worksheet.insert_image('A41', 'sector_industrial.png')
worksheet.insert_textbox('A60', 'Países usados en sector industrial:\n' + ', '.join(df['Pais'].tolist()))

# Estudios de salud pública
plt.figure(figsize=(16, 12))  # Aumentar el tamaño del gráfico
sns.scatterplot(data=df, x='GastoSalud_PIB', y='MortalidadInfantil_porMilNac')
for i, abbr in enumerate(df['Abreviacion']):
    plt.text(df['GastoSalud_PIB'][i], df['MortalidadInfantil_porMilNac'][i], abbr, fontsize=9, alpha=0.7)
plt.title('Gasto en Salud vs Mortalidad Infantil')
plt.tight_layout()  # Ajustar diseño
plt.savefig('salud_mortalidad.png')
plt.close()

# Añadir lista de países usados para Gasto en Salud vs Mortalidad Infantil
with open('salud_mortalidad_paises.txt', 'w') as f:
    for pais in df['Pais']:
        f.write("%s\n" % pais)

plt.figure(figsize=(16, 12))  # Aumentar el tamaño del gráfico
sns.scatterplot(data=df, x='medicos_porMilpoblacion', y='EsperanzaVidaFem')
for i, abbr in enumerate(df['Abreviacion']):
    plt.text(df['medicos_porMilpoblacion'][i], df['EsperanzaVidaFem'][i], abbr, fontsize=9, alpha=0.7)
plt.title('Médicos por Mil Habitantes vs Esperanza de Vida Femenina')
plt.tight_layout()  # Ajustar diseño
plt.savefig('medicos_esperanza.png')
plt.close()

# Añadir lista de países usados para Médicos por Mil Habitantes vs Esperanza de Vida Femenina
with open('medicos_esperanza_paises.txt', 'w') as f:
    for pais in df['Pais']:
        f.write("%s\n" % pais)

# Guardar resultados de salud pública en Excel
worksheet = workbook.add_worksheet('Salud Publica')
worksheet.insert_image('A1', 'salud_mortalidad.png')
worksheet.insert_textbox('A20', 'Países usados en salud y mortalidad:\n' + ', '.join(df['Pais'].tolist()))
worksheet.insert_image('A41', 'medicos_esperanza.png')
worksheet.insert_textbox('A60', 'Países usados en médicos por habitantes:\n' + ', '.join(df['Pais'].tolist()))

# Análisis Descriptivo
# Describiendo la Distribución de Variables
descriptive_stats = df.describe()
descriptive_stats.to_excel(writer, sheet_name='Descriptive Stats')

# Visualización de distribuciones (continuación)
variables_to_plot = ['PIB_PerCapita', 'EsperanzaVidaFem', 'EsperanzaVidaMasc', 'TasaFertilidac_NacVivosMujer']
for var in variables_to_plot:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[var], kde=True)
    plt.title(f'Distribución de {var}')
    plt.savefig(f'{var}_distribution.png')
    plt.close()
    worksheet = workbook.add_worksheet(f'{var[:20]} Dist')  # Asegurarse de que el nombre sea corto
    worksheet.insert_image('A1', f'{var}_distribution.png')
    worksheet.insert_textbox('A20', 'Países usados en distribución:\n' + ', '.join(df['Pais'].tolist()))

# Relación entre dos variables
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='PIB_PerCapita', y='EsperanzaVidaFem')
plt.title('Relación entre PIB per cápita y Esperanza de Vida Femenina')
plt.savefig('PIB_vs_EsperanzaVidaFem.png')
plt.close()
worksheet = workbook.add_worksheet('PIB_vs_EspVFem')
worksheet.insert_image('A1', 'PIB_vs_EsperanzaVidaFem.png')
worksheet.insert_textbox('A20', 'Países usados en relación PIB y esperanza de vida:\n' + ', '.join(df['Pais'].tolist()))

# Comparación de distribuciones con boxplots
variables_to_plot_boxplot = ['PIB_PerCapita', 'EsperanzaVidaFem', 'EsperanzaVidaMasc', 'TasaFertilidac_NacVivosMujer']
plt.figure(figsize=(12, 8))
df[variables_to_plot_boxplot].boxplot()
plt.title('Comparación de Distribuciones')
plt.savefig('comparacion_distribuciones.png')
plt.close()
worksheet = workbook.add_worksheet('ComparDistrib')
worksheet.insert_image('A1', 'comparacion_distribuciones.png')
worksheet.insert_textbox('A20', 'Países usados en comparación de distribuciones:\n' + ', '.join(df['Pais'].tolist()))

# Detección de Valores Atípicos
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))]
    return outliers

outliers = detect_outliers(df, 'PIB_PerCapita')
outliers.to_excel(writer, sheet_name='Outliers_PIB_PerCapita')

# Representación gráfica de outliers
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['PIB_PerCapita'])
plt.title('Detección de Valores Atípicos en PIB per cápita')
plt.savefig('outliers_PIB_PerCapita.png')
plt.close()
worksheet = workbook.add_worksheet('Outliers_PIB')
worksheet.insert_image('A1', 'outliers_PIB_PerCapita.png')
worksheet.insert_textbox('A20', 'Países usados en detección de outliers:\n' + ', '.join(df['Pais'].tolist()))

# Guardar y cerrar el archivo de Excel
writer.save()
print(f"Resultados guardados en '{filename}'")
