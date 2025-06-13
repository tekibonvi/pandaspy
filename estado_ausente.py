import pandas as pd
import sys
#ESTADOS AGENTES
report = sys.argv[1]
df = pd.read_csv(report, encoding='latin1', sep=';')

print(df.columns)

# Filtrar las filas donde la columna 'Ausente' no está vacía
ausencias = df[df['Ausente'] == 1]
#Falta restar 2700 segundos.
# Agrupar por 'Usuario: Nombre completo' y sumar la 'Duracion de Estado'
tiempo_ausente_por_usuario = ausencias.groupby('Usuario: Nombre completo')['Duración del estado'].sum().reset_index(name='Tiempo Total Ausente')
tiempo_ausente_por_usuario['Fecha'] = df['Fecha de creación'].iloc[0]
print(tiempo_ausente_por_usuario)
tiempo_ausente_por_usuario.to_clipboard(index=False, header=False)