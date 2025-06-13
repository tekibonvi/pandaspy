import pandas as pd
import sys
#OMNICHANNELREPORT
# 1. Cargar el CSV
report = sys.argv[1]
df = pd.read_csv(report, encoding='latin1', sep=';')

# Convertir 'Fecha de aceptación' a datetime, especificando el formato
df['Fecha de aceptación'] = pd.to_datetime(df['Fecha de aceptación'], format='%d/%m/%Y, %H:%M', errors='coerce')

# Extraer la fecha y formatearla como dd/mm/aaaa
df['Fecha'] = df['Fecha de aceptación'].dt.strftime('%d/%m/%Y')

# Convertir 'tmo agente' a numérico, reemplazando ',' por '.' y manejando errores
df['tmo agente'] = pd.to_numeric(df['tmo agente'].str.replace(',', '.'), errors='coerce')

# Calcular la media de 'Velocidad para responder' por agente
velocidad_respuesta_media = df.groupby('Creado por: Nombre completo')['Velocidad para responder'].mean().reset_index(name='Velocidad para responder media')
velocidad_respuesta_media['Velocidad para responder media'] = velocidad_respuesta_media['Velocidad para responder media'].apply(lambda x: str(x).replace('.', ','))
print(velocidad_respuesta_media['Velocidad para responder media'])
# Calcular la media de 'tmo agente' por agente
tmo_agente_medio = df.groupby('Creado por: Nombre completo')['tmo agente'].mean().reset_index(name='Media tmo agente')
tmo_agente_medio = df.groupby('Creado por: Nombre completo')['tmo agente'].mean().reset_index(name='Media tmo agente')
tmo_agente_medio['Media tmo agente (segundos)'] = (tmo_agente_medio['Media tmo agente'] * 60).apply(lambda x: f'{x:.2f}')
tmo_agente_medio = tmo_agente_medio.drop(columns=['Media tmo agente'])
tmo_agente_medio = tmo_agente_medio.rename(columns={'Media tmo agente (segundos)': 'Media tmo agente'})
tmo_agente_medio['Media tmo agente'] = tmo_agente_medio['Media tmo agente'].apply(lambda x: str(x).replace('.', ','))

# Calcular la suma de 'Tiempo activo' por agente
tiempo_activo_total = df.groupby('Creado por: Nombre completo')['Tiempo activo'].sum().reset_index(name='Tiempo activo')
tiempo_activo_total['Tiempo activo'] = tiempo_activo_total['Tiempo activo'].apply(lambda x: str(x).replace('.', ','))

# Calcular la suma de 'Tiempo tratado' por agente
tiempo_tratado_total = df.groupby('Creado por: Nombre completo')['Tiempo tratado'].sum().reset_index(name='Tiempo tratado')
tiempo_tratado_total['Tiempo tratado'] = tiempo_tratado_total['Tiempo tratado'].apply(lambda x: str(x).replace('.', ','))

# Calcular la cantidad de casos tratados por agente (conteo único de 'Elemento de trabajo: Nombre')
cantidad_casos_tratados = df.groupby('Creado por: Nombre completo')['Elemento de trabajo: Nombre'].nunique().reset_index(name='Cantidad de casos tratados')

# Fusionar los resultados en un solo DataFrame
informe_agentes = pd.merge(velocidad_respuesta_media, tmo_agente_medio, on='Creado por: Nombre completo', how='outer')
informe_agentes = pd.merge(informe_agentes, tiempo_activo_total, on='Creado por: Nombre completo', how='outer')
informe_agentes = pd.merge(informe_agentes, tiempo_tratado_total, on='Creado por: Nombre completo', how='outer')
informe_agentes = pd.merge(informe_agentes, cantidad_casos_tratados, on='Creado por: Nombre completo', how='outer').fillna(0)

# Renombrar la columna del agente
informe_agentes = informe_agentes.rename(columns={'Creado por: Nombre completo': 'Agente'})

# Agregar la columna 'Fecha' al final
informe_agentes['Fecha'] = df['Fecha'].iloc[0]

print(informe_agentes)
informe_agentes.to_clipboard(index=False,header=False, decimal=',')