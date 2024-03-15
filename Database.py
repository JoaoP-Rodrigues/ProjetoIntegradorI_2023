import pdb

import pyodbc
import yaml
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

with open('credenciais.yml', 'r') as file:
    credentials = yaml.safe_load(file)

server_name = credentials['server']
database_name = credentials['database']
logon = credentials['logon']
password = credentials['password']
driver = credentials['driver']
url_con = f'mssql+pyodbc://{logon}:{password}@{server_name}/{database_name}?driver={driver}'

def create_engine_easily():
    engine = create_engine(url_con)

    return engine

class DataBase:

    def create_connection(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={driver};SERVER={server_name};DATABASE={database_name};UID={logon};PQD={password};Trusted_Connection=True')
            self.cursor = self.connection.cursor()
        except Exception as ex:
            print(ex)

    def get_schema(self, table):
        query = f'SELECT * FROM {table}'
        squema = self.cursor.execute(query)
        columns = []
        for col in squema.description:
            columns.append(col[0])
        if 'id' in columns:
            columns.remove('id')
        return tuple(columns)

    def insert_inscritos(self, values):
        chaves = '(cpf, nome, nascimento, CEP, endereco, phone, email, protocol, id_turma)'
        query = f"INSERT INTO Inscricoes {chaves} VALUES {values}"

        try:
            self.cursor.execute(query)
        except pyodbc.Error as e:
            print(e)
        self.connection.commit()

    def insert_users(self, values):

        query = 'INSERT INTO usuarios (name, email, password) VALUES (?, ?, ?)'
        self.cursor.execute(query, values)
        self.connection.commit()

    def insert_sorteados(self, sorteados):

        #sorteados.to_sql('Sorteados', con=self.connection, if_exists='append', index=False)
        for inscrito in sorteados:
            query = f"INSERT INTO Sorteados (id_inscricao) VALUES (?)"
            self.cursor.execute(query, inscrito)
            self.connection.commit()

engine = create_engine_easily()
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)  # Adiciona uma coluna de chave primária
    email = Column(String)
    password = Column(String)
    name = Column(String)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def insert_adm(self, email, password, name):
        sub_engine = create_engine(url_con, echo=True)

        # create a Session
        Session = sessionmaker(bind=sub_engine)
        session = Session()

        user = Usuario(email, password, name)
        session.add(user)

        # commit the record the database
        session.commit()
