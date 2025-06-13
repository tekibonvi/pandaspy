import sys
import pandas as pd
from modules.data import id_0810
from modules.funciones import limpiar_excel
from modules.funciones import formatear_decimales
from auth import upload_data

def tiempos(informe_detalle_agentes, informe_pausas):
    agentes =limpiar_excel(informe_detalle_agentes)
    pausas = pd.read_excel(informe_pausas)

    
    agentes_filtered = agentes[agentes['ID de agente'].isin(id_0810) & (agentes['Tiempo de conversación\t']!= "00:00:00")]
    
    agentes_filtered['Tiempo de conversación\t']= pd.to_timedelta(agentes_filtered['Tiempo de conversación\t'])
    agentes_filtered['Tiempo en espera\t']= pd.to_timedelta(agentes_filtered['Tiempo en espera\t'])
    agentes_filtered['Tiempo de trabajo\t']= pd.to_timedelta(agentes_filtered['Tiempo de trabajo\t'])
    fecha =  pd.to_datetime(agentes_filtered['Hora de inicio de llamada'].iloc[0], format='%d/%m/%y %H:%M:%S').date()
    t_conversacion = agentes_filtered['Tiempo de conversación\t'].sum().total_seconds()
    t_espera = agentes_filtered['Tiempo en espera\t'].sum().total_seconds()
    t_trabajo = agentes_filtered['Tiempo de trabajo\t'].sum().total_seconds()
    pausas_filtered = pausas[pausas['Motivo']=="Work"]
    work = pausas_filtered["Estados"].sum().total_seconds()
    llamadas = len(agentes_filtered["Tipo de llamada"])
    tml = t_conversacion/llamadas
    tmo = (work + t_conversacion + t_espera + t_trabajo)/llamadas
    tmo = formatear_decimales(tmo)
    tml = formatear_decimales(tml)
    resultados = {
      'Fecha' : [fecha],
      'TMO' : [tmo],
      'TML' : [tml]
    }
    excel = pd.DataFrame(resultados)
    excel.to_clipboard(index = False, header = False)

    print("\x1b[1;32m"+">>> TIEMPOS TOTALES <<< "+"\x1b[1;37m")
    return(excel)

def tiempos_por_agente(informe_detalle_agentes, informe_pausas):
  informe_detalle_agentes = limpiar_excel(informe_detalle_agentes)
  informe_pausas = pd.read_excel(informe_pausas)
  columnas = ['Tiempo Total', 'Llamadas',"Estados",'Tiempo de conversación\t']

  informe_detalle_agentes = informe_detalle_agentes[informe_detalle_agentes['ID de agente'].isin(id_0810) & (informe_detalle_agentes['Tiempo de conversación\t']!='00:00:00')]

  informe_detalle_agentes['Tiempo de conversación\t']= pd.to_timedelta(informe_detalle_agentes['Tiempo de conversación\t'])
  informe_detalle_agentes['Tiempo en espera\t']= pd.to_timedelta(informe_detalle_agentes['Tiempo en espera\t'])
  informe_detalle_agentes['Tiempo de trabajo\t']= pd.to_timedelta(informe_detalle_agentes['Tiempo de trabajo\t'])

#  informe_detalle_agentes['"Hora inicio de llamada'] = pd.to_datetime(informe_detalle_agentes["Hora de inicio de llamada"], format='%d/%m/%y %H:%M:%S').date()
  informe_detalle_agentes['Tiempo Total'] = informe_detalle_agentes['Tiempo de conversación\t'] + informe_detalle_agentes['Tiempo en espera\t'] + informe_detalle_agentes['Tiempo de trabajo\t']

  detalle_cant_llamadas = informe_detalle_agentes.groupby(['Nombre del agente']).size().reset_index(name="Llamadas")
  #informe_detalle_agentes = informe_detalle_agentes.groupby(['Nombre del agente'])['Tiempo Total'].sum()
  informe_detalle_agentes = informe_detalle_agentes.groupby(['Nombre del agente']).agg(
    {'Tiempo Total': 'sum', 'Tiempo de conversación\t': 'sum'}
)
  informe_pausas = informe_pausas[informe_pausas["Motivo"] == 'Work']
  informe_pausas = informe_pausas.rename(columns = {'Agente': 'Nombre del agente'}).drop(columns="Motivo")
  
  informe_tmo = pd.merge(informe_detalle_agentes,informe_pausas, on = 'Nombre del agente',how='left').fillna("0")
  informe_tmo = pd.merge(informe_tmo,detalle_cant_llamadas, on = 'Nombre del agente',how='left').fillna("0")
  informe_tmo['Tiempo Total'] = pd.to_timedelta(informe_tmo['Tiempo Total']).dt.total_seconds()
  informe_tmo['Estados'] = pd.to_timedelta(informe_tmo['Estados']).dt.total_seconds()
  informe_tmo['TMO'] =(informe_tmo['Tiempo Total'] + informe_tmo['Estados']) / informe_tmo['Llamadas']
  informe_tmo['TMO'] = informe_tmo['TMO'].apply(formatear_decimales)
  informe_tmo['TML'] = informe_tmo["Tiempo de conversación\t"] / informe_tmo["Llamadas"]
  informe_tmo['TML'] = pd.to_timedelta(informe_tmo['TML']).dt.total_seconds()
  informe_tmo['TML'] = informe_tmo['TML'].apply(formatear_decimales)
  informe_tmo['Nombre del agente'] = informe_tmo['Nombre del agente'].str.upper()
  informe_tmo['Nombre del agente'] = informe_tmo['Nombre del agente'].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Í', 'I').str.replace('Ó', 'O').str.replace('Ú', 'U')
  informe_tmo = informe_tmo.drop(columns = columnas)
  informe_tmo.to_clipboard(index=False, header=False)


  print(f"\x1b[1;32m"+ "                                          >> TMO "+ "\x1b[1;37m")
  print(informe_tmo)
  


informe_detalle_agentes = sys.argv[1]
informe_pausas = sys.argv[2]
tiempos(informe_detalle_agentes, informe_pausas)
input()
tiempos_por_agente(informe_detalle_agentes,informe_pausas)