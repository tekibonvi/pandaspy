import sys
import pandas as pd



def take_time(excel_1,excel_2):
    print("Toma tiempo -------")
    excel_1 = pd.read_excel(excel_1)
    excel_2 = pd.read_excel(excel_2)

    if excel_1.columns[1] == "Motivo":
        pausas = excel_1
        estados = excel_2
    else:
        pausas = excel_2
        estados = excel_1
    estados['Agente'] = estados['Agente'].str.upper()
    estados['Agente'] = estados['Agente'].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Í', 'I').str.replace('Ó', 'O').str.replace('Ú', 'U')
    pausas['Agente'] = pausas['Agente'].str.upper()
    pausas['Agente'] = pausas['Agente'].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Í', 'I').str.replace('Ó', 'O').str.replace('Ú', 'U')
    estados = estados.pivot(index= 'Agente', columns='Estado', values='Estados').fillna("0")
    pausas = pausas.pivot(index= 'Agente', columns='Motivo', values='Estados').fillna("0")

    estados_pausas = pd.merge(estados,pausas,on="Agente" ,how="left")

    #estados_pausas['Tiempo productivo'] = (estados_pausas['Llamada']+ estados_pausas['Preparado']+ estados_pausas['Reservado']+ estados_pausas['Trabajo']+estados_pausas['Work'] + estados_pausas['Offhook']+  estados_pausas['Coaching'])
    estados_pausas['Tiempo productivo'] = (estados_pausas['Llamada']+ estados_pausas['Preparado']+ estados_pausas['Reservado']+ estados_pausas['Trabajo']+estados_pausas['Work']+ estados_pausas['Campañas'] + estados_pausas['Offhook'])#+estados_pausas['Coaching'])
    estados_pausas['Tiempo de Conexión'] = (estados_pausas['Llamada']+ estados_pausas['Preparado']+ estados_pausas['Reservado']+ estados_pausas['Trabajo']+estados_pausas['No Preparado'])
    estados_pausas['Tiempo Operativo'] =(estados_pausas['Llamada']+ estados_pausas['Reservado']+ estados_pausas['Trabajo']+estados_pausas['Work']) #estados_pausas['Coaching'])
    estados_pausas['Tiempos Improductivos'] = (estados_pausas['Tiempo de Conexión'] - estados_pausas['Descanso'] - estados_pausas['Baño']- estados_pausas['Tiempo productivo'])


    estados_pausas['% Ocupación'] =(estados_pausas['Tiempo Operativo'] / estados_pausas['Tiempo productivo']).astype(str).str.replace('.',',')   
    estados_pausas['Descanso'] = estados_pausas['Descanso'].dt.total_seconds()
    estados_pausas['Baño'] = estados_pausas['Baño'].dt.total_seconds()
    estados_pausas['Tiempos de Conexión'] = estados_pausas['Tiempo de Conexión'].dt.total_seconds()    
    estados_pausas['Tiempo productivo'] =  estados_pausas['Tiempo productivo'].dt.total_seconds()
    estados_pausas['Tiempos Improductivos'] = estados_pausas['Tiempos Improductivos'].dt.total_seconds()
    
    estados_final = estados_pausas.loc[:, ['Tiempo productivo', 'Descanso','Baño','Tiempos Improductivos','Tiempos de Conexión','% Ocupación']]
    print(estados_final)
    estados_final.to_clipboard(header= False)


excel_1 = sys.argv[1]
excel_2 = sys.argv[2]
take_time(excel_1, excel_2)