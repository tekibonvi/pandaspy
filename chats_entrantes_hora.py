import pandas as pd
import sys

report = sys.argv[1]
df = pd.read_csv(report, encoding='latin1', sep=';')

print(df.columns)
df = df[df['Usuario: Nombre completo'] != 'Platform Integration User']

# Convertir 'Fecha de solicitud' a datetime
df['Fecha de solicitud'] = pd.to_datetime(df['Fecha de solicitud'], errors='coerce')

# Extraer la hora de la columna 'Fecha de solicitud'
df['Hora de Solicitud'] = df['Fecha de solicitud'].dt.hour

# Agrupar por 'Propietario del caso' y 'Hora de Solicitud' y contar la cantidad de casos
casos_por_hora = df.groupby(['Hora de Solicitud']).size().reset_index(name='Cantidad de Casos')
casos_por_hora['Fecha'] = df['Fecha de la última modificación'].iloc[0]
print(casos_por_hora)
casos_por_hora.to_clipboard(index=False,header=False, decimal=',')
