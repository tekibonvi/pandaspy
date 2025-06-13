import pandas as pd
import sys
#HISTORIAL DE CASO
report = sys.argv[1]
df = pd.read_csv(report, encoding='latin1', sep=';')

print(df.columns)

# 1 - Eliminar números de casos duplicados modificados por la misma persona
df_sin_duplicados = df.drop_duplicates(subset=['Número del caso', 'Modificado por'], keep='first')

# 2 - Calcular cantidad de casos cerrados por persona / cantidad de casos que modificó

# Filtrar casos cerrados
casos_cerrados = df_sin_duplicados[df_sin_duplicados['Cerrado'] == 1]
print(len(casos_cerrados))
# Contar casos cerrados por persona (modificador)
cantidad_cerrados = casos_cerrados.groupby('Modificado por')['Número del caso'].nunique().reset_index(name='Casos Cerrados')

# Contar cantidad de casos modificados por persona
cantidad_modificados = df_sin_duplicados.groupby('Modificado por')['Número del caso'].nunique().reset_index(name='Casos Modificados')

# Fusionar los conteos
informe_final = pd.merge(cantidad_cerrados, cantidad_modificados, on='Modificado por', how='outer').fillna(0)

# Calcular la proporción
informe_final['Proporcion Cerrados/Modificados'] = informe_final['Casos Cerrados'] / informe_final['Casos Modificados']
informe_final['Proporcion Cerrados/Modificados'] = informe_final['Proporcion Cerrados/Modificados'].replace([float('inf'), float('nan')], 0)
informe_final['Fecha'] = df['Fecha de apertura'].iloc[0]
print(informe_final['Proporcion Cerrados/Modificados'] / len(informe_final['Proporcion Cerrados/Modificados'] ))
print(informe_final['Casos Cerrados'].sum())
print(informe_final['Casos Modificados'].sum())
print(informe_final)
informe_final.to_clipboard(index=False,header=False, decimal=',')