import sqlite3
from Databases import DataBase, User
from datetime import datetime
import time
import random
from Validations import Validations

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from tabledef import *

engine = create_engine('sqlite:///ProjetoIntegradorI_2023/users.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin", "password")
session.add(user)

user = User("python", "python")
session.add(user)

user = User("jumpiness", "python")
session.add(user)

# commit the record the database
session.commit()

session.commit()

'''nomes = [['Joao', 'Jose', 'Bruno', 'Aline', 'Carla', 'Maria', 'Dionisia', 'Roberto'],
         ['da Silva', 'Rodrigues', 'Souza', 'dos Santos']]
endereco = [['Rua', 'Avenida'],
            ['Cupertina', 'Campos Salles', 'Invernada', 'Independência', 'Onze de Agosto', 'Don Nery'],
            ['Jurema', 'Parque Portugal', 'Centro', 'Country Club', 'Macuco', 'Vale Verde']]

emails = [['@gmail', '@yahoo', '@outlook', '@hotmail'],
         ['.com.br', '.com']]
obj = DataBase()
obj.create_connection()

for i in range(0, 1032):
    cpf = random.randint(10000000000, 99999999999)
    while 1:
        if Validations.check_cpf_db(cpf):
            break
        else:
            cpf = random.randint(10000000000, 99999999999)

    nome = str(random.choice(nomes[0])) + ' ' + str(random.choice(nomes[1]))
    born = str(random.randint(1, 29)) + '/' + str(random.randint(1, 12)) + '/' + str(random.randint(1940, 2015))
    cep = str(random.randint(13270000, 13279999))
    address = str(random.choice(endereco[0])) + ' ' + \
              str(random.choice(endereco[1])) + ', N-' + \
              str(random.randint(10, 3000)) + ', ' + \
              str(random.choice(endereco[2]))
    phone = str(random.randint(19900000000, 19999999999))
    email = str(nome.replace(' ', '') + str(random.choice(emails[0])) + str(random.choice(emails[1]))).lower()
    turma = str(random.randint(3001, 3011))
    protocol = str(datetime.now())

    post = (cpf, nome, born, cep, address, phone, email, turma, protocol)
    obj.insert_inscritos(post)

    time.sleep(0.5)
    print(protocol)'''
