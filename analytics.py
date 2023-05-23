import pandas as pd
from Databases import DataBase
import io
import matplotlib as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random


def get_inscritos():
    db_obj = DataBase()
    db_obj.create_connection()

    consulta = 'SELECT * FROM VW_INSCRITOS'
    df_inscritos = db_obj.query_read(consulta)
    return df_inscritos


def create_chart():
    df = get_inscritos()
    df_ = df.reset_index(drop='True')
    df_.rename(columns={'NOME_TURMA': 'TURMA', 'HORARIO_AULA': 'HORARIO'}, inplace=True)

    colunas = ['NOME', 'CPF', 'DATA_NASCIMENTO', 'TELEFONE', 'EMAIL', 'CEP', 'ENDERECO', 'ID_TURMA', 'TURMA', 'HORARIO', 'PROTOCOLO']
    df_ = df_[colunas].sort_values(by=['ID_TURMA'])

    return df_.reset_index(drop='True')

def get_inscrito_by_cpf(cpf):
    df = create_chart()
    colunas = ['NOME', 'CPF', 'TURMA', 'HORARIO', 'PROTOCOLO']
    df = df[colunas]
    df = df.loc[df['CPF'] == str(cpf)]
    if not df.empty:
        return df.reset_index(drop='True')
    else:
        return str('Inscrição não encontrada!')


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

        df_sorteados_turma = df_turma.loc[df_turma['CPF'].isin(sorteados_turma)]
        df_sorteados_turma = df_sorteados_turma.reset_index(drop='True')
        df_sorteados_turma.index = df_sorteados_turma.index.map(lambda x: x + 1)

        df_sorteados = pd.concat([df_sorteados, df_sorteados_turma])

    colunas = ['TURMA', 'NOME', 'CPF', 'DATA_NASCIMENTO', 'TELEFONE', 'EMAIL', 'CEP', 'ENDERECO', 'PROTOCOLO']
    df_sorteados = df_sorteados[colunas]

    return df_sorteados

def create_sorteio():
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
        colunas = ['ID_SORTEIO', 'ID_TURMA', 'CPF_USUARIO', 'NOME', 'TELEFONE', 'EMAIL', 'PROTOCOLO']
        df_sorteados = create_sorteados(params)

        df_sorteados = df_sorteados.rename(columns={'CPF': 'CPF_USUARIO', 'TURMA': 'ID_TURMA'})
        df_sorteados['ID_SORTEIO'] = df_sorteados.index
        df_sorteados = df_sorteados[colunas]

        db_obj.insert_sorteados(df_sorteados)

    return df_sorteados