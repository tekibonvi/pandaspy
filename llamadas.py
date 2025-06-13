import sys
import pandas as pd
import pyperclip
from modules.data import id_0810
from modules.funciones import limpiar_excel
from asa import *


def llamadas_total(informe_entrantes, informe_detalle_agentes, detalle_sistema):
    excel = limpiar_excel(informe_entrantes)
    excel_agentes = limpiar_excel(informe_detalle_agentes)
    excel_0810 = excel[(excel['Nombre de CSQ'] == "0810")  | (excel["Nombre de CSQ"] == "CSQ_OSPEDEA")]
    excel_salientes = excel_agentes[excel_agentes['ID de agente'].isin(id_0810) & (excel_agentes["Tiempo de conversación	"] != '00:00:00')]
    excel_salientes = excel_salientes[(excel_salientes['Tipo de llamada']== "Outbound on IPCC") |  (excel_salientes['Tipo de llamada'] == "Outbound on IPCC, Transfer-out")]

    fecha =  pd.to_datetime(excel_0810["Hora de inicio del intervalo"].iloc[0], format='%d/%m/%y %H:%M:%S').date()
    abandonadas = excel_0810["Llamadas abandonadas"].astype(int).sum()
    entrantes = excel_0810["Llamadas presentadas"].astype(int).sum()
    atendidas = excel_0810["Llamadas manejadas"].astype(int).sum()
    salientes = len(excel_salientes["Tipo de llamada"])
    Total = entrantes + salientes
    Eficiencia = (atendidas/entrantes)
    Sla = (excel_0810["Llamadas manejadas < Nivel de servicio"].astype(int).sum()/atendidas)
    Asa = tiempo_med_espera(detalle_sistema)
    Rellamado = tasa_rellamado(detalle_sistema)
    
    Totales = {'Fecha': [fecha],
    'Entrantes': [entrantes],
    'Atendidas': [atendidas],
    'Salientes':[salientes],
    'Abandonadas':[abandonadas],
    'Total':[Total],
    'Eficiencia':[Eficiencia],
    'Sla':[Sla],
    'Asa':[Asa],
    'Rellamado':[Rellamado]
    }
    excelfinal = pd.DataFrame(Totales)
    excelfinal.to_clipboard(index = False, header = False)
    print(excelfinal)
    print("\x1b[1;32m"+">>> LLAMADAS HOJA 1 <<< "+"\x1b[1;37m")
    input()

def tablero_llamadas(informe_entrantes):
    excel = limpiar_excel(informe_entrantes)
    excel_0810 = excel[(excel['Nombre de CSQ'] == "0810")  | (excel["Nombre de CSQ"] == "CSQ_OSPEDEA")]
    excel_0810['Hora de inicio del intervalo'] = pd.to_datetime(excel_0810['Hora de inicio del intervalo'], format='%d/%m/%y %H:%M:%S')
    excel_0810['Fecha']=excel_0810['Hora de inicio del intervalo'].dt.strftime('%d/%m/%y')
    excel_0810['Hora']=excel_0810['Hora de inicio del intervalo'].dt.hour
    excel_0810['Llamadas manejadas'] = excel_0810['Llamadas manejadas'].astype(int)
    excel_0810['Llamadas presentadas'] = excel_0810['Llamadas presentadas'].astype(int)
    excel_0810['Llamadas manejadas < Nivel de servicio']  = excel_0810['Llamadas manejadas < Nivel de servicio'] .astype(int)
    excel_0810['Eficiencia'] = (excel_0810['Llamadas manejadas']/excel_0810['Llamadas presentadas']).astype(str).str.replace('.',',')
    excel_0810['Sla'] = (excel_0810['Llamadas manejadas < Nivel de servicio'] / excel_0810['Llamadas manejadas']).astype(str).str.replace('.',',')
    tabla_llamadas = excel_0810[['Fecha','Hora','Llamadas presentadas','Llamadas manejadas','Llamadas abandonadas', 'Eficiencia','Sla']]
    print(tabla_llamadas)
    tabla_llamadas.to_clipboard(index = False, header=False)
    print("\x1b[1;32m"+">>> RECIBIDAS-ATENDIDAS-ABANDONADAS <<< "+"\x1b[1;37m")
    input()

if __name__ == "__main__":
    informe_entrantes  = sys.argv[1]
    informe_detalle_agentes = sys.argv[2]
    detalle = sys.argv[3]

    llamadas_total(informe_entrantes, informe_detalle_agentes, detalle)
    tablero_llamadas(informe_entrantes)