import sqlite3
from Databases import DataBase
from datetime import datetime

from flask import Flask,  render_template, request
import os
from Validations import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form_inscricao.html')


@app.route('/inscricao')
def inscricao():
    return render_template('form_inscricao.html')


@app.route('/form_cpf')
def form_cpf():
    return render_template('form_cpf.html')


@app.route('/valida-cep/<cep>', methods=['GET', 'POST'])
def valida_cep(cep):
    cep = request.form['cep']
    print(cep)
    validacao = Validations.valida_cep(cep)
    print(validacao)
    return 'True' if validacao else 'False'
        #return form_cpf()
        #return True
    #else:
        #return False
        #return index()

@app.route('/valida_cpf/<cpf>')
#@app.route('/valida_cpf/<cpf>', methods=['GET', 'POST'])
def valida_cpf(cpf):
    #cpf = request.form['cpf']
    print(cpf)
    validacao = Validations.valida_cpf(cpf)
    print(validacao)
    return 'True' if validacao else 'False'
    #if validacao:
    #    return inscricao()
    #else:
    #    return index()


@app.route('/submit', methods=['POST'])
def submit():
    cep = request.form['cep']
    cpf = request.form['cpf']
    name = request.form['nome']
    born = request.form['nascimento']
    address = request.form['endereco']
    phone = request.form['telefone']
    email = request.form['email']
    turma = request.form['turma']

    obj = DataBase()
    obj.create_connection()
    protocol = str(datetime.now())
    post = (cpf, name, born, cep, address, phone, cpf, email, turma, protocol)
    obj.insert_inscritos(post)


if __name__ == '__main__':
    app.run(debug=True)  # Executa a aplicação

