import pandas as pd
import sys

# 1. Cargar el CSV
report = sys.argv[1]
df = pd.read_csv(report, encoding='latin1', sep=';')

# Convertir 'Fecha de apertura' a formato de fecha
# Usamos errors='coerce' para que si hay algún valor que no pueda convertir, ponga NaT (Not a Time)
df['Fecha de apertura'] = pd.to_datetime(df['Fecha de apertura'], format='%d/%m/%Y', errors='coerce')

# Eliminar números de casos duplicados (manteniendo la primera ocurrencia)
# Mantengo esta línea porque puede ser útil, pero para lo que pedís, el filtro por fecha es lo principal.
df_sin_duplicados = df.drop_duplicates(subset=['Número del caso', 'Modificado por'], keep='first')
print(f"Cantidad de casos sin duplicados: {len(df_sin_duplicados)}")

# Encontrar la fecha de apertura más reciente en todo el dataset
fecha_apertura_maxima = df['Fecha de apertura'].max()
print(f"\nLa fecha de apertura más reciente en el dataset es: {fecha_apertura_maxima.strftime('%d/%m/%Y')}")

# Filtrar los casos creados en el último día (usando la fecha de apertura máxima)
casos_ultimo_dia = df[df['Fecha de apertura'] == fecha_apertura_maxima].copy()
casos_ultimo_dia = df_sin_duplicados[df_sin_duplicados['Fecha de apertura'] == fecha_apertura_maxima].copy()

print(len(df))
print(len(df_sin_duplicados))
print(len(casos_ultimo_dia))
# Opcional: Si querés ver cuántos casos se abrieron ese día
print(f"Cantidad de casos abiertos en el último día ({fecha_apertura_maxima.strftime('%d/%m/%Y')}): {len(casos_ultimo_dia)}")


cantidad_casos_por_tipo_ultimo_dia = casos_ultimo_dia.groupby('Origen del caso')['Número del caso'].count().reset_index(name='Cantidad de Casos')

# Añadir la fecha de la apertura máxima a este resultado
cantidad_casos_por_tipo_ultimo_dia['Fecha'] = fecha_apertura_maxima.strftime('%d/%m/%Y')

print("\nCasos creados en el último día (agrupados por Tipo de registro del caso):")
print(cantidad_casos_por_tipo_ultimo_dia)

# Copiar el resultado al portapapeles
cantidad_casos_por_tipo_ultimo_dia.to_clipboard(index=False, header=False, decimal=',') 

print("\n¡Listo! Los casos del último día (agrupados por tipo) fueron copiados al portapapeles.")