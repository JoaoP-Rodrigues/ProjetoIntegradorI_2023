import sqlite3
from Databases import DataBase
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
from analytics import *
from io import BytesIO
import base64
from flask import Flask,  render_template, request
import os
from Validations import *
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form_inscricao.html')


@app.route('/valida_cep/<cep>', methods=['GET', 'POST'])
def valida_cep(cep):
    validacao = Validations.valida_cep(cep)
    if validacao:
        return 'True'
    else:
        return f'INSCRIÇÃO PERMITIDA SOMENTE PARA MORADORES DE VALINHOS!\nO CEP {cep} NÃO PERTENCE A CIDADE DE VALINHOS!'


@app.route('/valida_cpf/<cpf>', methods=['GET', 'POST'])
def valida_cpf(cpf):

    first_validacao = Validations.cpf_validate(cpf)
    if first_validacao:
        second_validacao = Validations.check_cpf_db(cpf)
        if second_validacao:
            return 'True'
        else:
            return 'ESTE CPF JÁ FOI USADO EM UMA INSCRIÇÃO!'
    else:
        return 'ESTE NÃO É UM NÚMERO VÁLIDO DE CPF!'


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
    post = (cpf, name, born, cep, address, phone, email, turma, protocol)
    obj.insert_inscritos(post)


@app.route('/estatisticas')
def estatisticas():
    inscritos = create_chart()
    #return render_template("stats.html", data=inscritos.to_html())
    return inscritos


@app.route('/plot')
def plot():
    img = BytesIO()
    y = [1, 2, 3, 4, 5]
    x = [0, 2, 1, 3, 4]

    plt.plot(x, y)

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('images.html', plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)  # Executa a aplicação

