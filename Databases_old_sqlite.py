import sqlite3
from sqlite3 import Error
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
        chaves = self.get_schema('Inscricoes')
        query = f'INSERT INTO Inscricoes {chaves} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.cur.execute(query, values)
        self.conn.commit()

    def insert_users(self, values):
        #chaves = self.get_schema('users')
        query = f'INSERT INTO users (name, email, password) VALUES (?, ?, ?)'
        self.cur.execute(query, values)
        self.conn.commit()

    def insert_sorteados(self, sorteados):

        sorteados.to_sql('SORTEADOS', con=self.conn, if_exists='append', index=False)
        self.conn.commit()

    def query_read(self, query):
        return pd.read_sql_query(query, self.conn)


engine = create_engine('sqlite:///C:/Users/joao_/OneDrive/Documentos2/UNIVESP/04 - Semestre/PI/Projeto_Repositorio/ProjetoIntegradorI_2023/DataBase/Banco_PI.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def insert_adm(self, email, password, name):
        sub_engine = create_engine('sqlite:///C:/Users/joao_/OneDrive/Documentos2/UNIVESP/04 - Semestre/PI/Projeto_Repositorio/ProjetoIntegradorI_2023/DataBase/Banco_PI.db', echo=True)

        # create a Session
        Session = sessionmaker(bind=sub_engine)
        session = Session()

        user = User(email, password, name)
        session.add(user)

        # commit the record the database
        session.commit()
