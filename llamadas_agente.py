import sys
import pandas as pd
from modules.funciones import limpiar_excel
from modules.data import id_0810
from modules.funciones import formatear_decimales





def llamadas_por_agente(informe_detalle_agentes, detalle_sistema_agente):
    df_det_agente = limpiar_excel(informe_detalle_agentes)
    df_det_agente = df_det_agente[df_det_agente['ID de agente'].isin(id_0810) & (df_det_agente['Tiempo de conversación\t']!= "00:00:00")]
    
    df_det_agente['Tipo de llamada'] = df_det_agente['Tipo de llamada'].apply(lambda t: 'Entrante' if t.startswith('Inbound') else ('Saliente'))
    
    df_det_sistema = limpiar_excel(detalle_sistema_agente)
    df_det_sistema = df_det_sistema[(df_det_sistema["Tiempo de conversación"] == "00:00:00") & (df_det_sistema["Tiempo de timbre"] == "00:00:12")]
    df_det_sistema = df_det_sistema.groupby(['Nombre del agente']).size().reset_index(name='Abandonadas')

    df_det_agente = df_det_agente.groupby(['Nombre del agente'])['Tipo de llamada'].value_counts().unstack(fill_value=0).rename(columns={'Entrante': 'Total Entrantes', 'Saliente': 'Total Salientes'})
    df_llamadas = pd.merge(df_det_agente, df_det_sistema, on='Nombre del agente', how='left').fillna(" ")
    df_llamadas['Abandonadas'] = df_llamadas["Abandonadas"]

    df_llamadas['Nombre del agente'] = df_llamadas['Nombre del agente'].str.upper()
    df_llamadas['Nombre del agente'] = df_llamadas['Nombre del agente'].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Í', 'I').str.replace('Ó', 'O').str.replace('Ú', 'U')

    print(df_llamadas)
    print(df_det_sistema)
    print(df_llamadas["Total Entrantes"].sum())
    df_llamadas.to_clipboard(header=False, index=False)
    
    #falta % de completo de couching



informe_detalle_agentes = sys.argv[1]
detalle_sistema_agente = sys.argv[2]
llamadas_por_agente(informe_detalle_agentes, detalle_sistema_agente)