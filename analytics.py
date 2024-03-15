import pdb

import pandas as pd
from Database import DataBase, create_engine_easily
import io
import matplotlib as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random


def get_inscritos():
    engine = create_engine_easily()

    consulta = 'SELECT * FROM VW_INSCRITOS'
    df_inscritos = pd.read_sql(consulta, engine)
    return df_inscritos


def organize_inscritos():
    df = get_inscritos()
    df_ = df.reset_index(drop='True')
    '''df_.rename(columns={'nome_turma': 'TURMA',
                        'horario': 'HORARIO',
                        'nascimento': 'DATA_NASCIMENTO',
                        'protocol': 'PROTOCOLO',
                        'phone': 'TELEFONE',
                        'id': 'ID_TURMA'}, inplace=True)'''
    #df_.columns = [str(col).upper() for col in df_.columns]

    colunas = ['ID', 'NOME', 'CPF', 'DATA_NASCIMENTO', 'TELEFONE', 'EMAIL', 'CEP', 'ENDERECO', 'ID_TURMA', 'TURMA', 'HORARIO', 'PROTOCOLO']
    df_ = df_[colunas].sort_values(by=['ID_TURMA'])

    return df_.reset_index(drop='True')

def get_inscrito_by_cpf(cpf):

    df = get_inscritos()
    df = df[df['CPF'] == cpf]

    colunas = ['NOME', 'CPF', 'NOME', 'TURMA']
    df = df[colunas]
    if not df.empty:
        return df.reset_index(drop='True')
    else:
        return str('Inscrição não encontrada!')


def create_sorteados(params):
    df = organize_inscritos()
    db_obj = DataBase()
    db_obj.create_connection()

    for k, v in params.items():

        df_turma = df[df['ID_TURMA'] == k]
        id_inscricao = list(df_turma['ID'])

        sorteados_turma = []
        count = 0
        while count < v:
            sorteado = random.choice(id_inscricao)
            if sorteado not in sorteados_turma:
                sorteados_turma.append(sorteado)
                count += 1

        '''df_sorteados_turma = df_turma[df_turma['ID'].isin(sorteados_turma)]
        df_sorteados_turma = df_sorteados_turma.reset_index(drop='True')
        df_sorteados_turma.index = df_sorteados_turma.index.map(lambda x: x + 1)

        df_sorteados = pd.concat([df_sorteados, df_sorteados_turma])'''
        db_obj.insert_sorteados(sorteados_turma)


def create_sorteio():
    '''params = {3001: 8,
              3002: 8,
              3003: 10,
              3004: 10,
              3005: 10,
              3006: 8,
              3007: 8,
              3008: 10,
              3009: 10,
              3010: 10}'''
    params = {3011: 25,
              3012: 25}

    db_obj = DataBase()
    db_obj.create_connection()
    engine = create_engine_easily()

    consulta = 'SELECT * FROM Sorteados'
    lista_sorteados = pd.read_sql(consulta, engine)

    if lista_sorteados.empty:
        create_sorteados(params)
        lista_sorteados = pd.read_sql(consulta, engine)

    df_inscritos = organize_inscritos()
    df_sorteados = df_inscritos[df_inscritos['ID'].isin(lista_sorteados['id_inscricao'])]
    df_sorteados = df_sorteados.rename(columns={'ID': 'ID_INSCR'})

    _df_sorteados = pd.merge(df_sorteados, lista_sorteados, left_on='ID_INSCR', right_on='id_inscricao', how='left')
    _df_sorteados = _df_sorteados.reset_index(drop=True)

    colunas = ['ID_SORTEIO', 'ID_TURMA', 'CPF_USUARIO', 'NOME', 'TELEFONE', 'EMAIL', 'PROTOCOLO']
    _df_sorteados = _df_sorteados.rename(columns={'CPF': 'CPF_USUARIO', 'id': 'ID_SORTEIO'})
    #_df_sorteados['ID_SORTEIO'] = _df_sorteados.index
    _df_sorteados = _df_sorteados[colunas]
    _df_sorteados = _df_sorteados.sort_values(by=['ID_SORTEIO'])

    return _df_sorteados
