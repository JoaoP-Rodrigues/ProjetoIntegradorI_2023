import pandas as pd
from Databases import DataBase
import io
import matplotlib as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random


def get_inscritos(turma="3001"):
    db_obj = DataBase()
    db_obj.create_connection()

    # consulta = f'SELECT * FROM INSCRICOES WHERE TURMA = "{turma}"'
    consulta = 'SELECT * FROM INSCRICOES'
    df_inscritos = db_obj.query_read(consulta)
    return df_inscritos


def create_chart():
    df = get_inscritos()
    df_ = df.groupby(["TURMA"]).count()
    df_ = df_.reset_index()
    return df_.to_html()


def create_sorteados(params):
    db_obj = DataBase()
    db_obj.create_connection()


    df_sorteados = pd.DataFrame()

    for k, v in params.items():
        query = f'SELECT * FROM INSCRICOES WHERE TURMA = {k}'
        df_turma = db_obj.query_read(query)
        id_turma = list(df_turma['CPF'])

        sorteados_turma = []
        count = 0
        while count < v:
            sorteado = random.choice(id_turma)
            if sorteado not in sorteados_turma:
                sorteados_turma.append(sorteado)
                count += 1
            #print(df_turma.loc[df_turma['CPF'] == sorteado])
        df_sorteados_turma = df_turma.loc[df_turma['CPF'].isin(sorteados_turma)]
        df_sorteados = pd.concat([df_sorteados, df_sorteados_turma])

    return df_sorteados

def sorteio():
    params = {3001: 8,
              3002: 8,
              3003: 10,
              3004: 10,
              3005: 10,
              3006: 8,
              3007: 8,
              3008: 10,
              3009: 10,
              3010: 10}

    db_obj = DataBase()
    db_obj.create_connection()
    consulta = 'SELECT * FROM SORTEADOS'
    df_sorteados = db_obj.query_read(consulta)
    if len(df_sorteados) == 0:
        df_sorteados = create_sorteados(params)

    for k in params.keys():
        print(df_sorteados.loc[df_sorteados['TURMA'] == k])

sorteio()
