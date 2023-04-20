import sqlite3
from Databases import DataBase
from datetime import datetime

from flask import Flask,  render_template, request
import os
from Validations import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/inscricao')
def inscricao():
    return render_template('form_inscricao.html')


@app.route('/valida-cep', methods=['POST'])
def process_form():
    cep = request.form['cep']
    validacao = Validations.valida_cep(cep)
    if validacao:
        return inscricao()
    else:
        return 'Incrição permitida somente para moradores da cidade de Valinhos.'


@app.route('/submit', methods=['POST'])
def submit():
    cep = request.form['cep']
    cpf = request.form['cpf']
    name = request.form['nome']
    born = request.form['nascimento']
    address = request.form['endereco']
    phone = request.form['telefone']
    email = request.form['email']
    obj = DataBase()
    obj.create_connection()
    protocol = str(datetime.now())

    post = (cpf, name, born, cep, address, phone, cpf, email, protocol)
    tabela = 'INSCRICOES'
    obj.insert_inscritos(post)


if __name__ == '__main__':
    app.run(debug=True)  # Executa a aplicação

