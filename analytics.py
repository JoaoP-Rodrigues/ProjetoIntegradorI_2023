import pandas as pd
from Databases import DataBase

obj = DataBase()
obj.create_connection()

consulta = 'SELECT * FROM INSCRICOES WHERE TURMA = "3001"'
df_inscritos = obj.query_read(consulta)

print(df_inscritos.columns)
