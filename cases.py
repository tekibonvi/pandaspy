import sys
import pandas as pd


def cases(csv_cases):
    df_cases = pd.read_csv(csv_cases, encoding='latin1', sep=';')
    date = df_cases.groupby("Creado por: Nombre completo")['Fecha'].min().reset_index()

    casos_por_agente = df_cases.groupby("Creado por: Nombre completo").size().reset_index(name="Casos creados")
    casos_cerrados = df_cases[df_cases['Cerrado tras su creación'] == 1]
    casos_cerrados = casos_cerrados.groupby('Creado por: Nombre completo').size().reset_index(name= "Casos Cerrados")
    casos = pd.merge(casos_por_agente,casos_cerrados, on='Creado por: Nombre completo', how='left')
    casos['FCR'] = (casos['Casos Cerrados']/casos['Casos creados']).astype(str).str.replace(".",",")
    casos_final = pd.merge(date,casos, on='Creado por: Nombre completo', how='left')
    
    casos_final = casos_final[['Fecha','Creado por: Nombre completo', 'Casos creados', 'Casos Cerrados', 'FCR']]

    casos_final.to_clipboard(header= False, index=False)
    print(casos_final)
    return casos_final






excel = sys.argv[1]


cases(excel)
