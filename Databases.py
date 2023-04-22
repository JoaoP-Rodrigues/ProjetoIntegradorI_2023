import sqlite3
from sqlite3 import Error
import pandas as pd


class DataBase:

    def create_connection(self):
        try:
            path_bd = r'C:/Users/joao_/OneDrive/Documentos2/UNIVESP/04 - Semestre/PI/Projeto_Repositorio/ProjetoIntegradorI_2023/DataBase/Banco_PI.db'
            self.conn = sqlite3.connect(path_bd)
            self.cur = self.conn.cursor()
        except Error as e:
            print(e)

    def get_schema(self, table):
        query = f'SELECT * FROM {table}'
        squema = self.cur.execute(query)
        columns = []
        for col in squema.description:
            columns.append(col[0])
        return tuple(columns)

    def insert_inscritos(self, values):
        chaves = self.get_schema('INSCRICOES')
        query = f'INSERT INTO INSCRICOES {chaves} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.cur.execute(query, values)
        self.conn.commit()

    def insert_users(self, values):
        chaves = self.get_schema('USUARIOS_ADM')
        query = f'INSERT INTO USUARIOS_ADM {chaves} VALUES (?, ?, ?, ?, ?)'
        self.cur.execute(query, values)
        self.conn.commit()

    def query_read(self, query):
        return pd.read_sql_query(query, self.conn)
