import sqlite3
from Databases import DataBase

'''obj = DataBase()
obj.create_connection()
post = ('12345678910', 'Joao Paulo', '13272999', 'Rua Fulano da Silva, 350', '19988997766', '11223344@aluno.univesp.br')
tabela = 'INSCRICOES'
obj.insert_inscritos(post)'''

from flask import Flask,  render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)  # Executa a aplicação

