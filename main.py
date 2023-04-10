import sqlite3
from databases import DataBase

obj = DataBase()
obj.create_connection()
post = ('98765432102', 'Joao Paulo', '13272350', 'Rua Joao do Ze, 350', '19988997766', '2102210@aluno.univesp.br')
tabela = 'INSCRICOES'
obj.insert_inscritos(post)
